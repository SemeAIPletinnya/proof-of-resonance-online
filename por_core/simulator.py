# por_core/simulator.py

import numpy as np
from .config import PoRConfig
from .metrics import stability_score, coherence
from .phase_lock import phase_lock

class ResonanceSimulator:
    """
    Full PoR engine:
      - initializes chain
      - performs iterative simulation
      - applies noise + phase alignment
      - tracks stability & coherence over time
    """

    def __init__(self, chain_length: int = 64):
        self.config = PoRConfig(chain_length=chain_length)
        self.chain = np.random.uniform(-1, 1, chain_length)

    def step(self):
        """Single simulation step."""
        # noise injection
        noise = np.random.normal(0, self.config.noise_level, len(self.chain))
        self.chain += noise

        # phase alignment
        self.chain = phase_lock(self.chain, self.config.phase_strength)

    def run_iterations(self, steps: int = 200):
        """Run simulation for N steps."""
        for _ in range(steps):
            self.step()

    def metrics(self):
        """Return stability & coherence."""
        return {
            "stability": stability_score(self.chain),
            "coherence": coherence(self.chain),
        }
