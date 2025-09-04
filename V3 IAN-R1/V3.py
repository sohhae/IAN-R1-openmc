import openmc

# ————— 1. MATERIALES —————
fuel = openmc.Material(name="TRIGA_LEU")
fuel.add_element("U", 1.0, enrichment=19.7)
fuel.add_element("Zr", 1.0)
fuel.add_element("H", 1.6)
fuel.set_density("g/cm3", 6.5)

moderator = openmc.Material(name="Light_Water")
moderator.add_nuclide("H1", 2.0)
moderator.add_nuclide("O16", 1.0)
moderator.set_density("g/cm3", 1.0)
moderator.add_s_alpha_beta("c_H_in_H2O")

graphite = openmc.Material(name="Graphite")
graphite.add_element("C", 1.0)
graphite.set_density("g/cm3", 1.7)

materials = openmc.Materials([fuel, moderator, graphite])
materials.export_to_xml()

# ————— 2. GEOMETRÍA —————

# Superficies para la caja del núcleo (6 lados)
x_min = openmc.XPlane(x0=-3.5, boundary_type='reflective')
x_max = openmc.XPlane(x0=+3.5, boundary_type='reflective')
y_min = openmc.YPlane(y0=-3.5, boundary_type='reflective')
y_max = openmc.YPlane(y0=+3.5, boundary_type='reflective')
z_min = openmc.ZPlane(z0=-5.0, boundary_type='reflective')
z_max = openmc.ZPlane(z0=+5.0, boundary_type='reflective')

# Región total cerrada
core_region = +x_min & -x_max & +y_min & -y_max & +z_min & -z_max

# Pin TRIGA
pin_fuel = openmc.ZCylinder(r=0.4)
fuel_cell = openmc.Cell(fill=fuel, region=-pin_fuel)
mod_cell = openmc.Cell(fill=moderator, region=+pin_fuel)
pin_univ = openmc.Universe(cells=[fuel_cell, mod_cell])

# Rejilla 7x7 de pines
lattice = openmc.RectLattice()
lattice.lower_left = (-3.5, -3.5)
lattice.pitch = (1.0, 1.0)
lattice.universes = [[pin_univ]*7 for _ in range(7)]

# Celda principal del núcleo, encerrada completamente
core_cell = openmc.Cell(fill=lattice, region=core_region)

# Universo raíz y geometría
root_universe = openmc.Universe(cells=[core_cell])
geometry = openmc.Geometry(root_universe)
geometry.export_to_xml()


# ————— 3. CONFIGURACIÓN eigenvalue —————
settings = openmc.Settings()
settings.run_mode = "eigenvalue"
settings.batches = 200
settings.inactive = 20
settings.particles = 2000
settings.export_to_xml()

# ————— 4. TALLIES —————
tallies = openmc.Tallies()

# Flujo en celda de combustible
flux = openmc.Tally(name="flux")
flux.filters = [openmc.CellFilter([fuel_cell])]
flux.scores = ["flux"]
tallies.append(flux)

# Fisión en combustible
fiss = openmc.Tally(name="fission")
fiss.filters = [openmc.CellFilter([fuel_cell])]
fiss.scores = ["fission"]
tallies.append(fiss)

# Malla de flujo
mesh = openmc.RegularMesh()
mesh.dimension = [20, 20, 1]
mesh.lower_left = [-6, -6, -10]
mesh.upper_right = [6, 6, 10]
mesh_t = openmc.Tally(name="mesh_flux")
mesh_t.filters = [openmc.MeshFilter(mesh)]
mesh_t.scores = ["flux"]
tallies.append(mesh_t)

tallies.export_to_xml()

openmc.run()