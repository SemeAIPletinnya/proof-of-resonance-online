# por_core/metrics.py

import numpy as np

def stability_score(chain: np.ndarray) -> float:
    """
    Stability = 1 - variance of differences.
    High stability → low fluctuation between steps.
    """
    diffs = np.diff(chain)
    variance = np.var(diffs)
    return float(max(0.0, 1.0 - variance))

def coherence(chain: np.ndarray) -> float:
    """
    Coherence = normalized autocorrelation strength.
    Measures harmonic alignment across the chain.
    """
    chain = chain - np.mean(chain)
    autocorr = np.correlate(chain, chain, mode="full")
    mid = len(autocorr) // 2
    norm = autocorr[mid] if autocorr[mid] != 0 else 1e-6
    return float(abs(autocorr[mid + 1] / norm))
