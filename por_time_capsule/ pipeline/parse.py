"""
pipeline/parse.py

Stage 4: Parse
- Парсимо Final grades + interestingness score з response.md
- Зберігаємо по статті + агрегуємо по користувачам
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, Optional, List

from datetime import date

from .fetch import get_data_dir


def parse_grades(text: str) -> Dict[str, Dict[str, str]]:
    """
    Parse the Final grades section from LLM output.

    Returns: username -> {"grade": "A", "rationale": "..."}
    """
    grades: Dict[str, Dict[str, str]] = {}

    pattern = r"(?:^|\n)(?:\d+[\.\)]\s*)?(?:#+ *)?Final grades\s*\n"
    match = re.search(pattern, text, re.IGNORECASE)
    if not match:
        return grades

    grades_section = text[match.end() :]
    line_pattern = r'^[\-\*]\s*([^:]+):\s*([A-F][+\-−]?)(?:\s*\(([^)]+)\))?'

    for line in grades_section.split("\n"):
        line = line.strip()
        if not line:
            continue
        if line.startswith("#") or line.startswith("["):
            break
        m = re.match(line_pattern, line)
        if m:
            username = m.group(1).strip()
            grade = m.group(2).strip()
            rationale = m.group(3).strip() if m.group(3) else ""
            grades[username] = {"grade": grade, "rationale": rationale}

    return grades


def grade_to_numeric(grade: str) -> float:
    base = {"A": 4.0, "B": 3.0, "C": 2.0, "D": 1.0, "F": 0.0}
    if not grade:
        return 0.0
    value = base.get(grade[0].upper(), 0.0)
    if len(grade) > 1:
        if grade[1] == "+":
            value += 0.3
        elif grade[1] in "-−":
            value -= 0.3
    return value


def parse_interestingness_score(text: str) -> Optional[int]:
    pattern = r"Article hindsight analysis interestingness score:\s*(\d+)"
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        score = int(match.group(1))
        return max(0, min(10, score))
    return None


def stage_parse(target_date: str) -> None:
    data_dir = get_data_dir(target_date)
    all_grades: Dict[str, List[Dict[str, str]]] = {}

    for article_dir in sorted(data_dir.iterdir()):
        if not article_dir.is_dir():
            continue

        response_file = article_dir / "response.md"
        if not response_file.exists():
            continue

        grades_file = article_dir / "grades.json"
        score_file = article_dir / "score.json"

        response = response_file.read_text(encoding="utf-8")
        grades = parse_grades(response)
        score = parse_interestingness_score(response)

        with open(grades_file, "w") as f:
            json.dump(grades, f, indent=2)

        with open(score_file, "w") as f:
            json.dump({"interestingness": score}, f, indent=2)

        item_id = article_dir.name
        for username, grade_info in grades.items():
            if username not in all_grades:
                all_grades[username] = []
            all_grades[username].append(
                {
                    "grade": grade_info["grade"],
                    "rationale": grade_info["rationale"],
                    "article": item_id,
                }
            )

        score_str = f", score={score}" if score is not None else ""
        print(f"Parsed {len(grades)} grades from {item_id}{score_str}")

    agg_file = data_dir / "all_grades.json"
    with open(agg_file, "w") as f:
        json.dump(all_grades, f, indent=2)

    print(f"\nParsed grades saved to {agg_file}")

    if all_grades:
        print("\n--- Grade Summary ---")
        user_gpas = []
        for username, grades_list in all_grades.items():
            gpas = [grade_to_numeric(g["grade"]) for g in grades_list]
            avg_gpa = sum(gpas) / len(gpas)
            user_gpas.append((username, avg_gpa, len(grades_list)))

        user_gpas.sort(key=lambda x: x[1], reverse=True)
        for username, gpa, count in user_gpas[:10]:
            print(f"  {username}: {gpa:.2f} ({count} articles)")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Parse grades & scores")
    parser.add_argument("--date", default=None)
    args = parser.parse_args()

    if args.date:
        target_date = args.date
    else:
        today = date.today()
        target_date = today.replace(year=today.year - 10).isoformat()

    print(f"Target date: {target_date}")
    stage_parse(target_date)
