"""
PoR Metrics Module
Contains numerical utilities for evaluating resonance quality,
stability, and coherence across chain states.
"""

import numpy as np


def stability_score(chain):
    """
    Computes the stability score of a resonance chain.
    Stability is defined as 1 − normalized variance.
    """
    if len(chain) == 0:
        return 0.0

    variance = np.var(chain)
    norm_var = variance / (np.mean(chain)**2 + 1e-8)
    return float(max(0.0, 1.0 - norm_var))


def coherence(chain):
    """
    Computes phase coherence of the chain using circular statistics.
    Values close to 1 indicate strong coherence.
    """
    if len(chain) == 0:
        return 0.0

    complex_repr = np.exp(1j * np.array(chain))
    return float(abs(np.mean(complex_repr)))


def composite_metric(chain):
    """
    Combines stability and coherence into a single PoR score.
    """
    s = stability_score(chain)
    c = coherence(chain)
    return float(0.5 * s + 0.5 * c)
