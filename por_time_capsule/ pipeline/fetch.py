"""
pipeline/fetch.py

Stage: 1. Fetch
- Завантажує HN frontpage за дату
- Тягне контент статей
- Тягне коментарі через Algolia API
- Складає все в data/<date>/...
"""

import json
import re
import html
import time
import urllib.request
import urllib.error
from dataclasses import dataclass, field, asdict
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
from typing import List, Tuple, Optional

import requests


# -----------------------------------------------------------------------------
# Data structures
# -----------------------------------------------------------------------------

@dataclass
class Article:
    rank: int
    title: str
    url: str
    hn_url: str
    points: int
    author: str
    comment_count: int
    item_id: str


@dataclass
class Comment:
    id: str
    author: str
    text: str
    children: list = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "author": self.author,
            "text": self.text,
            "children": [c.to_dict() for c in self.children],
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Comment":
        return cls(
            id=d["id"],
            author=d["author"],
            text=d["text"],
            children=[cls.from_dict(c) for c in d.get("children", [])],
        )


# -----------------------------------------------------------------------------
# HTML Parsing
# -----------------------------------------------------------------------------

class HNFrontpageParser(HTMLParser):
    """Parse HN frontpage HTML to extract article listings."""

    def __init__(self):
        super().__init__()
        self.articles: List[Article] = []
        self.current_article: dict = {}
        self.in_titleline = False
        self.in_title_link = False
        self.in_subline = False
        self.in_score = False
        self.in_user = False
        self.in_subline_links = False
        self.current_rank = 0

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "span" and attrs_dict.get("class") == "rank":
            self.in_titleline = True
        if tag == "span" and attrs_dict.get("class") == "titleline":
            self.in_titleline = True
        if self.in_titleline and tag == "a" and "href" in attrs_dict:
            if not self.current_article.get("title"):
                self.current_article["url"] = attrs_dict["href"]
                self.in_title_link = True
        if tag == "span" and attrs_dict.get("class") == "subline":
            self.in_subline = True
        if self.in_subline:
            if tag == "span" and attrs_dict.get("class") == "score":
                self.in_score = True
            if tag == "a" and attrs_dict.get("class") == "hnuser":
                self.in_user = True
            if tag == "a" and "href" in attrs_dict and "item?id=" in attrs_dict["href"]:
                href = attrs_dict["href"]
                item_id = href.split("item?id=")[-1]
                self.current_article["item_id"] = item_id
                self.current_article["hn_url"] = f"https://news.ycombinator.com/{href}"
                self.in_subline_links = True

    def handle_data(self, data):
        data = data.strip()
        if not data:
            return
        if self.in_title_link:
            self.current_article["title"] = data
        if self.in_score:
            try:
                self.current_article["points"] = int(data.split()[0])
            except (ValueError, IndexError):
                self.current_article["points"] = 0
        if self.in_user:
            self.current_article["author"] = data
        if self.in_subline_links:
            if "comment" in data.lower():
                try:
                    self.current_article["comment_count"] = int(data.split()[0])
                except (ValueError, IndexError):
                    self.current_article["comment_count"] = 0
            elif data.lower() == "discuss":
                self.current_article["comment_count"] = 0
        if data.endswith(".") and data[:-1].isdigit():
            self.current_rank = int(data[:-1])
            self.current_article["rank"] = self.current_rank

    def handle_endtag(self, tag):
        if tag == "a":
            self.in_title_link = False
            self.in_user = False
            self.in_subline_links = False
        if tag == "span":
            self.in_score = False
            if self.in_titleline:
                self.in_titleline = False
        if tag == "tr" and self.in_subline:
            self.in_subline = False
            if self.current_article.get("title") and self.current_article.get("item_id"):
                self.articles.append(
                    Article(
                        rank=self.current_article.get("rank", 0),
                        title=self.current_article.get("title", ""),
                        url=self.current_article.get("url", ""),
                        hn_url=self.current_article.get("hn_url", ""),
                        points=self.current_article.get("points", 0),
                        author=self.current_article.get("author", ""),
                        comment_count=self.current_article.get("comment_count", 0),
                        item_id=self.current_article.get("item_id", ""),
                    )
                )
            self.current_article = {}


