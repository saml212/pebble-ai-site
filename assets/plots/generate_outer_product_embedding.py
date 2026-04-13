"""
Generate outer_product_embedding.svg for the outer-product embedding finding.

Shows T=1 BPB (byte-per-byte loss) for matrix outer-product embedding vs
flat-vector baselines across three comparisons:

  - Run 22 (param-matched ablation, HEADLINE): Matrix d=16 2.55M params vs
    flat-vector d_model=256 5.66M params. Same pipeline, flat has 2.2x MORE
    params and still loses at T=1. Matrix T=1 BPB 2.117, Flat T=1 BPB 2.872.
  - Round 2 (Run 12 vs Run 13): Matrix Thinker d=32 vs tokens-matched LoopFormer
    baseline on 2.19B-token reasoning corpus at ~5.15M-5.33M params.
    Matrix T=1 BPB 2.12, LoopFormer T=1 BPB 4.29.
  - Run 18 (param-asymmetric ablation, FLAGGED): Matrix d=16 2.4M params vs
    flat 24M params (10x more). Matrix T=1 BPB 2.18, Flat T=1 BPB 3.219.
    Baseline has 10x more params; shown hatched to mark the asymmetry.

Output: SVG at pebble-ai-site/assets/plots/outer_product_embedding.svg
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
CODE_BG = "#f0e9d3"

# Comparisons: (label, matrix_bpb, baseline_bpb, matrix_params_M, baseline_params_M, note, asymmetric)
# Run 22 leads because it is the strongest clean signal: flat has 2.2x more
# params than matrix and still loses T=1.
comparisons = [
    ("Run 22\nparam-matched*", 2.117, 2.872, 2.55, 5.66, "flat has 2.2x more params", False),
    ("Round 2\n(Run 12 vs 13)", 2.12, 4.29, 5.15, 5.33, "tokens-matched", False),
    ("Run 18\nasymmetric", 2.18, 3.219, 2.4, 24.0, "flat has 10x more params", True),
]

plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["text.color"] = TEXT
plt.rcParams["axes.labelcolor"] = TEXT
plt.rcParams["xtick.color"] = TEXT
plt.rcParams["ytick.color"] = TEXT
plt.rcParams["axes.edgecolor"] = TEXT

fig, ax = plt.subplots(figsize=(7.6, 5.0), facecolor=BG)
ax.set_facecolor(BG)

n = len(comparisons)
bar_width = 0.36
x_positions = list(range(n))
matrix_x = [x - bar_width/2 for x in x_positions]
baseline_x = [x + bar_width/2 for x in x_positions]

matrix_bpbs = [c[1] for c in comparisons]
baseline_bpbs = [c[2] for c in comparisons]

# Matrix bars (brand red)
bars_m = ax.bar(matrix_x, matrix_bpbs, bar_width,
                color=ACCENT, edgecolor=TEXT, linewidth=1.0,
                label="matrix (outer-product embedding)", zorder=3)

# Baseline bars (soft/muted). Run 18 baseline is hatched to mark param asymmetry.
baseline_colors = [ACCENT_SOFT for _ in comparisons]
hatches = ["", "", "///"]
bars_b = ax.bar(baseline_x, baseline_bpbs, bar_width,
                color=baseline_colors, edgecolor=TEXT, linewidth=1.0,
                hatch=hatches,
                label="flat-vector baseline", zorder=3)

# Annotate each bar with BPB value
for bar, val in zip(bars_m, matrix_bpbs):
    ax.annotate(f"{val:.2f}", (bar.get_x() + bar.get_width()/2, val),
                textcoords="offset points", xytext=(0, 4),
                ha="center", fontsize=9, color=ACCENT, fontweight="bold")

for bar, val in zip(bars_b, baseline_bpbs):
    ax.annotate(f"{val:.2f}", (bar.get_x() + bar.get_width()/2, val),
                textcoords="offset points", xytext=(0, 4),
                ha="center", fontsize=9, color=MUTED, fontweight="bold")

# Annotate param counts below the x-axis
for i, c in enumerate(comparisons):
    m_params = c[3]
    b_params = c[4]
    ax.annotate(f"{m_params:.2f}M", (matrix_x[i], 0),
                textcoords="offset points", xytext=(0, -18),
                ha="center", fontsize=7.5, color=TEXT)
    ax.annotate(f"{b_params:.2f}M", (baseline_x[i], 0),
                textcoords="offset points", xytext=(0, -18),
                ha="center", fontsize=7.5, color=TEXT)

# Asymmetry badge above Run 18 baseline bar
asym_idx = 2
ax.annotate("10x params",
            (baseline_x[asym_idx], baseline_bpbs[asym_idx]),
            textcoords="offset points", xytext=(0, 20),
            ha="center", fontsize=7.5, color=TEXT, style="italic",
            bbox=dict(boxstyle="round,pad=0.25", fc=CODE_BG, ec=TEXT, lw=0.8))

ax.set_xticks(x_positions)
ax.set_xticklabels([c[0] for c in comparisons], fontsize=9)
ax.set_ylabel("T=1 BPB (lower is better)", fontsize=10, labelpad=8)
ax.set_ylim(0, 5.0)
ax.yaxis.set_major_locator(MultipleLocator(1.0))
ax.grid(True, axis="y", linestyle="-", linewidth=0.5, alpha=0.25, color=TEXT)
ax.set_axisbelow(True)

for spine in ax.spines.values():
    spine.set_linewidth(1.0)
    spine.set_color(TEXT)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

legend = ax.legend(loc="upper left", frameon=True, fontsize=8.5,
                   facecolor=BG, edgecolor=TEXT)
legend.get_frame().set_linewidth(1.0)

ax.set_title("T=1 BPB: outer-product matrix embedding vs flat-vector baselines",
             fontsize=10.5, color=TEXT, fontweight="bold", pad=14, loc="left")

# Small footer text about params row and asymmetry
fig.text(0.015, 0.015,
         "params (M) shown below each bar. * Run 22 flat baseline has 2.2x more params than matrix. "
         "Run 18 hatched bar marks 10x param asymmetry.",
         fontsize=7, color=MUTED, style="italic")

plt.tight_layout(rect=(0, 0.04, 1, 1))

out = "/Users/samuellarson/Experiments/learned-representations/pebble-ai-site/assets/plots/outer_product_embedding.svg"
plt.savefig(out, format="svg", facecolor=BG, bbox_inches="tight")
print(f"wrote {out}")
