"""
por_core/simulator.py

Майбутнє місце для резонансної симуляції між статтями / днями / моделями.
Поки тут лише інтерфейс, щоб не ламати імпорти.
"""

from typing import List, Dict, Any


def simulate_resonance_over_days(day_por_stats: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Приймає список PoR-статистик по днях і повертає агрегат:
    - середній PoR
    - тренд
    - можливо, піки резонансу.
    Зараз — проста середня по overall_por.
    """
    if not day_por_stats:
        return {"mean_overall_por": 0.0, "days": 0}

    overall_vals = [d.get("overall_por", 0.0) for d in day_por_stats]
    mean_val = sum(overall_vals) / len(overall_vals)
    return {
        "mean_overall_por": mean_val,
        "days": len(day_por_stats),
    }