class ArticleTextParser(HTMLParser):
    """Extract main text content from article HTML."""

    def __init__(self):
        super().__init__()
        self.text_parts: List[str] = []
        self.skip_tags = {
            "script",
            "style",
            "nav",
            "header",
            "footer",
            "aside",
            "noscript",
            "iframe",
        }
        self.skip_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag in self.skip_tags:
            self.skip_depth += 1
        if tag == "br":
            self.text_parts.append("\n")

    def handle_endtag(self, tag):
        if tag in self.skip_tags and self.skip_depth > 0:
            self.skip_depth -= 1
        if tag in (
            "p",
            "div",
            "article",
            "section",
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
        ):
            self.text_parts.append("\n\n")

    def handle_data(self, data):
        if self.skip_depth > 0:
            return
        text = data.strip()
        if text:
            self.text_parts.append(text + " ")

    def get_text(self) -> str:
        text = "".join(self.text_parts)
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        text = re.sub(r" +\n", "\n", text)
        return text.strip()


# -----------------------------------------------------------------------------
# Fetching helpers
# -----------------------------------------------------------------------------

MAX_ARTICLE_CHARS = 15000


def get_data_dir(target_date: str) -> Path:
    return Path("data") / target_date


def fetch_url(url: str, retries: int = 5, timeout: int = 15) -> str:
    """Fetch URL content with retry logic. Uses requests (краще ніж старий urllib-only)."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    }
    for attempt in range(retries):
        try:
            if attempt > 0:
                wait_time = 2**attempt
                print(f"  Retry {attempt}/{retries-1} after {wait_time}s...")
                time.sleep(wait_time)
            response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            return response.text
        except requests.exceptions.HTTPError as e:
            if e.response is not None and e.response.status_code == 403 and attempt < retries - 1:
                print("  Got 403, will retry...")
                continue
            raise
    raise RuntimeError(f"Failed to fetch {url} after {retries} retries")


def fetch_frontpage(day: str) -> List[Article]:
    url = f"https://news.ycombinator.com/front?day={day}"
    print(f"Fetching frontpage: {url}")
    page_html = fetch_url(url)
    parser = HNFrontpageParser()
    parser.feed(page_html)
    return parser.articles


def clean_html_to_text(text: str) -> str:
    """Convert HN comment HTML to clean markdown-ish text."""
    text = html.unescape(text)
    text = re.sub(r'<a href="([^"]+)"[^>]*>([^<]+)</a>', r"[\2](\1)", text)
    text = re.sub(r"<i>([^<]+)</i>", r"*\1*", text)
    text = re.sub(r"<b>([^<]+)</b>", r"**\1**", text)
    text = re.sub(r"<code>([^<]+)</code>", r"`\1`", text)
    text = text.replace("<p>", "\n\n").replace("</p>", "")
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def fetch_comments(item_id: str) -> List[Comment]:
    """Fetch all comments for an HN item using Algolia API."""
    url = f"https://hn.algolia.com/api/v1/items/{item_id}"
    print(f"  Fetching comments: {item_id}")
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=30) as response:
        data = json.loads(response.read().decode("utf-8"))

    def parse_children(children) -> List[Comment]:
        comments: List[Comment] = []
        for child in children:
            if child.get("type") != "comment" or child.get("text") is None:
                continue
            comment = Comment(
                id=str(child.get("id", "")),
                author=child.get("author") or "[deleted]",
                text=clean_html_to_text(child.get("text", "")),
                children=parse_children(child.get("children", [])),
            )
            comments.append(comment)
        return comments

    return parse_children(data.get("children", []))


def fetch_article_content(url: str) -> Tuple[str, Optional[str]]:
    """Fetch and extract text from article URL. Returns (text, error)."""
    if not url.startswith(("http://", "https://")):
        return "", "Not a web URL"
    if any(x in url for x in [".pdf", "youtube.com", "youtu.be", "twitter.com", "x.com"]):
        return "", "Skipped URL type"

    print(f"  Fetching article: {url[:60]}...")
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            content_type = response.headers.get("Content-Type", "")
            if "text/html" not in content_type and "application/xhtml" not in content_type:
                return "", f"Not HTML: {content_type}"
            data = response.read(5 * 1024 * 1024)
            try:
                page_html = data.decode("utf-8")
            except UnicodeDecodeError:
                page_html = data.decode("latin-1", errors="replace")

        page_html = html.unescape(page_html)
        parser = ArticleTextParser()
        parser.feed(page_html)
        text = parser.get_text()

        if len(text) < 100:
            return "", "Article too short or failed to extract"

        if len(text) > MAX_ARTICLE_CHARS:
            truncate_at = text.rfind(". ", MAX_ARTICLE_CHARS - 500, MAX_ARTICLE_CHARS)
            if truncate_at == -1:
                truncate_at = MAX_ARTICLE_CHARS
            text = text[: truncate_at + 1] + "\n\n[TRUNCATED]"

        return text, None

    except urllib.error.HTTPError as e:
        return "", f"HTTP {e.code}"
    except urllib.error.URLError as e:
        return "", f"URL error: {e.reason}"
    except Exception as e:
        return "", f"{type(e).__name__}: {e}"


# -----------------------------------------------------------------------------
# Stage 1: fetch
# -----------------------------------------------------------------------------

def stage_fetch(target_date: str, limit: Optional[int] = None) -> None:
    """Stage 1: Fetch frontpage and all article data."""
    data_dir = get_data_dir(target_date)
    data_dir.mkdir(parents=True, exist_ok=True)

    frontpage_file = data_dir / "frontpage.json"

    # Frontpage cache
    if frontpage_file.exists():
        print(f"Loading cached frontpage from {frontpage_file}")
        with open(frontpage_file) as f:
            articles = [Article(**a) for a in json.load(f)]
    else:
        articles = fetch_frontpage(target_date)
        with open(frontpage_file, "w") as f:
            json.dump([asdict(a) for a in articles], f, indent=2)
        print(f"Saved frontpage to {frontpage_file}")

    if limit:
        articles = articles[:limit]

    print(f"\nFetching data for {len(articles)} articles...")

    for article in articles:
        article_dir = data_dir / article.item_id
        article_dir.mkdir(exist_ok=True)

        # meta.json
        meta_file = article_dir / "meta.json"
        if not meta_file.exists():
            with open(meta_file, "w") as f:
                json.dump(asdict(article), f, indent=2)

        # article content
        article_file = article_dir / "article.txt"
        error_file = article_dir / "article_error.txt"
        if not article_file.exists() and not error_file.exists():
            text, error = fetch_article_content(article.url)
            if error:
                error_file.write_text(error)
            else:
                article_file.write_text(text)
            time.sleep(0.5)

        # comments
        comments_file = article_dir / "comments.json"
        if not comments_file.exists():
            comments = fetch_comments(article.item_id)
            with open(comments_file, "w") as f:
                json.dump([c.to_dict() for c in comments], f, indent=2)
            time.sleep(0.2)

    print(f"\nFetch complete. Data saved to {data_dir}")


if __name__ == "__main__":
    # Маленький CLI тільки для stage_fetch
    import argparse

    parser = argparse.ArgumentParser(description="HN fetch stage")
    parser.add_argument("--date", default=None, help="YYYY-MM-DD, default = 10 years ago")
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    if args.date:
        target_date = args.date
    else:
        today = date.today()
        target_date = today.replace(year=today.year - 10).isoformat()

    print(f"Target date: {target_date}")
    stage_fetch(target_date, args.limit)
