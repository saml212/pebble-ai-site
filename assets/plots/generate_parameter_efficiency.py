"""
Generate parameter_efficiency.svg for the parameter-efficiency finding.

Horizontal bar chart comparing parameter count per projection at d=16 for
four projection families:

  - Flatten -> Linear (d^2 x d^2): 65,536 params
  - Kronecker K=8 (sum of 8 sandwich products): 4,096 params
  - Kronecker K=4 (sum of 4 sandwich products): 2,048 params
  - RowThenCol bilinear (silu(A @ M) @ B, A, B in R^{d x d}): 512 params

Numbers come from research/matrix-native-projections.md and
research/matrix-native-operations-code.md. Ratio 65,536 / 512 = 128x.

Log scale on x-axis so the 128x difference is legible without crushing
the small bars. Brand palette.

Output: SVG at pebble-ai-site/assets/plots/parameter_efficiency.svg
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Brand palette
BG = "#FAF5E7"
TEXT = "#1a1a1a"
ACCENT = "#8B2E1F"
ACCENT_SOFT = "#c4826b"
MUTED = "#5a5a5a"
CODE_BG = "#f0e9d3"

# (label, params at d=16, colour, note)
# Ordered from most params (top) to fewest (bottom) so the visual slope
# reads left-to-right as the efficiency gain.
rows = [
    ("Flatten -> Linear\n(d^2 x d^2)", 65_536, MUTED, "baseline"),
    ("Kronecker K=8\n(8 x A_k @ M @ B_k)", 4_096, ACCENT_SOFT, "16x fewer"),
    ("Kronecker K=4\n(4 x A_k @ M @ B_k)", 2_048, ACCENT_SOFT, "32x fewer"),
    ("RowThenCol bilinear\nsilu(A @ M) @ B", 512, ACCENT, "128x fewer"),
]

plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["text.color"] = TEXT
plt.rcParams["axes.labelcolor"] = TEXT
plt.rcParams["xtick.color"] = TEXT
plt.rcParams["ytick.color"] = TEXT
plt.rcParams["axes.edgecolor"] = TEXT

fig, ax = plt.subplots(figsize=(7.6, 4.6), facecolor=BG)
ax.set_facecolor(BG)

labels = [r[0] for r in rows]
values = [r[1] for r in rows]
colors = [r[2] for r in rows]
notes = [r[3] for r in rows]

y_positions = list(range(len(rows)))
y_positions.reverse()  # so the first row appears at the top

bars = ax.barh(
    y_positions, values,
    color=colors, edgecolor=TEXT, linewidth=1.0, height=0.62, zorder=3,
)

# Annotate each bar with the raw param count and the "Nx fewer" note.
for bar, val, note in zip(bars, values, notes):
    y = bar.get_y() + bar.get_height() / 2
    # Number label just past the bar end.
    ax.annotate(
        f"{val:,}",
        (val, y),
        xytext=(6, 0),
        textcoords="offset points",
        va="center",
        ha="left",
        fontsize=9,
        color=TEXT,
        fontweight="bold",
    )
    # "Nx fewer" note one line below the number, muted.
    if note != "baseline":
        ax.annotate(
            note,
            (val, y),
            xytext=(6, -11),
            textcoords="offset points",
            va="center",
            ha="left",
            fontsize=7.5,
            color=MUTED,
            style="italic",
        )
    else:
        ax.annotate(
            note,
            (val, y),
            xytext=(6, -11),
            textcoords="offset points",
            va="center",
            ha="left",
            fontsize=7.5,
            color=MUTED,
            style="italic",
        )

ax.set_yticks(y_positions)
ax.set_yticklabels(labels, fontsize=8.5)
ax.set_xscale("log")
ax.set_xlim(200, 400_000)
ax.set_xlabel("parameters per projection (d = 16, log scale)", fontsize=10, labelpad=8)

ax.grid(True, axis="x", linestyle="-", linewidth=0.5, alpha=0.25, color=TEXT)
ax.set_axisbelow(True)

for spine in ax.spines.values():
    spine.set_linewidth(1.0)
    spine.set_color(TEXT)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.set_title(
    "parameters per projection at d = 16",
    fontsize=11, color=TEXT, fontweight="bold", pad=14, loc="left",
)

# Footer note naming the source files.
fig.text(
    0.015, 0.015,
    "counts from research/matrix-native-projections.md and research/matrix-native-operations-code.md. "
    "ratio 65,536 / 512 = 128x.",
    fontsize=7, color=MUTED, style="italic",
)

plt.tight_layout(rect=(0, 0.04, 1, 1))

out = "/Users/samuellarson/Experiments/learned-representations/pebble-ai-site/assets/plots/parameter_efficiency.svg"
plt.savefig(out, format="svg", facecolor=BG, bbox_inches="tight")
print(f"wrote {out}")
