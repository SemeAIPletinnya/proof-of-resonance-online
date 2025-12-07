📘 Proof-of-Resonance (PoR) Framework

A computational engine for stability, coherence, and harmonic alignment in iterative systems.








🌟 Overview

Proof-of-Resonance (PoR) is a novel computational paradigm that does not rely on traditional loss minimization.
Instead, PoR operates through resonance optimization, where iterative systems evolve toward:

low noise

high stability

harmonic phase alignment

The PoR Engine already includes the full computational cycle:

configuration

stability & coherence metrics

harmonic phase-locking

full-chain iterative simulation

PoR is designed for AI research, dynamical systems analysis, climate modeling, experimental ML training loops, and any domain requiring stability-driven optimization.

📦 Installation

PoR will soon be available as a Python package (pip install por-core).
For now, you can install it locally:

git clone https://github.com/SemeAIPletinnya/proof-of-resonance-online
cd proof-of-resonance-online
pip install -r requirements.txt

⚡ Quick Start — Run a Simulation

This example runs a complete PoR simulation using the built-in synthetic chain.

from por_core.simulator import ResonanceSimulator
from por_core.metrics import stability_score, coherence

# Initialize simulator
sim = ResonanceSimulator(chain_length=64)

print("Initial chain sample:", sim.chain[:10], "...")

# Run 200 iterations
sim.run_iterations(200)

print("Final chain sample:", sim.chain[:10], "...")

# Evaluate metrics
print("Stability:", stability_score(sim.chain))
print("Coherence:", coherence(sim.chain))


Output example:

Initial chain sample: [0.91, -1.03, 0.22, ...]
Final chain sample:   [0.11,  0.12, 0.10, ...]
Stability: 0.982
Coherence: 0.913

🧠 Core Architecture

The PoR engine consists of four core modules:

1️⃣ config.py

Defines global parameters and default engine settings.

2️⃣ metrics.py

Implements stability and harmonic coherence metrics.

3️⃣ phase_lock.py

Performs harmonic alignment and phase-locking steps across the chain.

4️⃣ simulator.py

Runs full iterative PoR simulations.

📂 Project Structure
proof-of-resonance-online/
│
├─ por_core/
│   ├─ __init__.py
│   ├─ config.py
│   ├─ metrics.py
│   ├─ phase_lock.py
│   └─ simulator.py
│
├─ examples/
│   ├─ run_synthetic_chain.py
│   └─ climate_chain_demo.md
│
├─ docs/
│   ├─ theory_overview.md
│   └─ roadmap.md
│
├─ README.md
└─ requirements.txt

📘 Examples
▶️ Synthetic Chain Simulation

examples/run_synthetic_chain.py
A complete demonstration using random initial conditions.

🌍 Climate Chain Demo

examples/climate_chain_demo.md
Shows how PoR can model quasi-real environmental signals and long-range dependencies.

📑 Documentation

Full documentation is available in:

docs/theory_overview.md — theoretical foundations

docs/roadmap.md — project roadmap, milestones, and future expansions

🗺️ Roadmap
✅ v0.1 — Core Engine (Completed)

PoR configuration

Stability & coherence metrics

Harmonic phase-locking

Full iterative simulation engine

Examples & docs

🟦 v0.2 — API Expansion (Next)

Public-facing Python API

.fit() / .run() interface

Better visualization

Micro-benchmarking suite

🟥 v0.3 — Domain Integrations

Climate & geophysical modeling

Financial time-series resonance maps

Neural chain stabilization experiments

Multi-agent alignment via PoR metrics

🤝 Contributing

Contributions, suggestions, and experiments using PoR are welcome.
If you build something using resonance optimization — let us know!

📄 License

MIT License © 2025 — SemeAIPletinnya

🚀 Final Notes

PoR is designed as a new computation principle — not a variation of loss-based training, but a stability-first optimization framework.
Its goal is to become a foundational tool for researchers exploring:

emergent dynamics

phase coherence

stability-driven learning

harmonic energy alignment in AI systems
