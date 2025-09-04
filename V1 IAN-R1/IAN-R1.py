import openmc

# ------------------------
# 1. MATERIALES
# ------------------------
fuel = openmc.Material(name="UO2 Fuel")
fuel.add_element("U", 1.0, enrichment=19.75)  # Enriquecido para TRIGA
fuel.add_element("O", 2.0)
fuel.set_density("g/cm3", 10.4)

moderator = openmc.Material(name="Water")
moderator.add_nuclide("H1", 2.0)
moderator.add_nuclide("O16", 1.0)
moderator.set_density("g/cm3", 1.0)
moderator.add_s_alpha_beta("c_H_in_H2O")

reflector = openmc.Material(name="Graphite Reflector")
reflector.add_element("C", 1.0)
reflector.set_density("g/cm3", 1.6)

materials = openmc.Materials([fuel, moderator, reflector])
materials.export_to_xml()

# ------------------------
# 2. GEOMETRÍA
# ------------------------
fuel_radius = openmc.ZCylinder(r=0.4)
moderator_radius = openmc.ZCylinder(r=0.6)
reflector_box = openmc.model.rectangular_prism(width=12.0, height=12.0, boundary_type='reflective')

fuel_cell = openmc.Cell(name="Fuel", fill=fuel, region=-fuel_radius)
moderator_cell = openmc.Cell(name="Moderator", fill=moderator, region=+fuel_radius & -moderator_radius)
reflector_cell = openmc.Cell(name="Reflector", fill=reflector, region=+moderator_radius & reflector_box)

universe = openmc.Universe(cells=[fuel_cell, moderator_cell, reflector_cell])
geometry = openmc.Geometry(universe)
geometry.export_to_xml()

# ------------------------
# 3. CONFIGURACIÓN DE SIMULACIÓN
# ------------------------
settings = openmc.Settings()
settings.batches = 50
settings.inactive = 10
settings.particles = 1000
settings.run_mode = "fixed source"

source = openmc.Source()
source.space = openmc.stats.Point((0.0, 0.0, 0.0))
source.energy = openmc.stats.Discrete([1.0e6], [1.0])  # 1 MeV
settings.source = source

settings.export_to_xml()

# ------------------------
# 4. TALLIES
# ------------------------
tallies = openmc.Tallies()

# Tally 1: Flujo por material
flux_tally = openmc.Tally(name="neutron_flux")
flux_tally.filters = [openmc.CellFilter([fuel_cell, moderator_cell, reflector_cell])]
flux_tally.scores = ["flux"]
tallies.append(flux_tally)

# Tally 2: Tasa de fisión en el combustible
fission_tally = openmc.Tally(name="fission_rate")
fission_tally.filters = [openmc.CellFilter([fuel_cell])]
fission_tally.scores = ["fission"]
tallies.append(fission_tally)

# Tally 3: Flujo en malla 3D
mesh = openmc.RegularMesh()
mesh.dimension = [20, 20, 1]
mesh.lower_left = [-6.0, -6.0, -10.0]
mesh.upper_right = [6.0, 6.0, 10.0]

mesh_filter = openmc.MeshFilter(mesh)
mesh_tally = openmc.Tally(name="mesh_flux")
mesh_tally.filters = [mesh_filter]
mesh_tally.scores = ["flux"]
tallies.append(mesh_tally)

tallies.export_to_xml()
