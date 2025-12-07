# Climate Chain Demo — Applying PoR to Quasi-Real Earth Data 🌍

This example demonstrates how the Proof-of-Resonance (PoR) engine  
can be applied to quasi-real climate-like time-series data.

The goal is to show how resonance metrics (stability and coherence)  
behave on slowly drifting, noisy environmental signals.

---

## 📌 Data Description

We generate a synthetic “climate trend” composed of:
- a slow sinusoidal drift (temperature-like)
- small seasonal fluctuations
- additive Gaussian noise

This signal mimics real climate station recordings:
long-range dependency, local noise, periodic structure.

---

## 📌 Code Example

```python
import numpy as np
from por_core.simulator import ResonanceSimulator
from por_core.metrics import stability_score, coherence

# Generate quasi-real climate-style data
t = np.linspace(0, 50, 512)
trend = 0.3 * np.sin(0.2 * t)
season = 0.1 * np.sin(2 * t)
noise = 0.05 * np.random.randn(len(t))

signal = trend + season + noise

# Initialize PoR engine
sim = ResonanceSimulator(chain_length=len(signal))

# Inject the climate signal
sim.chain = np.array(signal)

print("Initial Stability:", stability_score(sim.chain))
print("Initial Coherence:", coherence(sim.chain))

# Run PoR adjustment steps
sim.run_iterations(300)

print("Final Stability:", stability_score(sim.chain))
print("Final Coherence:", coherence(sim.chain))
