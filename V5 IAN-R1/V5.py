# V5.py — IAN‑R1 (TRIGA) en OpenMC, versión extendida con reflector correcto y sin deprecations.

import openmc
import numpy as np
from openmc.stats import Box

# ============================================================
# 1) PARÁMETROS GLOBALES (ajusta con datos oficiales IAN‑R1)
# ============================================================
PITCH = 3.76                 # cm, separación centro‑centro TRIGA
FUEL_RADIUS = 1.55           # cm, radio combustible
CLAD_THICK = 0.05            # cm, espesor vaina
PELLET_STACK_HEIGHT = 72.0   # cm, altura activa (TODO confirmar)

U235_ENRICH_WT = 0.197       # fracción en peso de U‑235 dentro del U (19.7%)
B10_ENRICH = 0.90            # fracción isotópica de B‑10 en B4C (90%)
GRAPHITE_RHO = 1.75          # g/cc
CONCRETE_RHO = 2.3           # g/cc
SS304_RHO = 7.9              # g/cc

# Bloque reflector (debe ser mayor que el núcleo)
REFLECTOR_XY_HALF = 30.0     # cm, semi‑ancho del reflector (TODO)
REFLECTOR_HEIGHT = 80.0      # cm (>= zona activa)

# Piscina / blindaje
POOL_RADIUS = 100.0          # cm
POOL_DEPTH = 500.0           # cm
CONCRETE_OUTER_RADIUS = 260.0  # cm

# Barras de control y canales
CR_ROD_RADIUS = 1.2          # cm absorber
CR_GUIDE_RADIUS = 1.6        # cm guía (acero)
IRR_RADIUS = 1.6             # cm canal irradiación

# ============================================================
# 2) MATERIALES
# ============================================================
mats = openmc.Materials()

# Agua ligera (moderador/piscina)
h2o = openmc.Material(name='Light water', temperature=300)
h2o.set_density('g/cc', 0.997)
h2o.add_element('H', 2)
h2o.add_element('O', 1)
h2o.add_s_alpha_beta('c_H_in_H2O')
mats.append(h2o)

# Aire
air = openmc.Material(name='Air')
air.set_density('kg/m3', 1.225)
air.add_element('N', 0.7808)
air.add_element('O', 0.2095)
air.add_element('Ar', 0.0093)
air.add_element('C', 0.0004)
mats.append(air)

# Grafito
graphite = openmc.Material(name='Graphite')
graphite.set_density('g/cc', GRAPHITE_RHO)
graphite.add_element('C', 1, percent_type='ao')
graphite.add_s_alpha_beta('c_Graphite')
mats.append(graphite)

# Acero inoxidable 304
ss304 = openmc.Material(name='Stainless Steel 304')
ss304.set_density('g/cc', SS304_RHO)
ss304.add_element('Fe', 0.70, percent_type='wo')
ss304.add_element('Cr', 0.19, percent_type='wo')
ss304.add_element('Ni', 0.10, percent_type='wo')
ss304.add_element('Mn', 0.01, percent_type='wo')
mats.append(ss304)

# B4C (barras de control)
b4c = openmc.Material(name='B4C (Control Rods)')
b4c.set_density('g/cc', 2.52)
b4c.add_element('B', 4, enrichment=B10_ENRICH*100.0, enrichment_target='B10', percent_type='ao')
b4c.add_element('C', 1, percent_type='ao')
mats.append(b4c)

# Combustible TRIGA U‑ZrH1.6 (TODO: ajusta %U según lote real, p.ej. 0.085 = 8.5 wt%)
U_WT_FRACTION = 0.085

# Desglose U por isótopos (en peso, respecto al MATERIAL total):
u235_w_total = U_WT_FRACTION * U235_ENRICH_WT
u234_w_total = U_WT_FRACTION * U235_ENRICH_WT * 0.008   # U‑234 = 0.8% de la masa de U‑235
u238_w_total = U_WT_FRACTION - (u235_w_total + u234_w_total)

# ZrH1.6 fracciones en peso dentro del resto:
H_frac_in_ZrH = 0.01739
Zr_frac_in_ZrH = 1.0 - H_frac_in_ZrH
ZR_BLOCK = (1.0 - U_WT_FRACTION) * Zr_frac_in_ZrH
H_BLOCK  = (1.0 - U_WT_FRACTION) * H_frac_in_ZrH

fuel = openmc.Material(name='TRIGA fuel (U-ZrH1.6)')
fuel.set_density('g/cc', 5.95)
fuel.add_nuclide('U234', u234_w_total, percent_type='wo')
fuel.add_nuclide('U235', u235_w_total, percent_type='wo')
fuel.add_nuclide('U238', u238_w_total, percent_type='wo')
fuel.add_element('Zr', ZR_BLOCK, percent_type='wo')
fuel.add_element('H',  H_BLOCK,  percent_type='wo')
mats.append(fuel)

