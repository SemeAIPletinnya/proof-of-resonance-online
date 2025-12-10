# 🔷 Proof-of-Resonance (PoR) Framework  
*A computational engine for stability, coherence, and harmonic alignment in iterative systems.*

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![PoR Stability](https://img.shields.io/badge/PoR-Stability_Validated-purple.svg)
![Status](https://img.shields.io/badge/Status-Stable-brightgreen.svg)

---

# 🌟 Overview

**Proof-of-Resonance (PoR)** is a computational paradigm that replaces classical loss minimization with  
**resonance optimization** — a process where systems evolve toward:

- low noise  
- high stability  
- harmonic phase alignment  

PoR provides a complete engine for:

- stability metrics  
- coherence / Δφ metrics  
- harmonic phase-locking  
- iterative full-chain simulations  
- multimodal resonance (v0.2)

PoR is built for:

- AI research & model alignment  
- dynamical systems simulations  
- chain-of-thought stabilization  
- multimodal embedding harmonization  
- multi-agent coherence analysis  

---

# 🚀 Version Roadmap

## **v0.1 — Core Engine (Completed)**

- `por_core/config.py` — global defaults  
- `por_core/metrics.py` — stability & coherence metrics  
- `por_core/phase_lock.py` — harmonic phase-locking  
- `por_core/simulator.py` — iterative resonance simulator  
- Basic examples + docs  

This version establishes PoR as a theoretical and computational foundation.

---

## **v0.2 — Multimodal PoR (NEW)**

The new module introduces a **PoR resonance layer for image–text embeddings**, enabling:

### ✔ Shared Phase-Space Mapping  
CLIP embeddings (image/text) are projected into a unified phase space.

### ✔ Iterative Resonance Updates  
Embeddings are harmonized through PoR dynamics until they converge to a stable attractor.

### ✔ Cross-Modal Stability  
PoR reduces noise in mismatched image–text pairs and amplifies semantic alignment.

### New components:

### Example usage

```python
from por_multimodal.resonance_mm import MultimodalResonator
from por_multimodal.clip_loader import load_text_emb, load_image_emb

img = load_image_emb("tests/cat.png")
txt = load_text_emb("a small animal")

res = MultimodalResonator(img, txt)
res.run(iterations=120)

print("Final coherence:", res.coherence())
benchmarks/
├── configs/
├── datasets/
└── runners/
python benchmarks/runners/run_solo.py \
  --config benchmarks/configs/reasoning_v1.yaml \
  --model gpt-4.1 \
  --out solo_results.jsonl
python benchmarks/runners/run_resonance_two_model.py \
  --config benchmarks/configs/creative_v1.yaml \
  --pair "gpt-4.1,gpt-4.1-mini" \
  --out resonance_results.jsonl
python benchmarks/runners/run_resonance_two_model.py \
  --config benchmarks/configs/creative_v1.yaml \
  --pair "gpt-4.1,gpt-4.1-mini" \
  --out resonance_results.jsonl
python benchmarks/runners/evaluate_por_score.py \
  --solo solo_results.jsonl \
  --res resonance_results.jsonl \
  --config benchmarks/configs/memory_v1.yaml \
  --out por_score.json
Solo Stability:     0.982
Solo Coherence:     0.913
Δφ Drift:           0.021

Multi Stability:    0.991
Multi Coherence:    0.944

PoR Gain:           +0.032
git clone https://github.com/SemeAIPletinnya/proof-of-resonance-online
cd proof-of-resonance-online
pip install -r requirements.txt
from por_core.simulator import ResonanceSimulator
from por_core.metrics import stability_score, coherence

sim = ResonanceSimulator(chain_length=64)
sim.run_iterations(200)

print("Stability:", stability_score(sim.chain))
print("Coherence:", coherence(sim.chain))
proof-of-resonance-online/
│
├── por_core/
│── por_multimodal/
├── benchmarks/
├── docs/
├── examples/
└── README.md


