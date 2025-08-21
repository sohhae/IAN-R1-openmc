# CoreSideSchematic.py
# XZ side-view schematic (not OpenMC-dependent) matching your IAN‑R1 setup.

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D

# ===== Match these to your reactor model =====
PITCH = 3.76                # cm (pin pitch)
CR_ROD_RADIUS = 1.2         # cm (B4C absorber radius)
CR_GUIDE_RADIUS = 1.6       # cm (guide outer radius)
REFLECTOR_XY_HALF = 30.0    # cm (half-width of graphite block)
REFLECTOR_HEIGHT  = 80.0    # cm (height of graphite block)
PELLET_STACK_HEIGHT = 72.0  # cm (active fuel height)

POOL_RADIUS = 100.0         # cm (pool inner radius in plan view)
POOL_DEPTH  = 500.0         # cm (pool depth)
CONCRETE_OUTER_RADIUS = 260.0  # cm (outer radius of concrete well)

# For the **schematic cut** we show a central XZ slice (y=0).
# Three control-rod column positions from your 9×9 lattice (cols 2,4,6):
nx = 9
col_center = (nx - 1) / 2.0  # 4
ROD_COLS = [2, 4, 6]
ROD_X = [(c - col_center) * PITCH for c in ROD_COLS]  # x-positions in cm

# Control-rod insertion depths from **top of graphite block** (as in your model)
CR_INSERTIONS_CM = [55.0, 35.0, 10.0]  # adjust as you like (Shim, Safety, Reg)

# Derived axial refs
CORE_Z_TOP =  REFLECTOR_HEIGHT / 2.0
CORE_Z_BOT = -REFLECTOR_HEIGHT / 2.0
FUEL_Z_TOP =  PELLET_STACK_HEIGHT / 2.0
FUEL_Z_BOT = -PELLET_STACK_HEIGHT / 2.0

# ===== Visual style =====
COL = {
    'bg':        '#ffffff',
    'water':     '#a6d8ff',
    'concrete':  '#c7c2b1',
    'graphite':  '#9e9e9e',
    'guide':     '#b0b0b0',
    'b4c':       '#000000',
    'active':    '#ffd27f'  # fuel active band overlay
}
EDGE = '#333333'

# ===== Figure =====
fig, ax = plt.subplots(figsize=(10, 6), dpi=200)
ax.set_facecolor(COL['bg'])

# Coordinate extents (x horizontal, z vertical)
x_pad = 10
z_pad = 10
x_left  = -CONCRETE_OUTER_RADIUS - x_pad
x_right =  CONCRETE_OUTER_RADIUS + x_pad
z_top   =  POOL_DEPTH/2 + z_pad
z_bot   = -POOL_DEPTH/2 - z_pad

# ---- Concrete well (outer) ----
ax.add_patch(Rectangle(
    (x_left, -POOL_DEPTH/2),   # (x,z) bottom-left
    2*CONCRETE_OUTER_RADIUS + 2*x_pad,
    POOL_DEPTH,
    facecolor=COL['concrete'], edgecolor=EDGE, lw=1.2, zorder=0
))

# ---- Pool water (inner) ----
ax.add_patch(Rectangle(
    (-POOL_RADIUS, -POOL_DEPTH/2),
    2*POOL_RADIUS,
    POOL_DEPTH,
    facecolor=COL['water'], edgecolor=EDGE, lw=0.8, zorder=1
))

# ---- Graphite block (core block) ----
ax.add_patch(Rectangle(
    (-REFLECTOR_XY_HALF, CORE_Z_BOT),
    2*REFLECTOR_XY_HALF,
    REFLECTOR_HEIGHT,
    facecolor=COL['graphite'], edgecolor=EDGE, lw=1.2, zorder=2
))

# ---- Active fuel band (for visual reference) ----
ax.add_patch(Rectangle(
    (-REFLECTOR_XY_HALF, FUEL_Z_BOT),
    2*REFLECTOR_XY_HALF,
    PELLET_STACK_HEIGHT,
    facecolor=COL['active'], edgecolor='none', alpha=0.35, zorder=3
))

# ---- Control rods (guides + B4C insertion from top) ----
for i, (x, ins) in enumerate(zip(ROD_X, CR_INSERTIONS_CM), start=1):
    # Guide tube (full block height)
    guide_w = 2*CR_GUIDE_RADIUS
    ax.add_patch(Rectangle(
        (x - guide_w/2, CORE_Z_BOT),
        guide_w,
        REFLECTOR_HEIGHT,
        facecolor=COL['guide'], edgecolor=EDGE, lw=0.8, zorder=4
    ))

    # B4C absorber segment: from CORE_Z_TOP down to CORE_Z_TOP - ins
    z_abs_top = CORE_Z_TOP
    z_abs_bot = max(CORE_Z_TOP - ins, CORE_Z_BOT)  # clip to block if needed
    b4c_w = 2*CR_ROD_RADIUS
    ax.add_patch(Rectangle(
        (x - b4c_w/2, z_abs_bot),
        b4c_w,
        z_abs_top - z_abs_bot,
        facecolor=COL['b4c'], edgecolor=EDGE, lw=0.6, zorder=5
    ))

    # Label
    ax.text(x, CORE_Z_TOP + 3.0, f"CR{i}\n{ins:.0f} cm",
            ha='center', va='bottom', fontsize=8, color='#111', zorder=6)

# ---- Axes/labels/legend ----
ax.set_xlim(x_left, x_right)
ax.set_ylim(z_bot, z_top)
ax.set_aspect('equal', adjustable='box')

ax.set_xlabel('X (cm)')
ax.set_ylabel('Z (cm)')
ax.set_title('IAN‑R1 — XZ Side View (Pool, Concrete, Graphite Block, Control Rod Insertions)', fontsize=12, pad=10)

# Axial reference lines
ax.axhline(CORE_Z_TOP, color=EDGE, lw=0.6, ls='--', alpha=0.6)
ax.axhline(CORE_Z_BOT, color=EDGE, lw=0.6, ls='--', alpha=0.6)
ax.text(x_right-5, CORE_Z_TOP+1.5, 'Block Top', ha='right', va='bottom', fontsize=8)
ax.text(x_right-5, CORE_Z_BOT-1.5, 'Block Bottom', ha='right', va='top', fontsize=8)

# Legend
legend_elems = [
    Line2D([0],[0], marker='s', color='w', label='Concrete Well',
           markerfacecolor=COL['concrete'], markersize=12),
    Line2D([0],[0], marker='s', color='w', label='Pool Water',
           markerfacecolor=COL['water'], markersize=12),
    Line2D([0],[0], marker='s', color='w', label='Graphite Block',
           markerfacecolor=COL['graphite'], markersize=12),
    Line2D([0],[0], marker='s', color='w', label='Active Fuel Height',
           markerfacecolor=COL['active'], markersize=12),
    Line2D([0],[0], marker='s', color='w', label='CR Guide (Steel)',
           markerfacecolor=COL['guide'], markersize=12),
    Line2D([0],[0], marker='s', color='w', label='B4C Absorber (Inserted)',
           markerfacecolor=COL['b4c'], markersize=12),
]
ax.legend(handles=legend_elems, loc='lower right', frameon=True, fontsize=8)

ax.grid(alpha=0.15, linewidth=0.5)
plt.tight_layout()
plt.savefig('core_side_xz.png', dpi=300)
print('✅ Saved: core_side_xz.png')
