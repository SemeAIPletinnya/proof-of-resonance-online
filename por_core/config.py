"""
PoR Engine Configuration
Defines global parameters and defaults for the Proof-of-Resonance system.
"""

DEFAULT_SETTINGS = {
    "sampling_rate": 128,
    "chain_length": 64,
    "stability_threshold": 0.92,
    "phase_lock_tolerance": 0.015,
}

def get_config():
    """Return a copy of the default PoR configuration."""
    return DEFAULT_SETTINGS.copy()
