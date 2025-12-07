"""
Phase-Locking Module
Implements functions for phase adjustment and resonance-lock simulation.
"""

import numpy as np


def normalize_phase(x):
    """
    Normalize a phase value into the range [-π, π].
    """
    return float((x + np.pi) % (2 * np.pi) - np.pi)


def phase_difference(a, b):
    """
    Compute the signed difference between two phases.
    """
    return normalize_phase(a - b)


def phase_lock_step(chain, tolerance=0.02):
    """
    Performs one iteration of a phase-lock adjustment step.
    Elements try to align with the mean phase.
    """
    if len(chain) == 0:
        return chain

    mean_phase = np.angle(np.mean(np.exp(1j * np.array(chain))))

    new_chain = []
    for x in chain:
        diff = phase_difference(x, mean_phase)

        # If difference is small enough → lock
        if abs(diff) < tolerance:
            new_chain.append(mean_phase)
        else:
            # Partial adjustment toward mean phase
            new_chain.append(x - diff * 0.5)

    return np.array(new_chain)
