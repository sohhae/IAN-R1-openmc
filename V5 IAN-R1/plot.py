import openmc

# Vista XY centrada en el núcleo
plot_xy = openmc.Plot()
plot_xy.filename = 'plot_xy_core'
plot_xy.origin = (0.0, 0.0, 0.0)   # Centro del núcleo
plot_xy.width = (150.0, 150.0)     # 1.5 m de lado
plot_xy.pixels = (1200, 1200)
plot_xy.basis = 'xy'
plot_xy.color_by = 'material'
plot_xy.background = 'white'

# Vista XZ centrada en el núcleo
plot_xz = openmc.Plot()
plot_xz.filename = 'plot_xz_section'
plot_xz.origin = (0.0, 0.0, 0.0)
plot_xz.width = (300.0, 600.0)     # 3 m ancho x 6 m alto
plot_xz.pixels = (1200, 1200)
plot_xz.basis = 'xz'
plot_xz.color_by = 'material'
plot_xz.background = 'white'

plots = openmc.Plots([plot_xy, plot_xz])
plots.export_to_xml()

openmc.plot_geometry()