# Concreto
concrete = openmc.Material(name='Concrete')
concrete.set_density('g/cc', CONCRETE_RHO)
concrete.add_element('O', 0.52,  percent_type='wo')
concrete.add_element('Si', 0.325, percent_type='wo')
concrete.add_element('Ca', 0.06,  percent_type='wo')
concrete.add_element('Al', 0.02,  percent_type='wo')
concrete.add_element('Fe', 0.02,  percent_type='wo')
concrete.add_element('H',  0.055, percent_type='wo')
mats.append(concrete)

mats.export_to_xml()

# ============================================================
# 3) PINES / UNIVERSOS
# ============================================================
fuel_or = FUEL_RADIUS
clad_ir = fuel_or
clad_or = clad_ir + CLAD_THICK
pin_fuel_cyl = openmc.ZCylinder(r=fuel_or, boundary_type='transmission')
pin_clad_cyl = openmc.ZCylinder(r=clad_or, boundary_type='transmission')

fuel_cell = openmc.Cell(fill=fuel, region=-pin_fuel_cyl)
clad_cell = openmc.Cell(fill=ss304, region=+pin_fuel_cyl & -pin_clad_cyl)
mod_cell  = openmc.Cell(fill=h2o,  region=+pin_clad_cyl)
pin_fuel_univ = openmc.Universe(cells=[fuel_cell, clad_cell, mod_cell])

cr_abs_cyl   = openmc.ZCylinder(r=CR_ROD_RADIUS)
cr_guide_cyl = openmc.ZCylinder(r=CR_GUIDE_RADIUS)
cr_abs_cell   = openmc.Cell(fill=b4c,   region=-cr_abs_cyl)
cr_guide_cell = openmc.Cell(fill=ss304, region=+cr_abs_cyl & -cr_guide_cyl)
cr_mod_cell   = openmc.Cell(fill=h2o,   region=+cr_guide_cyl)
pin_cr_univ   = openmc.Universe(cells=[cr_abs_cell, cr_guide_cell, cr_mod_cell])

irr_tube_ir = openmc.ZCylinder(r=IRR_RADIUS-0.05)
irr_tube_or = openmc.ZCylinder(r=IRR_RADIUS)
irr_water_cell = openmc.Cell(fill=h2o,   region=-irr_tube_ir)
irr_tube_cell  = openmc.Cell(fill=ss304, region=+irr_tube_ir & -irr_tube_or)
irr_mod_cell   = openmc.Cell(fill=h2o,   region=+irr_tube_or)
pin_irr_univ   = openmc.Universe(cells=[irr_water_cell, irr_tube_cell, irr_mod_cell])

air_cyl = openmc.ZCylinder(r=CR_GUIDE_RADIUS)
air_core_cell = openmc.Cell(fill=air, region=-air_cyl)
air_mod_cell  = openmc.Cell(fill=h2o, region=+air_cyl)
pin_air_univ  = openmc.Universe(cells=[air_core_cell, air_mod_cell])

pin_water_univ = openmc.Universe(cells=[openmc.Cell(fill=h2o)])

# ============================================================
# 4) LATTICE DEL NÚCLEO (vista superior con “muesca”)
# ============================================================
lattice_map = [
  ['W','W','F','F','F','F','W','W'],
  ['W','F','F','F','F','C','F','W'],
  ['F','F','F','F','F','F','F','F'],
  ['F','C','F','F','I','F','F','F'],
  ['F','F','F','F','F','F','A','F'],
  ['F','F','F','F','F','F','F','W'],
  ['W','F','F','C','F','F','W','W'],
  ['W','W','F','F','F','W','W','W']
]
char_to_univ = {'F': pin_fuel_univ, 'C': pin_cr_univ, 'A': pin_air_univ, 'I': pin_irr_univ, 'W': pin_water_univ}
array_univs = np.array([[char_to_univ[ch] for ch in row] for row in lattice_map], dtype=object)

ny, nx = array_univs.shape     # filas (y), columnas (x)
core_half_x = (nx * PITCH) / 2.0
core_half_y = (ny * PITCH) / 2.0

lat = openmc.RectLattice()
lat.lower_left = (-core_half_x, -core_half_y)
lat.pitch = (PITCH, PITCH)
lat.universes = array_univs[::-1]  # fila 0 "arriba"
core_lat_univ = openmc.Universe()
core_lat_univ.add_cell(openmc.Cell(fill=lat))

