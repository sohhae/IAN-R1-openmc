
import openmc

# Carga geometry/materials recién exportados
mats = openmc.Materials.from_xml()
by_name = {m.name: m for m in mats}

# --- Vista superior (XY) con zoom para ver el patrón y la fila de canales ---
plot_xy = openmc.Plot()
plot_xy.filename = 'plot_xy_core'
plot_xy.origin = (0.0, 0.0, 0.0)
plot_xy.width = (120.0, 150.0)   # ancho 120 cm, alto 150 cm para abarcar la fila de 'O'
plot_xy.pixels = (2000, 2500)
plot_xy.basis = 'xy'
plot_xy.color_by = 'material'
plot_xy.background = 'white'
plot_xy.colors = {
    by_name['TRIGA fuel (U-ZrH1.6)']: 'red',          # 🔴 combustible
    by_name['B4C (Control Rods)']: 'limegreen',       # 🟢 control
    by_name['Air']: 'khaki',                          # 🟡 aire
    by_name['Light water']: 'deepskyblue',            # 🔵 agua
    by_name['Graphite']: 'dimgray',                   # reflector
    by_name['Stainless Steel 304']: 'gray',           # vaina/guías
    by_name['Concrete']: 'orange'                     # blindaje
}

# --- Sección vertical (XZ) para ver piscina/reflector/núcleo ---
plot_xz = openmc.Plot()
plot_xz.filename = 'plot_xz_section'
plot_xz.origin = (0.0, 0.0, 0.0)
plot_xz.width = (250.0, 400.0)
plot_xz.pixels = (2000, 3200)
plot_xz.basis = 'xz'
plot_xz.color_by = 'material'
plot_xz.background = 'white'
plot_xz.colors = plot_xy.colors

openmc.Plots([plot_xy, plot_xz]).export_to_xml()
openmc.plot_geometry()
