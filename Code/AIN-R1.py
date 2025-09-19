import openmc
import numpy as np
from openmc.stats import Box

# ====== Parámetros globales ======
PITCH = 3.76
FUEL_RADIUS = 1.55
CLAD_THICK = 0.05
PELLET_STACK_HEIGHT = 72.0

U235_ENRICH_WT = 0.197
B10_ENRICH = 0.90
GRAPHITE_RHO = 1.75
CONCRETE_RHO = 2.3
SS304_RHO = 7.9

REFLECTOR_XY_HALF = 30.0
REFLECTOR_HEIGHT = 80.0
POOL_RADIUS = 100.0
POOL_DEPTH = 500.0
CONCRETE_OUTER_RADIUS = 264.0

# Pines especiales
CR_ROD_RADIUS = 1.2
CR_GUIDE_RADIUS = 1.6
IRR_RADIUS = 1.6
AIR_PIN_RADIUS = 1.6

# Referencias axiales
CORE_Z_TOP = +REFLECTOR_HEIGHT/2.0
CORE_Z_BOT = -REFLECTOR_HEIGHT/2.0

# ======================== Materiales ========================
mats = openmc.Materials()

h2o = openmc.Material(name='Light water', temperature=300)
h2o.set_density('g/cc', 0.997)
h2o.add_element('H', 2)
h2o.add_element('O', 1)
h2o.add_s_alpha_beta('c_H_in_H2O')
mats.append(h2o)

air = openmc.Material(name='Air')
air.set_density('kg/m3', 1.225)
air.add_element('N', 0.7808)
air.add_element('O', 0.2095)
air.add_element('Ar', 0.0093)
air.add_element('C', 0.0004)
mats.append(air)

air_yellow = openmc.Material(name='Air (yellow pin)')
air_yellow.set_density('kg/m3', 1.225)
air_yellow.add_element('N', 0.7808)
air_yellow.add_element('O', 0.2095)
air_yellow.add_element('Ar', 0.0093)
air_yellow.add_element('C', 0.0004)
mats.append(air_yellow)

air_white = openmc.Material(name='Air (white channel/outside)')
air_white.set_density('kg/m3', 1.225)
air_white.add_element('N', 0.7808)
air_white.add_element('O', 0.2095)
air_white.add_element('Ar', 0.0093)
air_white.add_element('C', 0.0004)
mats.append(air_white)

graphite = openmc.Material(name='Graphite')
graphite.set_density('g/cc', GRAPHITE_RHO)
graphite.add_element('C', 1, percent_type='ao')
graphite.add_s_alpha_beta('c_Graphite')
mats.append(graphite)

ss304 = openmc.Material(name='Stainless Steel 304')
ss304.set_density('g/cc', SS304_RHO)
ss304.add_element('Fe', 0.70, percent_type='wo')
ss304.add_element('Cr', 0.19, percent_type='wo')
ss304.add_element('Ni', 0.10, percent_type='wo')
ss304.add_element('Mn', 0.01, percent_type='wo')
mats.append(ss304)

b4c = openmc.Material(name='B4C (Control Rods)')
b4c.set_density('g/cc', 2.52)
b4c.add_element('B', 4, enrichment=B10_ENRICH*100.0,
                 enrichment_target='B10', percent_type='ao')
b4c.add_element('C', 1, percent_type='ao')
mats.append(b4c)

# Combustible TRIGA U-ZrH1.6
U_WT_FRACTION = 0.085
u235_w_total = U_WT_FRACTION * U235_ENRICH_WT
u234_w_total = U_WT_FRACTION * U235_ENRICH_WT * 0.008
u238_w_total = U_WT_FRACTION - (u235_w_total + u234_w_total)
H_frac_in_ZrH = 0.01739
Zr_frac_in_ZrH = 1.0 - H_frac_in_ZrH
ZR_BLOCK = (1.0 - U_WT_FRACTION) * Zr_frac_in_ZrH
H_BLOCK = (1.0 - U_WT_FRACTION) * H_frac_in_ZrH

fuel = openmc.Material(name='TRIGA fuel (U-ZrH1.6)')
fuel.set_density('g/cc', 5.95)
fuel.add_nuclide('U234', u234_w_total, percent_type='wo')
fuel.add_nuclide('U235', u235_w_total, percent_type='wo')
fuel.add_nuclide('U238', u238_w_total, percent_type='wo')
fuel.add_element('Zr', ZR_BLOCK, percent_type='wo')
fuel.add_element('H', H_BLOCK, percent_type='wo')
mats.append(fuel)

