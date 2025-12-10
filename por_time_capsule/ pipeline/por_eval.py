from por_time_capsule.por_core.metrics import stability_score, coherence_score
from por_time_capsule.por_core.phase_lock import phase_lock_value
from por_time_capsule.por_core.simulator import run_chain

def evaluate_comments(comments):
    """Compute PoR metrics for every comment."""
    results = []

    for c in comments:
        chain = run_chain(c)
        s = stability_score(chain)
        coh = coherence_score(chain)
        pl = phase_lock_value(chain)

        results.append({
            "text": c,
            "stability": s,
            "coherence": coh,
            "phase_lock": pl,
            "por_total": round(0.5*s + 0.3*coh + 0.2*pl, 4)
        })

    # sort from most prescient/insightful
    return sorted(results, key=lambda x: x["por_total"], reverse=True)

