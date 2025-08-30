# CoreSchematic.py
# Draws a clean XY schematic of your core like the reference image.
# No OpenMC dependency: pure matplotlib using your same lattice and sizes.

import math
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
from matplotlib.lines import Line2D

# ====== Parameters (copy from your model so it matches) ======
PITCH = 3.76               # cm, pin pitch (center-to-center)
FUEL_RADIUS = 1.55         # cm, fuel radius
CLAD_THICK = 0.05          # cm, cladding thickness
CR_ROD_RADIUS = 1.2        # cm, B4C radius (absorber)
CR_GUIDE_RADIUS = 1.6      # cm, steel guide outer radius
IRR_RADIUS = 1.6           # cm, irradiation channel tube OR
REFLECTOR_XY_HALF = 30.0   # cm, half-width of graphite block

# === Lattice (your updated 9x9 with 3 control rods) ===
# 'F'=fuel, 'C'=control rod position, 'A'=air rod, 'O'=irradiation channel, 'W'=water/reflector
lattice_map = [
  ['W','W','W','W','W','W','W','W','W'],
  ['W','F','F','F','F','F','W','W','W'],
  ['W','F','F','F','F','F','F','W','W'],
  ['W','F','C','F','F','F','F','F','W'],
  ['W','F','F','F','F','F','F','F','W'],
  ['W','W','F','F','F','F','F','F','W'],
  ['W','W','F','F','C','F','F','F','W'],  # center rod
  ['W','W','F','F','F','F','C','F','W'],
  ['W','O','O','O','O','O','O','O','W']
]

# ====== Visual style (tweak to taste) ======
COLORS = {
    'background':  '#ffffff',
    'graphite':    '#9e9e9e',
    'water':       '#a6d8ff',
    'fuel':        '#ffa500',
    'clad':        '#b0b0b0',
    'steel':       '#b0b0b0',
    'b4c':         '#000000',
    'air':         '#ffffff',
    'irr':         '#ffffff',
    'grid':        '#777777'
}
EDGE = '#333333'

# ====== Helpers ======
def cm_to_ax(x_cm):
    # identity (we plot directly in cm units for clarity)
    return x_cm

ny = len(lattice_map)
nx = len(lattice_map[0])

# Coordinates so that row 0 is at the top visually (like your picture)
# Center the lattice at (0,0) in cm
x0 = - (nx - 1) * PITCH / 2.0
y0 = + (ny - 1) * PITCH / 2.0

# Outer dimensions for graphite block box
box_w = 2 * REFLECTOR_XY_HALF
box_h = 2 * REFLECTOR_XY_HALF

# ====== Create figure ======
fig, ax = plt.subplots(figsize=(9, 9), dpi=200)
ax.set_facecolor(COLORS['background'])

# Draw graphite reflector box
ax.add_patch(Rectangle(
    (-REFLECTOR_XY_HALF, -REFLECTOR_XY_HALF),  # bottom-left
    box_w, box_h,
    facecolor=COLORS['graphite'], edgecolor=EDGE, lw=1.5, zorder=0
))

# Draw grid lines for lattice (light)
for i in range(nx + 1):
    x = x0 + i * PITCH
    ax.plot([x, x], [y0, y0 - ny * PITCH], color=COLORS['grid'], lw=0.4, alpha=0.35, zorder=1)
for j in range(ny + 1):
    y = y0 - j * PITCH
    ax.plot([x0, x0 + nx * PITCH], [y, y], color=COLORS['grid'], lw=0.4, alpha=0.35, zorder=1)

# Label rows/cols
for i in range(nx):
    x = x0 + i * PITCH + PITCH/2
    ax.text(x, y0 + 0.9, f"c{i}", ha='center', va='bottom', fontsize=7, color='#222')
for j in range(ny):
    y = y0 - j * PITCH - PITCH/2
    ax.text(x0 - 1.2, y, f"r{j}", ha='right', va='center', fontsize=7, color='#222')

# ====== Draw pins by type (circles) ======
clad_or = FUEL_RADIUS + CLAD_THICK

irr_label_count = 0
cr_label_count = 0

