"""
pipeline/render.py

Stage 5: Render
- HTML-дашборд по даті
- Головний index.html
"""

from __future__ import annotations

import json
import html
from pathlib import Path
from typing import List, Dict, Optional

from datetime import date

from .fetch import Article, get_data_dir
from .parse import grade_to_numeric


def get_output_dir(target_date: Optional[str] = None) -> Path:
    base = Path("output")
    if target_date:
        return base / target_date
    return base


def get_all_output_dates() -> List[str]:
    output_base = get_output_dir()
    if not output_base.exists():
        return []
    dates: List[str] = []
    for d in output_base.iterdir():
        if d.is_dir() and (d / "index.html").exists():
            dates.append(d.name)
    return sorted(dates)


def stage_render_day(target_date: str, update_index: bool = True) -> None:
    data_dir = get_data_dir(target_date)
    output_dir = get_output_dir(target_date)
    output_dir.mkdir(parents=True, exist_ok=True)

    frontpage_file = data_dir / "frontpage.json"
    with open(frontpage_file) as f:
        articles = [Article(**a) for a in json.load(f)]

    articles_data = []
    for article in articles:
        article_dir = data_dir / article.item_id

        response_file = article_dir / "response.md"
        response = response_file.read_text() if response_file.exists() else ""

        prompt_file = article_dir / "prompt.md"
        prompt = prompt_file.read_text() if prompt_file.exists() else ""

        score_file = article_dir / "score.json"
        score = None
        if score_file.exists():
            with open(score_file) as f:
                score_data = json.load(f)
                score = score_data.get("interestingness")

        grades_file = article_dir / "grades.json"
        grades: Dict[str, Dict] = {}
        if grades_file.exists():
            with open(grades_file) as f:
                grades = json.load(f)

        articles_data.append(
            {
                "article": article,
                "response": response,
                "prompt": prompt,
                "score": score,
                "grades": grades,
            }
        )

    all_dates = get_all_output_dates()
    if target_date not in all_dates:
        all_dates = sorted(all_dates + [target_date])
    current_idx = all_dates.index(target_date)
    prev_date = all_dates[current_idx - 1] if current_idx > 0 else None
    next_date = all_dates[current_idx + 1] if current_idx < len(all_dates) - 1 else None

    # HTML
    html_parts: List[str] = [
        f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>PoR Time Capsule - {target_date}</title>
    <style>
        * {{ box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
               margin: 0; padding: 0; line-height: 1.6; height: 100vh; overflow: hidden; }}
        .container {{ display: flex; height: 100vh; }}
        .sidebar {{ width: 350px; min-width: 350px; background: #f5f5f5; border-right: 1px solid #ddd;
                   overflow-y: auto; padding: 15px; }}
        .sidebar h1 {{ color: #ff6600; font-size: 1.3em; margin: 0 0 5px 0; }}
        .sidebar h1 a {{ color: #ff6600; text-decoration: none; }}
        .sidebar h2 {{ font-size: 0.95em; color: #666; margin: 0 0 8px 0; font-weight: normal; }}
        .nav {{ display: flex; gap: 10px; margin-bottom: 15px; font-size: 0.85em; }}
        .nav a {{ color: #0066cc; text-decoration: none; }}
        .nav .disabled {{ color: #ccc; }}
        .article-item {{ padding: 10px; margin-bottom: 8px; background: #fff; border-radius: 6px;
                        cursor: pointer; border: 2px solid transparent; display: flex; gap: 10px; }}
        .article-item.selected {{ border-color: #ff6600; background: #fff5f0; }}
        .article-item .score-box {{ width: 36px; height: 36px; border-radius: 6px; display: flex;
                                   align-items: center; justify-content: center; font-weight: bold;
                                   font-size: 0.85em; flex-shrink: 0; }}
        .article-item .score-box.score-none {{ background: #eee; color: #999; font-size: 0.7em; }}
        .article-item .content {{ flex: 1; min-width: 0; }}
        .article-item .title {{ font-size: 0.9em; font-weight: 500; margin-bottom: 4px; color: #333; }}
        .article-item .meta {{ font-size: 0.75em; color: #888; }}

        .score {{ display: inline-block; padding: 2px 6px; border-radius: 10px; font-weight: bold;
                 font-size: 0.7em; margin-left: 6px; vertical-align: middle; background:#ff6600; color:white; }}

        .main {{ flex: 1; overflow-y: auto; padding: 30px 40px; background: #fff; }}
        .main-inner {{ max-width: 800px; }}
        .main h1 {{ margin-top: 0; font-size: 1.5em; }}
        .article-meta {{ color: #666; font-size: 0.9em; margin-bottom: 20px; padding-bottom: 15px;
                        border-bottom: 1px solid #eee; }}
        .article-meta a {{ color: #0066cc; }}

        .analysis {{ font-size: 0.95em; white-space: pre-wrap; }}
        .grades-section {{ background: #f9f9f9; padding: 15px; border-radius: 6px; margin-top: 20px; }}
        .grade {{ display:inline-block; padding:2px 8px; margin:2px; border-radius:3px; font-size:0.8em;
                  background:#e5e7eb; }}

        .prompt-section {{ margin-top:20px; }}
        .prompt-content {{ white-space:pre-wrap; font-size:0.85em; background:#f5f5f5;
                           padding:15px; border-radius:4px; max-height:400px; overflow-y:auto; }}

        .placeholder {{ color:#999; text-align:center; margin-top:100px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="sidebar">
            <h1><a href="../index.html">PoR Time Capsule</a></h1>
            <h2>{target_date} (10 years ago)</h2>
            <div class="nav">
                {f'<a href="../{prev_date}/index.html">&larr; {prev_date}</a>' if prev_date else '<span class="disabled">&larr; prev</span>'}
                <span>|</span>
                {f'<a href="../{next_date}/index.html">{next_date} &rarr;</a>' if next_date else '<span class="disabled">next &rarr;</span>'}
            </div>
"""
    ]

    # sidebar items
    for i, data in enumerate(articles_data):
        article = data["article"]
        score = data["score"]
        if score is not None:
            score_box = f'<div class="score-box"> {score} </div>'
        else:
            score_box = '<div class="score-box score-none">--</div>'

        selected = "selected" if i == 0 else ""
        html_parts.append(
            f"""
            <div class="article-item {selected}" id="article-{article.item_id}" onclick="selectArticle({i})">
                {score_box}
                <div class="content">
                    <div class="title">{article.rank}. {html.escape(article.title)}</div>
                    <div class="meta">{article.points} pts &middot; {article.comment_count} comments</div>
                </div>
            </div>"""
        )

    html_parts.append(
        """
        </div>
        <div class="main">
            <div class="main-inner" id="main-content">
                <div class="placeholder">Select an article from the sidebar</div>
            </div>
        </div>
    </div>

    <script>
    const articles = ["""
    )

    # JS data
    for data in articles_data:
        article: Article = data["article"]
        response = data["response"]
        prompt = data["prompt"]
        grades = data["grades"]
        score = data["score"]

        # simple grades render (name: grade)
        grade_html = ""
        if grades:
            sorted_grades = sorted(
                grades.items(),
                key=lambda x: -{k: grade_to_numeric(k) for k in ["A","B","C","D","F"]}.get(x[1].get("grade","A")[0], 0),
            )
            for username, info in sorted_grades[:20]:
                grade_html += f'<span class="grade">{html.escape(username)}: {info["grade"]}</span> '

        title_js = json.dumps(article.title)
        url_js = json.dumps(article.url)
        hn_url_js = json.dumps(article.hn_url)
        resp_js = json.dumps(response)
        prompt_js = json.dumps(prompt)
        grade_html_js = json.dumps(grade_html)

        html_parts.append(
            f"""
        {{
            id: "{article.item_id}",
            title: {title_js},
            url: {url_js},
            hn_url: {hn_url_js},
            points: {article.points},
            comments: {article.comment_count},
            score: {json.dumps(score)},
            response: {resp_js},
            prompt: {prompt_js},
            grades: {grade_html_js}
        }},"""
        )

    html_parts.append(
        """
    ];

    function selectArticle(idx) {
        document.querySelectorAll('.article-item').forEach((el, i) => {
            el.classList.toggle('selected', i === idx);
        });

        const a = articles[idx];
        const scoreHtml = a.score !== null ? `<span class="score">${a.score}/10</span>` : '';

        document.getElementById('main-content').innerHTML = `
            <h1>${a.title}${scoreHtml}</h1>
            <div class="article-meta">
                ${a.points} points &middot; ${a.comments} comments &middot;
                <a href="${a.url}" target="_blank">Original</a> &middot;
                <a href="${a.hn_url}" target="_blank">HN</a>
            </div>
            ${a.grades ? `<div class="grades-section"><strong>Grades:</strong> ${a.grades}</div>` : ''}
            <div class="analysis">${a.response ? a.response.replace(/</g, '&lt;') : '<em>No analysis</em>'}</div>
            ${a.prompt ? `<details class="prompt-section"><summary>View prompt</summary><div class="prompt-content">${a.prompt.replace(/</g, '&lt;')}</div></details>` : ''}
        `;
    }

    if (articles.length > 0) {
        selectArticle(0);
    }
    </script>
</body>
</html>"""
    )

    output_file = output_dir / "index.html"
    output_file.write_text("\n".join(html_parts), encoding="utf-8")
    print(f"Rendered HTML to {output_file}")

    if update_index:
        stage_render_index()


def stage_render_index() -> None:
    output_base = get_output_dir()
    output_base.mkdir(parents=True, exist_ok=True)

    data_base = Path("data")
    all_dates: List[str] = []
    if data_base.exists():
        for d in data_base.iterdir():
            if d.is_dir() and (d / "frontpage.json").exists():
                all_dates.append(d.name)
    all_dates = sorted(all_dates)

    if not all_dates:
        print("No dates to index.")
        return

    for d in all_dates:
        stage_render_day(d, update_index=False)

    html_index = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>PoR Time Capsule</title>
    <style>
        body { font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
               max-width:800px; margin:0 auto; padding:40px 20px; line-height:1.6; }
        h1 { color:#ff6600; }
        .intro { color:#666; margin-bottom:30px; }
        .date-list { list-style:none; padding:0; }
        .date-list li { margin-bottom:10px; }
        .date-list a { display:block; padding:12px 18px; background:#f5f5f5; border-radius:6px;
                       text-decoration:none; color:#333; }
        .date-list a:hover { background:#ff6600; color:white; }
        .date { font-weight:500; }
        .desc { font-size:0.85em; color:#888; margin-top:3px; }
    </style>
</head>
<body>
    <h1>PoR Time Capsule</h1>
    <p class="intro">
        PoR Time Capsule: LLM + Proof-of-Resonance retrospective on Hacker News frontpages 10 years ago.
    </p>
    <ul class="date-list">
"""

    for d in reversed(all_dates):
        html_index += f"""        <li>
            <a href="{d}/index.html">
                <div class="date">{d}</div>
                <div class="desc">10 years ago today</div>
            </a>
        </li>
"""

    html_index += """    </ul>
</body>
</html>"""

    output_index = output_base / "index.html"
    output_index.write_text(html_index, encoding="utf-8")
    print(f"Rendered index to {output_index} ({len(all_dates)} dates)")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Render PoR Time Capsule")
    parser.add_argument("stage", choices=["day", "index", "all"])
    parser.add_argument("--date", default=None)
    args = parser.parse_args()

    if args.stage in ("day", "all"):
        if args.date:
            target_date = args.date
        else:
            today = date.today()
            target_date = today.replace(year=today.year - 10).isoformat()
        print(f"Target date: {target_date}")
        stage_render_day(target_date)
    if args.stage in ("index", "all"):
        stage_render_index()
