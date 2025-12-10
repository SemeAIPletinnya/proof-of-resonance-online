import numpy as np
from por_multimodal.clip_loader import CLIPLoader
from por_multimodal.resonance_mm import MultimodalResonance
import matplotlib.pyplot as plt

clip_model = CLIPLoader()
resonator = MultimodalResonance(alpha=0.08, steps=120)

# 1 — matched
img1 = clip_model.embed_image("data/dog.png")
txt1 = clip_model.embed_text("a dog running in a field")

# 2 — mismatched
img2 = clip_model.embed_image("data/car.png")
txt2 = clip_model.embed_text("a small kitten on a pillow")

_, _, hist_matched = resonator.resonate(img1, txt1)
_, _, hist_mismatch = resonator.resonate(img2, txt2)

plt.figure(figsize=(8,5))
plt.plot(hist_matched, label="Matched pair")
plt.plot(hist_mismatch, label="Mismatched pair")
plt.title("Multimodal PoR — Convergence of Embeddings")
plt.xlabel("Iteration")
plt.ylabel("Distance img–txt")
plt.legend()
plt.grid(True)
plt.savefig("docs/visuals/mm_convergence_curve.png", dpi=300)
plt.close()
