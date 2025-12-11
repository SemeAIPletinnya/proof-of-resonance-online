"""
pipeline/por_eval.py

Stages:
2. prompt   - з Article + тексту + коментарів -> prompt.md
3. analyze  - ганяємо LLM (GPT-5.1 / Grok / що завгодно) по prompt.md
              + можемо одразу рахувати PoR-метрики для відповіді
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import List, Optional

from datetime import date

from .fetch import Article, Comment, get_data_dir, clean_html_to_text
from por_core.metrics import compute_por_for_response  # наша PoR-надбудова (можна залишити поки як stub)


PROMPT_TEMPLATE = """The following is an article that appeared on Hacker News 10 years ago, and the discussion thread.

Let's use our benefit of hindsight now in 6 sections:

1. Give a brief summary of the article and the discussion thread.
2. What ended up happening to this topic? (research the topic briefly and write a summary)
3. Give out awards for "Most prescient" and "Most wrong" comments, considering what happened.
4. Mention any other fun or notable aspects of the article or discussion.
5. Give out grades to specific people for their comments, considering what happened.
6. At the end, give a final score (from 0-10) for how interesting this article and its retrospect analysis was.

[PoR note]
Additionally, make your reasoning explicit and structured:
- Highlight where the discussion was internally coherent vs. noisy.
- Mark any strong prediction patterns or phase-locked consensus in the thread.
---

"""


def comments_to_markdown(comments: List[Comment], indent: int = 0) -> str:
    """Convert comment tree to markdown format."""
    lines: List[str] = []
    for comment in comments:
        prefix = "  " * indent
        lines.append(f"{prefix}- **{comment.author}**: {comment.text}")
        if comment.children:
            lines.append(comments_to_markdown(comment.children, indent + 1))
    return "\n\n".join(lines)


def generate_prompt(
    article: Article,
    article_text: str,
    article_error: Optional[str],
    comments: List[Comment],
) -> str:
    lines: List[str] = [
        PROMPT_TEMPLATE,
        f"# {article.title}",
        "",
        "## Article Info",
        "",
        f"- **Original URL**: {article.url}",
        f"- **HN Discussion**: {article.hn_url}",
        f"- **Points**: {article.points}",
        f"- **Submitted by**: {article.author}",
        f"- **Comments**: {article.comment_count}",
        "",
        "## Article Content",
        "",
    ]
    if article_error:
        lines.append(f"*Could not fetch article: {article_error}*")
    else:
        lines.append(article_text)

    lines.extend(["", "## HN Discussion", "", comments_to_markdown(comments)])
    return "\n".join(lines)


# -----------------------------------------------------------------------------
# Stage 2: prompt
# -----------------------------------------------------------------------------

def stage_prompt(target_date: str) -> None:
    data_dir = get_data_dir(target_date)

    for article_dir in sorted(data_dir.iterdir()):
        if not article_dir.is_dir():
            continue

        prompt_file = article_dir / "prompt.md"
        if prompt_file.exists():
            continue

        meta_file = article_dir / "meta.json"
        if not meta_file.exists():
            continue

        with open(meta_file) as f:
            article = Article(**json.load(f))

        article_file = article_dir / "article.txt"
        error_file = article_dir / "article_error.txt"
        if article_file.exists():
            article_text = article_file.read_text()
            article_error = None
        elif error_file.exists():
            article_text = ""
            article_error = error_file.read_text()
        else:
            article_text = ""
            article_error = "Not fetched"

        comments_file = article_dir / "comments.json"
        if comments_file.exists():
            with open(comments_file) as f:
                comments = [Comment.from_dict(c) for c in json.load(f)]
        else:
            comments = []

        prompt = generate_prompt(article, article_text, article_error, comments)
        prompt_file.write_text(prompt, encoding="utf-8")

        print(f"Generated prompt for {article.item_id}: {article.title[:50]}...")

    print(f"\nPrompts generated in {data_dir}")


# -----------------------------------------------------------------------------
# Stage 3: analyze (LLM + PoR)
# -----------------------------------------------------------------------------

def stage_analyze(
    target_date: str,
    model: str = "gpt-5.1",
    max_workers: int = 5,
) -> None:
    """
    - читає prompt.md
    - викликає OpenAI / інший LLM
    - зберігає response.md
    - рахує PoR-метрики по відповіді (через por_core.metrics)
    """
    from concurrent.futures import ThreadPoolExecutor, as_completed
    from dotenv import load_dotenv
    from openai import OpenAI

    load_dotenv()
    client = OpenAI()
    data_dir = get_data_dir(target_date)

    to_analyze = []
    for article_dir in sorted(data_dir.iterdir()):
        if not article_dir.is_dir():
            continue
        prompt_file = article_dir / "prompt.md"
        response_file = article_dir / "response.md"

        if not prompt_file.exists() or response_file.exists():
            continue

        meta_file = article_dir / "meta.json"
        with open(meta_file) as f:
            article = Article(**json.load(f))

        to_analyze.append((article_dir, article, prompt_file.read_text()))

    if not to_analyze:
        print("No articles to analyze.")
        return

    print(f"Analyzing {len(to_analyze)} articles with {max_workers} workers...")

    def analyze_one(item):
        article_dir, article, prompt = item
        response_file = article_dir / "response.md"
        por_file = article_dir / "por.json"

        try:
            response = client.responses.create(
                model=model,
                input=prompt,
                reasoning={"effort": "medium"},
                text={"verbosity": "medium"},
            )
            result = response.output_text
            response_file.write_text(result, encoding="utf-8")

            # PoR-метрики по відповіді (можна поки що мати простий stub в por_core.metrics)
            por_stats = compute_por_for_response(result)
            with open(por_file, "w") as f:
                json.dump(por_stats, f, indent=2)

            return (article.item_id, article.title[:50], len(result), None)
        except Exception as e:
            return (article.item_id, article.title[:50], 0, str(e))

    from concurrent.futures import ThreadPoolExecutor, as_completed

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(analyze_one, item): item for item in to_analyze}
        for future in as_completed(futures):
            item_id, title, chars, error = future.result()
            if error:
                print(f"  {item_id}: {title}... Error: {error}")
            else:
                print(f"  {item_id}: {title}... Done ({chars} chars)")

    print(f"\nAnalysis complete. Results in {data_dir}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="PoR eval stages (prompt + analyze)")
    parser.add_argument("stage", choices=["prompt", "analyze", "all"])
    parser.add_argument("--date", default=None)
    parser.add_argument("--model", default="gpt-5.1")
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args()

    if args.date:
        target_date = args.date
    else:
        today = date.today()
        target_date = today.replace(year=today.year - 10).isoformat()

    print(f"Target date: {target_date}")

    if args.stage in ("prompt", "all"):
        stage_prompt(target_date)
    if args.stage in ("analyze", "all"):
        stage_analyze(target_date, args.model, args.workers)
