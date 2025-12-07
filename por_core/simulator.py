"""
PoR Simulation Engine
Handles long-chain iterative resonance simulations using the core modules.
"""

import numpy as np
from .config import get_config
from .metrics import stability_score, coherence
from .phase_lock import phase_lock_step


class ResonanceSimulator:
    """
    Main engine for running Proof-of-Resonance simulations.
    """

    def __init__(self, chain_length=None, config=None):
        self.config = config or get_config()
        self.chain_length = chain_length or self.config["chain_length"]

        # Initialize random phases
        self.chain = np.random.uniform(-np.pi, np.pi, size=self.chain_length)

        self.history = []

    def step(self):
        """
        Performs one resonance update step using the phase-locking function.
        """
        self.chain = phase_lock_step(
            self.chain,
            tolerance=self.config["phase_lock_tolerance"]
        )

        self.history.append(self.chain.copy())

    def run(self, steps=50):
        """
        Run full simulation for N steps.
        Returns stability, coherence, and chain history.
        """
        for _ in range(steps):
            self.step()

        stab = stability_score(self.chain)
        coh = coherence(self.chain)

        return {
            "final_chain": self.chain,
            "stability": stab,
            "coherence": coh,
            "history": np.array(self.history),
        }


def run_default_simulation(steps=50):
    """
    Convenience wrapper for quick tests.
    """
    sim = ResonanceSimulator()
    return sim.run(steps)
