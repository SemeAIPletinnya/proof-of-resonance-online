# 🔷 Proof-of-Resonance (PoR) Framework
*A computational engine for stability, coherence, and harmonic alignment in iterative systems.*

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Resonance Score](https://img.shields.io/badge/PoR-Core_Stability-Verified-purple.svg)
![Status](https://img.shields.io/badge/Status-Stable-brightgreen.svg)

---

## 🌟 Overview

**Proof-of-Resonance (PoR)** is a novel computational paradigm that does **not** rely on classical loss minimization.  
Instead, PoR applies **resonance optimization**, where iterative systems evolve toward:

- low noise  
- high stability  
- harmonic phase alignment  

The PoR Engine includes the full computational cycle:

- configuration  
- stability & coherence metrics  
- harmonic phase-locking  
- full-chain iterative simulation  

PoR is designed for:

- AI research  
- dynamical systems modeling  
- climate & geophysical simulations  
- ML training stability  
- multi-agent coherence analysis  

---

## 📦 Installation

PoR will soon be available as a Python package (`pip install por-core`).  
For now, install locally:

```bash
git clone https://github.com/SemeAIPletinnya/proof-of-resonance-online
cd proof-of-resonance-online
pip install -r requirements.txt
from por_core.simulator import ResonanceSimulator
from por_core.metrics import stability_score, coherence

sim = ResonanceSimulator(chain_length=64)

print("Initial chain sample:", sim.chain[:10], "...")

sim.run_iterations(200)

print("Final chain sample:", sim.chain[:10], "...")
print("Stability:", stability_score(sim.chain))
print("Coherence:", coherence(sim.chain))
Initial chain sample: [0.91, -1.03, 0.22, ...]
Final chain sample:   [0.11, 0.12, 0.10, ...]
Stability: 0.982  
Coherence: 0.913
examples/run_synthetic_chain.py
examples/climate_chain_demo.md