# ============================================================
# 5) ZONAS: NÚCLEO (caja interna) + REFLECTOR (caja externa)
# ============================================================
# Caja interna del núcleo
cx_min = openmc.XPlane(x0=-core_half_x, boundary_type='transmission')
cx_max = openmc.XPlane(x0=+core_half_x, boundary_type='transmission')
cy_min = openmc.YPlane(y0=-core_half_y, boundary_type='transmission')
cy_max = openmc.YPlane(y0=+core_half_y, boundary_type='transmission')
cz_bot = openmc.ZPlane(z0=-REFLECTOR_HEIGHT/2, boundary_type='transmission')
cz_top = openmc.ZPlane(z0=+REFLECTOR_HEIGHT/2, boundary_type='transmission')
core_box_region = +cx_min & -cx_max & +cy_min & -cy_max & +cz_bot & -cz_top

# Caja externa del reflector (debe ser mayor que la interna)
rx_min = openmc.XPlane(x0=-REFLECTOR_XY_HALF, boundary_type='transmission')
rx_max = openmc.XPlane(x0=+REFLECTOR_XY_HALF, boundary_type='transmission')
ry_min = openmc.YPlane(y0=-REFLECTOR_XY_HALF, boundary_type='transmission')
ry_max = openmc.YPlane(y0=+REFLECTOR_XY_HALF, boundary_type='transmission')
rz_bot = openmc.ZPlane(z0=-REFLECTOR_HEIGHT/2, boundary_type='transmission')
rz_top = openmc.ZPlane(z0=+REFLECTOR_HEIGHT/2, boundary_type='transmission')
refl_box_region = +rx_min & -rx_max & +ry_min & -ry_max & +rz_bot & -rz_top

# Core = caja interna con el lattice
cell_core = openmc.Cell(fill=core_lat_univ, region=core_box_region)

# Reflector = volumen entre caja externa y caja interna
graphite_region = refl_box_region & ~core_box_region
cell_reflector = openmc.Cell(fill=graphite, region=graphite_region)

block_univ = openmc.Universe(cells=[cell_core, cell_reflector])

# ============================================================
# 6) PISCINA Y BLINDAJE
# ============================================================
pool_cyl = openmc.ZCylinder(r=POOL_RADIUS)
concrete_cyl = openmc.ZCylinder(r=CONCRETE_OUTER_RADIUS)
z_pool_bot = openmc.ZPlane(z0=-POOL_DEPTH/2, boundary_type='vacuum')
z_pool_top = openmc.ZPlane(z0=+POOL_DEPTH/2, boundary_type='vacuum')

# Hueco para insertar el bloque (usamos la caja externa del reflector)
block_region_3d = refl_box_region

pool_region = -pool_cyl & +z_pool_bot & -z_pool_top
pool_minus_block = pool_region & ~block_region_3d
pool_cell = openmc.Cell(fill=h2o, region=pool_minus_block)

concrete_region = +pool_cyl & -concrete_cyl & +z_pool_bot & -z_pool_top
concrete_cell = openmc.Cell(fill=concrete, region=concrete_region)

outside_region = +concrete_cyl | -z_pool_bot | +z_pool_top
outside_cell = openmc.Cell(fill=air, region=outside_region)

block_cell_container = openmc.Cell(fill=block_univ, region=block_region_3d)

root_univ = openmc.Universe(cells=[pool_cell, concrete_cell, outside_cell, block_cell_container])

geom = openmc.Geometry(root_univ)
geom.export_to_xml()

# ============================================================
# 7) SETTINGS (modo k‑eff y fuente moderna)
# ============================================================
settings = openmc.Settings()
settings.run_mode = 'eigenvalue'
settings.batches = 200
settings.inactive = 50
settings.particles = 50000

# Fuente (Box) centrada en el núcleo/reflector
bounds = [-REFLECTOR_XY_HALF, -REFLECTOR_XY_HALF, -PELLET_STACK_HEIGHT/2,
           REFLECTOR_XY_HALF,  REFLECTOR_XY_HALF,  PELLET_STACK_HEIGHT/2]
space = Box(bounds[:3], bounds[3:])
src = openmc.IndependentSource()
src.space = space
settings.source = src

settings.temperature = {'default': 300.0, 'method': 'interpolation'}
settings.export_to_xml()

# ============================================================
# 8) TALLIES
# ============================================================
tallies = openmc.Tallies()

mat_filter = openmc.MaterialFilter([fuel, h2o, graphite, ss304, b4c, concrete])
tally_reactor = openmc.Tally(name='flux_fission_by_material')
tally_reactor.filters = [mat_filter]
tally_reactor.scores = ['flux', 'fission']
tallies.append(tally_reactor)

mesh = openmc.RegularMesh()
mesh.dimension = [80, 80, 1]
mesh.lower_left = [-50.0, -50.0, -1.0]
mesh.upper_right = [ 50.0,  50.0,  1.0]
mesh_filter = openmc.MeshFilter(mesh)
mesh_tally = openmc.Tally(name='xy_mesh_flux')
mesh_tally.filters = [mesh_filter]
mesh_tally.scores = ['flux']
tallies.append(mesh_tally)

tallies.export_to_xml()

openmc.run()