for r, row in enumerate(lattice_map):
    for c, ch in enumerate(row):
        # Center of this lattice position
        cx = x0 + c * PITCH + PITCH/2
        cy = y0 - r * PITCH - PITCH/2

        if ch == 'W':
            # Water "cell" inside block – just light blue square to make it obvious
            ax.add_patch(Rectangle(
                (cx - PITCH/2, cy - PITCH/2), PITCH, PITCH,
                facecolor=COLORS['water'], edgecolor='none', zorder=2, alpha=0.55
            ))
            continue

        if ch == 'F':
            # Draw water cell for contrast
            ax.add_patch(Rectangle(
                (cx - PITCH/2, cy - PITCH/2), PITCH, PITCH,
                facecolor=COLORS['water'], edgecolor='none', alpha=0.35, zorder=2
            ))
            # Clad ring (outer)
            ax.add_patch(Circle((cx, cy), radius=clad_or, facecolor=COLORS['clad'],
                                edgecolor=EDGE, lw=0.8, zorder=3))
            # Fuel
            ax.add_patch(Circle((cx, cy), radius=FUEL_RADIUS, facecolor=COLORS['fuel'],
                                edgecolor=EDGE, lw=0.6, zorder=4))

        elif ch == 'C':
            # Water square
            ax.add_patch(Rectangle(
                (cx - PITCH/2, cy - PITCH/2), PITCH, PITCH,
                facecolor=COLORS['water'], edgecolor='none', alpha=0.35, zorder=2
            ))
            # Guide (steel) outer
            ax.add_patch(Circle((cx, cy), radius=CR_GUIDE_RADIUS, facecolor=COLORS['steel'],
                                edgecolor=EDGE, lw=0.8, zorder=3))
            # Absorber (B4C) inner
            ax.add_patch(Circle((cx, cy), radius=CR_ROD_RADIUS, facecolor=COLORS['b4c'],
                                edgecolor=EDGE, lw=0.6, zorder=4))
            cr_label_count += 1
            ax.text(cx, cy, f"CR{cr_label_count}", ha='center', va='center',
                    fontsize=7, color='white', zorder=5)

        elif ch == 'A':
            # Air rod inside water (use white core)
            ax.add_patch(Rectangle(
                (cx - PITCH/2, cy - PITCH/2), PITCH, PITCH,
                facecolor=COLORS['water'], edgecolor='none', alpha=0.35, zorder=2
            ))
            ax.add_patch(Circle((cx, cy), radius=CR_GUIDE_RADIUS, facecolor=COLORS['air'],
                                edgecolor=EDGE, lw=0.8, zorder=3))
            ax.text(cx, cy, "AIR", ha='center', va='center', fontsize=7, color='#333', zorder=4)

        elif ch == 'O':
            # Irradiation channel tube (white) inside water
            ax.add_patch(Rectangle(
                (cx - PITCH/2, cy - PITCH/2), PITCH, PITCH,
                facecolor=COLORS['water'], edgecolor='none', alpha=0.35, zorder=2
            ))
            ax.add_patch(Circle((cx, cy), radius=IRR_RADIUS, facecolor=COLORS['irr'],
                                edgecolor=EDGE, lw=0.8, zorder=3))
            irr_label_count += 1
            ax.text(cx, cy, f"IRR{irr_label_count}", ha='center', va='center',
                    fontsize=7, color='#222', zorder=4)

# Axes/limits/format
pad = 3.0
ax.set_xlim(-REFLECTOR_XY_HALF - pad, REFLECTOR_XY_HALF + pad)
ax.set_ylim(-REFLECTOR_XY_HALF - pad, REFLECTOR_XY_HALF + pad)
ax.set_aspect('equal', adjustable='box')
ax.set_xticks([])
ax.set_yticks([])
ax.set_title("IAN‑R1 Core — XY Schematic (like reference)", fontsize=12, pad=10)

# Legend
legend_elems = [
    Line2D([0],[0], marker='s', color='w', label='Graphite Reflector',
           markerfacecolor=COLORS['graphite'], markersize=12),
    Line2D([0],[0], marker='s', color='w', label='Water (inside block)',
           markerfacecolor=COLORS['water'], markersize=12),
    Line2D([0],[0], marker='o', color=EDGE, label='Fuel (w/ cladding)',
           markerfacecolor=COLORS['fuel'], markersize=10),
    Line2D([0],[0], marker='o', color=EDGE, label='Control Rod (B4C in guide)',
           markerfacecolor=COLORS['b4c'], markersize=10),
    Line2D([0],[0], marker='o', color=EDGE, label='Irradiation Channel',
           markerfacecolor=COLORS['irr'], markersize=10),
    Line2D([0],[0], marker='o', color=EDGE, label='Air Rod',
           markerfacecolor=COLORS['air'], markersize=10),
]
ax.legend(handles=legend_elems, loc='upper right', frameon=True, fontsize=8)

plt.tight_layout()
plt.savefig("core_like_picture.png", dpi=300)
print("✅ Saved: core_like_picture.png")
