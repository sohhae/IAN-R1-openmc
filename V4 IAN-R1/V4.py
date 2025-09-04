# ===================
# MODELO DETALLADO DEL REACTOR IAN-R1 EN OPENMC
# Basado en configuración TRIGA Mark I con 50 elementos combustibles LEU, reflector de grafito y piscina de agua
# ===================

import openmc
import numpy as np


# 1. MATERIALES

uzrh_fuel = openmc.Material(name="U-ZrH Fuel")
uzrh_fuel.set_density("g/cm3", 6.5)
uzrh_fuel.add_element("U", 1.0, enrichment=19.7)
uzrh_fuel.add_element("Zr", 1.0)
uzrh_fuel.add_element("H", 1.6)

water = openmc.Material(name="Light Water")
water.set_density("g/cm3", 1.0)
water.add_nuclide("H1", 2.0)
water.add_nuclide("O16", 1.0)
water.add_s_alpha_beta("c_H_in_H2O")

b4c = openmc.Material(name="B4C Control Rod")
b4c.set_density("g/cm3", 2.52)
b4c.add_element("B", 4.0)
b4c.add_element("C", 1.0)

graphite = openmc.Material(name="Graphite Reflector")
graphite.set_density("g/cm3", 1.7)
graphite.add_element("C", 1.0)

materials = openmc.Materials([uzrh_fuel, water, b4c, graphite])
materials.export_to_xml()


# 2. GEOMETRÍA

fuel_radius = 0.4  # cm
pin_height = 60.0  # cm (aproximado)

fuel_cylinder = openmc.ZCylinder(r=fuel_radius)
z_top = openmc.ZPlane(z0=+pin_height/2, boundary_type='reflective')
z_bottom = openmc.ZPlane(z0=-pin_height/2, boundary_type='reflective')

fuel_region = -fuel_cylinder & -z_top & +z_bottom
moderator_region = +fuel_cylinder & -z_top & +z_bottom

fuel_cell = openmc.Cell(fill=uzrh_fuel, region=fuel_region)
mod_cell = openmc.Cell(fill=water, region=moderator_region)
fuel_pin = openmc.Universe(cells=[fuel_cell, mod_cell])

# Celdas vacías y de control
empty_univ = openmc.Universe()
control_rod_cell = openmc.Cell(fill=b4c, region=-fuel_cylinder & -z_top & +z_bottom)
control_univ = openmc.Universe(cells=[control_rod_cell])

# Rejilla hexagonal 5 anillos
lattice = openmc.HexLattice(name="IAN-R1 Core")
lattice.center = (0.0, 0.0)
lattice.pitch = (1.3,)  # cm entre centros de elementos

ring_0 = [fuel_pin]
ring_1 = [fuel_pin]*6
ring_2 = [fuel_pin]*12
ring_3 = [fuel_pin]*18
ring_4 = [fuel_pin]*13 + [empty_univ]*5  # simula canales y barras de control

# Asignar barras de control (posiciones conocidas)
ring_4[0] = control_univ
ring_4[3] = control_univ
ring_4[6] = control_univ

lattice.universes = [ring_0, ring_1, ring_2, ring_3, ring_4]

# Insertar el núcleo en celda de agua
core_region = -openmc.ZCylinder(r=10.0)
core_cell = openmc.Cell(region=core_region, fill=lattice)

# Reflector radial de grafito
graphite_region = +openmc.ZCylinder(r=10.0) & -openmc.ZCylinder(r=15.0)
graphite_cell = openmc.Cell(region=graphite_region, fill=graphite)

# Piscina externa de agua
outer_boundary = openmc.Sphere(r=30.0, boundary_type='vacuum')
outer_region = +openmc.ZCylinder(r=15.0) & -outer_boundary
outer_cell = openmc.Cell(region=outer_region, fill=water)

universe = openmc.Universe(cells=[core_cell, graphite_cell, outer_cell])
geometry = openmc.Geometry(universe)
geometry.export_to_xml()


# 3. SETTINGS

settings = openmc.Settings()
settings.batches = 200
settings.inactive = 20
settings.particles = 5000
settings.run_mode = 'eigenvalue'

source = openmc.IndependentSource()
source.space = openmc.stats.Point((0.0, 0.0, 0.0))
settings.source = source
settings.export_to_xml()

# 4. TALLIES

tallies = openmc.Tallies()

# Flujo en el núcleo
flux_tally = openmc.Tally(name="Flux tally")
flux_tally.filters = [openmc.CellFilter(core_cell)]
flux_tally.scores = ["flux"]
tallies.append(flux_tally)

# Flujo en malla XY
mesh = openmc.RegularMesh()
mesh.dimension = [100, 100, 1]
mesh.lower_left = [-15, -15, -1]
mesh.upper_right = [15, 15, 1]

mesh_filter = openmc.MeshFilter(mesh)
mesh_tally = openmc.Tally(name="Mesh Flux")
mesh_tally.filters = [mesh_filter]
mesh_tally.scores = ["flux"]
tallies.append(mesh_tally)

tallies.export_to_xml()


# 5. EJECUTAR SIMULACIÓN

openmc.run()