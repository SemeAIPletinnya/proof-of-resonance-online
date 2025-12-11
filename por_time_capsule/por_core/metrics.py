"""
por_core/metrics.py


"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, Any, List


@dataclass
class PoRStats:
    coherence_score: float   
    prediction_density: float  
    phase_lock_index: float  
    overall_por: float      


def _clip(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


def compute_por_for_response(text: str) -> Dict[str, Any]:
    """
    Дуже проста евристика, щоб поки щось рахувалось:

    - coherence_score: 1 / (1 + кількість "however"/"but" як маркерів суперечностей)
    - prediction_density: кількість слів типу "will", "won't", "likely" / загальна довжина
    - phase_lock_index: умовно = середнє по двом попереднім
    - overall_por: середнє трьох
    """
    lowered = text.lower()
    length = max(len(lowered.split()), 1)

    contradictions = sum(lowered.count(k) for k in ["however", "but", "on the other hand"])
    coherence = 1.0 / (1.0 + contradictions)

    prediction_tokens = ["will", "likely", "unlikely", "won't", "going to"]
    pred_count = sum(lowered.count(k) for k in prediction_tokens)
    prediction_density = pred_count / length

    phase_lock = (coherence + prediction_density) / 2.0

    overall = (coherence + prediction_density + phase_lock) / 3.0

    stats = PoRStats(
        coherence_score=_clip(coherence),
        prediction_density=_clip(prediction_density * 10),  # трохи масштабнемо
        phase_lock_index=_clip(phase_lock),
        overall_por=_clip(overall),
    )
    return asdict(stats)
