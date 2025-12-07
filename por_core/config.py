# por_core/config.py

class PoRConfig:
    """
    Global parameters for PoR engine.
    """

    def __init__(
        self,
        chain_length: int = 64,
        noise_level: float = 0.03,
        phase_strength: float = 0.15,
    ):
        self.chain_length = chain_length
        self.noise_level = noise_level
        self.phase_strength = phase_strength
