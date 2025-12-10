import numpy as np

def phase_lock_value(chain):
    """Phase-lock index (0..1) similar to Kuramoto order parameter."""
    phases = np.exp(1j * np.array(chain))
    R = np.abs(np.mean(phases))
    return float(R)  # 1 = perfect coherence

