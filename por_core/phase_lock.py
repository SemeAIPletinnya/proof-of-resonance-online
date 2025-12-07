# por_core/phase_lock.py

import numpy as np

def phase_lock(chain: np.ndarray, strength: float) -> np.ndarray:
    """
    Performs harmonic phase alignment.
    Moves values slightly toward local harmonic mean.
    """
    new_chain = chain.copy()
    for i in range(1, len(chain) - 1):
        local_mean = (chain[i - 1] + chain[i] + chain[i + 1]) / 3
        new_chain[i] = chain[i] + strength * (local_mean - chain[i])
    return new_chain
