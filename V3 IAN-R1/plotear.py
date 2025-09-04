import openmc

# Crear un objeto de tipo Plot
plot = openmc.Plot()
plot.filename = "core_xy"
plot.basis = 'xz'
plot.origin = (0.0, 0.0, 0.0)
plot.width = (7.0, 7.0)
plot.pixels = (600, 600)
plot.color_by = 'material'

# Exportar el XML de plots
plots = openmc.Plots([plot])
plots.export_to_xml()

# Ejecutar la generación del gráfico
openmc.plot_geometry()
