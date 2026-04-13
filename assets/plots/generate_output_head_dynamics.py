"""
Generate output_head_dynamics.svg for the output-head-dynamics findings page.

Data source: three runs from EXPERIMENT_LOG.md that share the Matrix Thinker
backbone but vary in output mechanism. The runs are not FLOPs-matched; they
differ in training corpus, step count, and (for the 3D matrix-product run)
attention mechanism. See the paper for caveats.

  - Run 12, Round 2 MultiProbeHead: val-time per-iteration effective rank from
    the step-3000 *BEST* eval checkpoint (round2_full_train.log line 125).
    Measured values at every iteration.
    [5.05, 5.45, 5.71, 5.86, 5.99, 6.06, 6.11, 6.13]. T=8 BPB 1.670.
  - Run 10, Frobenius attention + vector-collapse output head: reported as
    solidification (falling) during iterative refinement. No per-iteration
    numbers were logged for this run. Drawn as a two-point line from an
    illustrative higher starting point down to an illustrative lower end —
    direction only, no intermediate markers.
  - Run 21, 3D matrix-product attention: endpoints 2.75 -> 2.66 are reported
    in EXPERIMENT_LOG.md. Intermediate points were never measured. Drawn as a
    two-point line with markers only at the endpoints.

The MultiProbeHead series keeps its per-iteration markers because every
value is real. The two control series are drawn as straight two-point lines
so the plot does not visually imply intermediate measurements that do not
exist.

Output: SVG at pebble-ai-site/assets/plots/output_head_dynamics.svg
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

# Brand palette
BG = "#FAF5E7"
TEXT = "#1a1a1a"
ACCENT = "#8B2E1F"
ACCENT_SOFT = "#c4826b"
MUTED = "#5a5a5a"

iterations = list(range(1, 9))

# Measured Round 2 MultiProbeHead val-time rank trajectory.
# Source: experiment-runs/8xh100-session1/round2_full_train.log line 125
# ("T= 8: PPL 72.4 | Rank [5.05, 5.45, 5.71, 5.86, 5.99, 6.06, 6.11, 6.13] *BEST*")
# This is the final step-3000 BEST eval checkpoint, val-time per-iteration
# rank at T=8, averaged over 512 held-out positions.
multiprobe = [5.05, 5.45, 5.71, 5.86, 5.99, 6.06, 6.11, 6.13]

# Vector-collapse head: no per-iteration numbers were logged for this run.
# Draw a two-point direction line from an illustrative start to an illustrative
# end, with markers ONLY at the endpoints. The absolute height is illustrative;
# the axis is shared with the other series to make the direction reversal
# legible but NOT to imply a matched comparison.
vector_collapse_x = [iterations[0], iterations[-1]]
vector_collapse_y = [4.80, 4.07]  # illustrative endpoints, direction only

# 3D matrix-product attention endpoints: measured in Run 21 (2.75 -> 2.66).
# Intermediate points were not measured. Draw as a two-point line with
# markers only at the endpoints.
matprod_3d_x = [iterations[0], iterations[-1]]
matprod_3d_y = [2.75, 2.66]

plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["text.color"] = TEXT
plt.rcParams["axes.labelcolor"] = TEXT
plt.rcParams["xtick.color"] = TEXT
plt.rcParams["ytick.color"] = TEXT
plt.rcParams["axes.edgecolor"] = TEXT

fig, ax = plt.subplots(figsize=(7.2, 4.6), facecolor=BG)
ax.set_facecolor(BG)

# MultiProbeHead (measured at every iteration — primary series, solid line
# with per-iteration circle markers)
ax.plot(iterations, multiprobe,
        color=ACCENT, linewidth=2.5, marker="o", markersize=6,
        label="MultiProbeHead (Run 12, val-time, measured)", zorder=3)
for x, y in zip(iterations, multiprobe):
    ax.annotate(f"{y:.2f}", (x, y), textcoords="offset points",
                xytext=(6, 6), fontsize=8, color=ACCENT, fontweight="bold")

# Vector-collapse head: two-point dashed line, markers only at endpoints
ax.plot(vector_collapse_x, vector_collapse_y,
        color=ACCENT_SOFT, linewidth=1.8, marker="s", markersize=6,
        linestyle="--",
        label="Vector-collapse (Run 10, direction only, illustrative)",
        zorder=2)

# 3D matrix-product attention: two-point dotted line, markers only at endpoints
ax.plot(matprod_3d_x, matprod_3d_y,
        color=MUTED, linewidth=1.5, marker="^", markersize=6,
        linestyle=":",
        label="3D matrix-product (Run 21, endpoints measured)",
        zorder=1)

# Annotate the 3D matrix-product endpoints (real numbers)
ax.annotate("2.75", (matprod_3d_x[0], matprod_3d_y[0]),
            textcoords="offset points", xytext=(-22, -4),
            fontsize=8, color=MUTED)
ax.annotate("2.66", (matprod_3d_x[1], matprod_3d_y[1]),
            textcoords="offset points", xytext=(8, -4),
            fontsize=8, color=MUTED)

ax.set_xlabel("refinement iteration", fontsize=10, labelpad=8)
ax.set_ylabel("effective rank", fontsize=10, labelpad=8)
ax.set_xlim(0.5, 8.5)
ax.set_ylim(2.0, 6.8)
ax.xaxis.set_major_locator(MultipleLocator(1))
ax.yaxis.set_major_locator(MultipleLocator(1))
ax.grid(True, linestyle="-", linewidth=0.5, alpha=0.25, color=TEXT)

for spine in ax.spines.values():
    spine.set_linewidth(1.0)
    spine.set_color(TEXT)

legend = ax.legend(loc="center right", frameon=True, fontsize=8.0,
                   facecolor=BG, edgecolor=TEXT)
legend.get_frame().set_linewidth(1.0)

ax.set_title("rank trajectory under three output mechanisms", fontsize=11,
             color=TEXT, fontweight="bold", pad=14, loc="left")

plt.tight_layout()

out = "/Users/samuellarson/Experiments/learned-representations/pebble-ai-site/assets/plots/output_head_dynamics.svg"
plt.savefig(out, format="svg", facecolor=BG, bbox_inches="tight")
print(f"wrote {out}")
