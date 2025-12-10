import os
import numpy as np
import matplotlib.pyplot as plt

from por_core.simulator import ResonanceSimulator
from por_core.metrics import stability_score, coherence


# -------------------------------------------------------------
#  Ensure output directory exists
# -------------------------------------------------------------
OUTPUT_DIR = os.path.dirname(__file__)
print("Saving images to:", OUTPUT_DIR)


# -------------------------------------------------------------
#  Run Resonance Simulation
# -------------------------------------------------------------
sim = ResonanceSimulator(chain_length=64)
initial_chain = sim.chain.copy()

history = []

for _ in range(200):
    sim.run_iterations(1)
    history.append(sim.chain.copy())

history = np.array(history)  # shape = (200, 64)


# -------------------------------------------------------------
#  Compute metrics
# -------------------------------------------------------------
final_stability = stability_score(sim.chain)
final_coherence = coherence(sim.chain)

print("Final Stability:", final_stability)
print("Final Coherence:", final_coherence)


# -------------------------------------------------------------
#  1. Stabilization Curve
# -------------------------------------------------------------
stability_curve = [stability_score(h) for h in history]

plt.figure(figsize=(8, 4))
plt.plot(stability_curve, linewidth=2)
plt.title("Stability Over Iterations", fontsize=14)
plt.xlabel("Iteration")
plt.ylabel("Stability Score")
plt.grid(True)

plt.savefig(os.path.join(OUTPUT_DIR, "1_stabilization_curve.png"), dpi=200)
plt.close()


# -------------------------------------------------------------
#  2. Coherence Heatmap
# -------------------------------------------------------------
coherence_matrix = np.array([coherence(h) for h in history])

plt.figure(figsize=(8, 4))
plt.imshow(coherence_matrix.reshape(-1, 1), aspect='auto', cmap="viridis")
plt.colorbar(label="Coherence")
plt.title("Coherence Heatmap", fontsize=14)
plt.xlabel("Time")
plt.ylabel("Coherence Level")

plt.savefig(os.path.join(OUTPUT_DIR, "2_coherence_heatmap.png"), dpi=200)
plt.close()


# -------------------------------------------------------------
#  3. Resonance Locking Trajectory (3D)
# -------------------------------------------------------------
from mpl_toolkits.mplot3d import Axes3D  # noqa

fig = plt.figure(figsize=(7, 5))
ax = fig.add_subplot(111, projection="3d")

x = np.arange(64)
y = np.arange(len(history))
X, Y = np.meshgrid(x, y)
Z = history

ax.plot_surface(X, Y, Z, cmap="plasma", linewidth=0, antialiased=True)

ax.set_title("Resonance Locking Trajectory", fontsize=14)
ax.set_xlabel("Chain Position")
ax.set_ylabel("Iteration")
ax.set_zlabel("Value")

plt.savefig(os.path.join(OUTPUT_DIR, "3_resonance_locking.png"), dpi=200)
plt.close()


# -------------------------------------------------------------
#  4. PoR Metrics Over Time
# -------------------------------------------------------------
stability_curve = [stability_score(h) for h in history]
coherence_curve = [coherence(h) for h in history]

plt.figure(figsize=(8, 4))
plt.plot(stability_curve, label="Stability", linewidth=2)
plt.plot(coherence_curve, label="Coherence", linewidth=2)
plt.title("PoR Metrics Over Time", fontsize=14)
plt.xlabel("Iteration")
plt.ylabel("Metric Value")
plt.legend()
plt.grid(True)

plt.savefig(os.path.join(OUTPUT_DIR, "4_por_metrics_over_time.png"), dpi=200)
plt.close()


print("\n✔ All PoR visuals generated successfully!")
print("✔ Files saved in:", OUTPUT_DIR)