concrete = openmc.Material(name='Concrete')
concrete.set_density('g/cc', CONCRETE_RHO)
concrete.add_element('O', 0.52, percent_type='wo')
concrete.add_element('Si', 0.325, percent_type='wo')
concrete.add_element('Ca', 0.06, percent_type='wo')
concrete.add_element('Al', 0.02, percent_type='wo')
concrete.add_element('Fe', 0.02, percent_type='wo')
concrete.add_element('H', 0.055, percent_type='wo')
mats.append(concrete)

mats.export_to_xml()

# ==================== Pines / Universos =====================
# Combustible
fuel_or = FUEL_RADIUS
clad_ir = fuel_or
clad_or = clad_ir + CLAD_THICK
pin_fuel_cyl = openmc.ZCylinder(r=fuel_or, boundary_type='transmission')
pin_clad_cyl = openmc.ZCylinder(r=clad_or, boundary_type='transmission')
fuel_cell = openmc.Cell(fill=fuel, region=-pin_fuel_cyl)
clad_cell = openmc.Cell(fill=ss304, region=+pin_fuel_cyl & -pin_clad_cyl)
mod_cell = openmc.Cell(fill=h2o, region=+pin_clad_cyl)
pin_fuel_univ = openmc.Universe(cells=[fuel_cell, clad_cell, mod_cell])

# Barra de control (verde)
cr_abs_cyl = openmc.ZCylinder(r=CR_ROD_RADIUS)
cr_guide_cyl = openmc.ZCylinder(r=CR_GUIDE_RADIUS)
pin_cr_univ = openmc.Universe(cells=[
    openmc.Cell(fill=b4c, region=-cr_abs_cyl),
    openmc.Cell(fill=ss304, region=+cr_abs_cyl & -cr_guide_cyl),
    openmc.Cell(fill=h2o, region=+cr_guide_cyl)
])

# Barra de aire (amarilla)
air_cyl = openmc.ZCylinder(r=AIR_PIN_RADIUS)
pin_air_univ = openmc.Universe(cells=[
    openmc.Cell(fill=air_yellow, region=-air_cyl),
    openmc.Cell(fill=h2o, region=+air_cyl)
])

# Canal de irradiación (blanco)
irr_ir = openmc.ZCylinder(r=IRR_RADIUS-0.05)
irr_or = openmc.ZCylinder(r=IRR_RADIUS)
pin_irr_univ = openmc.Universe(cells=[
    openmc.Cell(fill=air_white, region=-irr_ir),
    openmc.Cell(fill=ss304, region=+irr_ir & -irr_or),
    openmc.Cell(fill=h2o, region=+irr_or),
])

# Reflector de grafito
pin_graphite_univ = openmc.Universe(cells=[openmc.Cell(fill=graphite)])
# Agua
pin_water_univ = openmc.Universe(cells=[openmc.Cell(fill=h2o)])
# Canal de irradiación (blanco)
irr_ir = openmc.ZCylinder(r=IRR_RADIUS-0.05)
irr_or = openmc.ZCylinder(r=IRR_RADIUS)

cell_irr_air = openmc.Cell(name="Irradiation Air", fill=air_white, region=-irr_ir)
cell_irr_ss  = openmc.Cell(name="Irradiation Steel", fill=ss304, region=+irr_ir & -irr_or)
cell_irr_mod = openmc.Cell(name="Irradiation Moderator", fill=h2o, region=+irr_or)

pin_irr_univ = openmc.Universe(cells=[cell_irr_air, cell_irr_ss, cell_irr_mod])

# Guardar la lista de celdas de irradiación
irr_cells = [cell_irr_air, cell_irr_ss, cell_irr_mod]

