"""
Synthetic Resonance Chain Demo
Runs a full Proof-of-Resonance simulation using synthetic data.
"""

from por_core.simulator import ResonanceSimulator
from por_core.metrics import stability_score, coherence

# Initialize simulator
sim = ResonanceSimulator(chain_length=64)

print("Initial random chain:")
print(sim.chain[:10], "...")

# Run several resonance iterations
sim.run(iterations=200)

print("\nFinal chain sample:")
print(sim.chain[:10], "...")

# Evaluate metrics
stab = stability_score(sim.chain)
coh = coherence(sim.chain)

print("\n=== Resonance Metrics ===")
print(f"Stability score: {stab:.4f}")
print(f"Coherence:       {coh:.4f}")
print("========================")
