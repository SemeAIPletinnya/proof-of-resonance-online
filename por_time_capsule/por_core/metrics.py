import numpy as np

def stability_score(chain):
    """Stability = inverse drift across chain."""
    diffs = np.abs(np.diff(chain))
    drift = np.mean(diffs)
    return float(np.exp(-drift))  # 0..1


def coherence_score(chain):
    """Coherence = similarity of chain to its mean phase."""
    mean_phase = np.mean(chain)
    return float(1 / (1 + np.std(chain - mean_phase)))


def normalize(v):
    return float(np.clip(v, 0.0, 1.0))

