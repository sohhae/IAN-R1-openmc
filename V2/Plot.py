import openmc

# Define geometry limits
POOL_RADIUS = 200.0
POOL_HEIGHT = 600.0
REFLECTOR_XY_HALF = 50.0
REFLECTOR_HEIGHT = 400.0
CORE_HALF_X = 20.0
CORE_HALF_Y = 20.0
CORE_HEIGHT = 300.0

plots = []

# --- Plot 1: Full Pool (XY view) ---
plot1 = openmc.Plot()
plot1.filename = "pool_xy"
plot1.width = (2*POOL_RADIUS, 2*POOL_RADIUS)
plot1.pixels = (800, 800)
plot1.color_by = 'material'
plot1.basis = 'xy'
plot1.origin = (0.0, 0.0, 0.0)   # set separately
plots.append(plot1)

# --- Plot 2: Core Zoom (XY view) ---
plot2 = openmc.Plot()
plot2.filename = "core_xy"
plot2.width = (2*REFLECTOR_XY_HALF*1.2, 2*REFLECTOR_XY_HALF*1.2)
plot2.pixels = (800, 800)
plot2.color_by = 'material'
plot2.basis = 'xy'
plot2.origin = (0.0, 0.0, 0.0)
plots.append(plot2)

# --- Plot 3: Core Side (XZ view) ---
plot3 = openmc.Plot()
plot3.filename = "core_xz"
plot3.width = (2*REFLECTOR_XY_HALF*1.2, CORE_HEIGHT*1.2)
plot3.pixels = (800, 800)
plot3.color_by = 'material'
plot3.basis = 'xz'
plot3.origin = (0.0, 0.0, 0.0)
plots.append(plot3)

# --- Plot 4: Core Side (YZ view) ---
plot4 = openmc.Plot()
plot4.filename = "core_yz"
plot4.width = (2*REFLECTOR_XY_HALF*1.2, CORE_HEIGHT*1.2)
plot4.pixels = (800, 800)
plot4.color_by = 'material'
plot4.basis = 'yz'
plot4.origin = (0.0, 0.0, 0.0)
plots.append(plot4)

# Export plots.xml
plot_file = openmc.Plots(plots)
plot_file.export_to_xml()

print("✅ plots.xml has been created. Run:  openmc-plot --geometry")