# ================= Lattice (NO CAMBIO EL MAPA) =================
lattice_rows = [
    ['W','W','W','W','W','W','W','W','W','W'],
    ['W','W','G','G','G','G','G','G','G','G','W'],
    ['W','G','G','F','F','F','F','F','F','G','G','W','W'],
    ['W','G','G','F','F','F','F','C','F','G','G','G','G','W'],
    ['W','G','G','F','F','F','F','F','F','F','F','G','G','W'],
    ['W','G','G','F','C','F','F','A','F','F','F','G','G','W'],
    ['W','G','G','F','F','F','F','F','F','F','F','G','G','W'],
    ['W','G','G','F','F','A','F','F','F','C','F','G','G','W'],
    ['W','G','G','G','G','F','F','F','F','F','F','G','G','W'],
    ['W','G','G','G','G','F','F','F','F','F','A','G','G','W'],
    ['W','G','G','G','G','G','G','G','G','G','G','G','G','W'],
    ['W','G','G','T','T','G','T','T','G','T','T','G','G','W'],
    ['W','G','G','G','G','G','G','G','G','G','G','G','G','W'],
    ['W','W','W','W','W','W','W','W','W','W','W','W','W','W'],
]

char_to_univ = {
    'F': pin_fuel_univ,
    'C': pin_cr_univ,
    'A': pin_air_univ,
    'T': pin_irr_univ,
    'G': pin_graphite_univ,
    'W': pin_water_univ
}

max_cols = max(len(row) for row in lattice_rows)
normalized_rows = [row + ['W']*(max_cols - len(row)) for row in lattice_rows]
array_univs = np.array([[char_to_univ[ch] for ch in row] for row in normalized_rows], dtype=object)
ny, nx = array_univs.shape

core_half_x = (nx * PITCH) / 2.0
core_half_y = (ny * PITCH) / 2.0

lat = openmc.RectLattice()
lat.lower_left = (-core_half_x, -core_half_y)
lat.pitch = (PITCH, PITCH)
lat.universes = array_univs[::-1]

block_univ = openmc.Universe()
block_univ.add_cell(openmc.Cell(fill=lat))

# ====== Contenedor del bloque (lattice completo) ======
cx_min = openmc.XPlane(x0=-core_half_x, boundary_type='transmission')
cx_max = openmc.XPlane(x0=+core_half_x, boundary_type='transmission')
cy_min = openmc.YPlane(y0=-core_half_y, boundary_type='transmission')
cy_max = openmc.YPlane(y0=+core_half_y, boundary_type='transmission')
cz_bot = openmc.ZPlane(z0=-REFLECTOR_HEIGHT/2, boundary_type='transmission')
cz_top = openmc.ZPlane(z0=+REFLECTOR_HEIGHT/2, boundary_type='transmission')
block_region = +cx_min & -cx_max & +cy_min & -cy_max & +cz_bot & -cz_top

# ================= Piscina y blindaje (escalonado circular) =================
# Z
z_pool_top = openmc.ZPlane(z0=440.0)
z_con_top = openmc.ZPlane(z0=170.0)
z_con_mid = openmc.ZPlane(z0=-50.0)
z_con_bot = openmc.ZPlane(z0=-220.0)
z_base = openmc.ZPlane(z0=-530.0)

# Radios
r_pool = openmc.ZCylinder(r=100.0)
r1_concrete = openmc.ZCylinder(r=134.0)
r2_concrete = openmc.ZCylinder(r=204.0)
r3_concrete = openmc.ZCylinder(r=264.0)
r_outer_boundary = openmc.ZCylinder(r=526.0, boundary_type='vacuum')

# Universo raíz
root_univ = openmc.Universe(name='Root Universe')

# Bloque reactor
block_cell_container = openmc.Cell(name='Reactor Block', fill=block_univ, region=block_region)

# Suelo delgado
z_floor_top = openmc.ZPlane(z0=z_base.z0 + 50.0)
floor_region = -r_pool & +z_base & -z_floor_top
floor_cell = openmc.Cell(name='Concrete Floor Thin', fill=concrete, region=floor_region)

# Piscina de agua
pool_cavity = -r_pool & +z_floor_top & -z_pool_top
pool_cell = openmc.Cell(name='Pool', fill=h2o, region=pool_cavity & ~block_region)

# --- Concreto ---
# Nivel Superior
concrete_top_ring = openmc.Cell(name='Concrete Top Ring', fill=concrete, 
                                 region=+r_pool & -r1_concrete & +z_con_top & -z_pool_top)

# Nivel Intermedio
concrete_mid_level = openmc.Cell(name='Concrete Mid Level', fill=concrete,
                                 region=+r_pool & -r2_concrete & +z_con_mid & -z_con_top)

