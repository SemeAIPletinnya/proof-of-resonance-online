"""
por_core/phase_lock.py

"""

from typing import List, Dict


def estimate_phase_lock_from_grades(grades: List[Dict[str, str]]) -> float:
    """
    Дуже проста штука:
    - якщо більшість оцінок A/B -> phase-lock високий
    - якщо багато F/D -> низький
    """
    if not grades:
        return 0.0

    score_map = {"A": 1.0, "B": 0.8, "C": 0.5, "D": 0.2, "F": 0.0}
    vals = []
    for g in grades:
        letter = g.get("grade", "C")[0].upper()
        vals.append(score_map.get(letter, 0.5))
    return sum(vals) / len(vals)