# Nivel Inferior (Esta es la corrección clave para llenar el hueco)
concrete_low = openmc.Cell(name='Concrete Low Ring', fill=concrete, 
                           region=+r_pool & -r3_concrete & +z_con_bot & -z_con_mid)

# Base completa
concrete_base = openmc.Cell(name='Concrete Base', fill=concrete, 
                             region=-r3_concrete & +z_base & -z_con_bot)

# Aire exterior (Rellena todo el espacio vacío)
air_region = -r_outer_boundary & (~concrete_base.region & ~concrete_low.region & 
              ~concrete_mid_level.region & ~concrete_top_ring.region &
              ~floor_cell.region & ~pool_cell.region & ~block_cell_container.region)
air_cell = openmc.Cell(name='Outside Air', fill=air, region=air_region)

# Agregar al universo raíz
root_univ.add_cells([
    block_cell_container,
    pool_cell,
    floor_cell,
    concrete_top_ring,
    concrete_mid_level,
    concrete_low,
    concrete_base,
    air_cell 
])

# Geometría
geom = openmc.Geometry(root_univ)
geom.export_to_xml()

# ================= Settings =================
settings = openmc.Settings()
settings.run_mode = 'eigenvalue'
settings.batches = 200
settings.inactive = 50
settings.particles = 50000

bounds = [-REFLECTOR_XY_HALF, -REFLECTOR_XY_HALF, -PELLET_STACK_HEIGHT/2,
           REFLECTOR_XY_HALF, REFLECTOR_XY_HALF, PELLET_STACK_HEIGHT/2]
space = Box(bounds[:3], bounds[3:])
src = openmc.IndependentSource()
src.space = space
settings.source = src
settings.temperature = {'default': 300.0, 'method': 'interpolation'}
settings.export_to_xml()

# ================= Plots =================
plots = []
mat_colors = {
    h2o: (150, 200, 255),
    air: (230, 230, 230),
    air_white: (245, 245, 245),
    air_yellow: (255, 255, 200),
    fuel: (255, 160, 0),
    b4c: (20, 20, 20),
    ss304: (175, 175, 175),
    graphite: (120, 120, 120),
    concrete: (210, 180, 140),
}

# Zoom núcleo
p_zoom = openmc.Plot()
p_zoom.basis = 'xy'
p_zoom.width = (2*core_half_x*1.05, 2*core_half_y*1.05)
p_zoom.pixels = (1400, 1400)
p_zoom.level = 0
p_zoom.color_by = 'material'
p_zoom.colors = mat_colors
p_zoom.filename = 'core_zoom_xy'
plots.append(p_zoom)

# Vista completa XY
p_full = openmc.Plot()
p_full.basis = 'xy'
p_full.width = (2*r3_concrete.r * 1.1, 2*r3_concrete.r * 1.1)
p_full.pixels = (1400, 1400)
p_full.level = 0
p_full.color_by = 'material'
p_full.colors = mat_colors
p_full.filename = 'core_full_xy'
plots.append(p_full)

# Vista XZ (perfil)
p_xz = openmc.Plot()
p_xz.basis = 'xz'
p_xz.width = (2*r3_concrete.r * 1.1, (z_pool_top.z0 - z_base.z0)*1.1)
p_xz.pixels = (1400, 1400)
p_xz.color_by = 'material'
p_xz.colors = mat_colors
p_xz.filename = 'reactor_xz'
plots.append(p_xz)

openmc.Plots(plots).export_to_xml()
openmc.plot_geometry()

# ================= Tallies =================
tallies = openmc.Tallies()

# Por material
mat_filter = openmc.MaterialFilter([fuel, h2o, graphite, ss304, b4c, concrete, air, air_white, air_yellow])
tally_reactor = openmc.Tally(name='flux_fission_by_material')
tally_reactor.filters = [mat_filter]
tally_reactor.scores = ['flux', 'fission']
tallies.append(tally_reactor)

# Malla XY
mesh = openmc.RegularMesh()
mesh.dimension = [80, 80, 1]
mesh.lower_left = [-50.0, -50.0, -1.0]
mesh.upper_right = [ 50.0, 50.0, 1.0]
mesh_filter = openmc.MeshFilter(mesh)
mesh_tally = openmc.Tally(name='xy_mesh_flux')
mesh_tally.filters = [mesh_filter]
mesh_tally.scores = ['flux']
tallies.append(mesh_tally)

# Malla Z (axial)
z_mesh = openmc.RegularMesh()
z_mesh.dimension = [1, 1, 80]
z_mesh.lower_left = [-1.0, -1.0, -50.0]
z_mesh.upper_right = [ 1.0, 1.0, 50.0]
z_mesh_filter = openmc.MeshFilter(z_mesh)
z_tally = openmc.Tally(name='z_mesh_flux')
z_tally.filters = [z_mesh_filter]
z_tally.scores = ['flux']
tallies.append(z_tally)

# === Tally: Espectros de energía en el canal de irradiación ===
energy_filter = openmc.EnergyFilter.from_group_structure("XMAS-172")
cell_filter = openmc.CellFilter(irr_cells)

tally_spectra = openmc.Tally(name="multi_cell_spectrum")
tally_spectra.filters = [cell_filter, energy_filter]
tally_spectra.scores = ["flux"]

tallies.append(tally_spectra)

# === Tally radial ===
r_mesh = openmc.CylindricalMesh(
    r_grid=np.linspace(0.0, 60.0, 30),  # radios 0–60 cm en 30 bins
    z_grid=[-50.0, 50.0],               # altura (un solo bin entre -50 y 50 cm)
    phi_grid=[0.0, 2*np.pi]             # ángulo (un solo bin para todo 360°)
)

r_filter = openmc.MeshFilter(r_mesh)

radial_tally = openmc.Tally(name="radial_flux")
radial_tally.filters = [r_filter]
radial_tally.scores = ["flux"]
tallies.append(radial_tally)

# Malla Z (axial)
z_mesh = openmc.RegularMesh()
z_mesh.dimension = [1, 1, 80]
z_mesh.lower_left = [-1.0, -1.0, -50.0]
z_mesh.upper_right = [ 1.0, 1.0, 50.0]
z_mesh_filter = openmc.MeshFilter(z_mesh)
z_tally = openmc.Tally(name='z_mesh_flux')
z_tally.filters = [z_mesh_filter]
z_tally.scores = ['flux']
tallies.append(z_tally)

# --- Flux, fission y absorción por material ---
mat_filter = openmc.MaterialFilter([fuel, h2o, graphite, ss304, b4c, concrete, air, air_white, air_yellow])
tally_reactor = openmc.Tally(name='flux_fission_absorption_by_material')
tally_reactor.filters = [mat_filter]
tally_reactor.scores = ['flux', 'fission', 'absorption']
tallies.append(tally_reactor)

# === Tally: Espectros por material ===
energy_filter = openmc.EnergyFilter.from_group_structure("XMAS-172")
mat_filter = openmc.MaterialFilter([fuel, h2o, graphite, b4c])

tally_spectrum_materials = openmc.Tally(name="spectrum_by_material")
tally_spectrum_materials.filters = [mat_filter, energy_filter]
tally_spectrum_materials.scores = ["flux"]

tallies.append(tally_spectrum_materials)

# === Tally radial extendido ===
r_mesh = openmc.CylindricalMesh(
    r_grid=np.linspace(0.0, 60.0, 60),  
    z_grid=[-50.0, 50.0],               
    phi_grid=[0.0, 2*np.pi]             
)

r_filter = openmc.MeshFilter(r_mesh)

radial_tally = openmc.Tally(name="radial_flux_extended")
radial_tally.filters = [r_filter]
radial_tally.scores = ["flux"]
tallies.append(radial_tally)

# === Tally axial extendido ===
z_mesh = openmc.RegularMesh()
z_mesh.dimension = [1, 1, 100]         # 100 bins para más detalle
z_mesh.lower_left = [-1.0, -1.0, -250.0]  # de -250 cm
z_mesh.upper_right = [ 1.0,  1.0,  250.0] # a +250 cm
z_filter = openmc.MeshFilter(z_mesh)

axial_tally = openmc.Tally(name="axial_flux_extended")
axial_tally.filters = [z_filter]
axial_tally.scores = ["flux"]
tallies.append(axial_tally)


tallies.export_to_xml()

# ====== Ejecutar ======
openmc.run()