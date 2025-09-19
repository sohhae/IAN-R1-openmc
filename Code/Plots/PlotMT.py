import openmc
import matplotlib.pyplot as plt

# Abrir statepoint
sp = openmc.StatePoint("statepoint.200.h5")
tally = sp.get_tally(name="xy_mesh_flux")

# Convertir a DataFrame
df = tally.get_pandas_dataframe()

# Reshape (80x80) para el mapa
flux = df['mean'].to_numpy().reshape((80, 80))

plt.imshow(flux, origin='lower', cmap='inferno',
           extent=[-50, 50, -50, 50])
plt.colorbar(label="Neutron flux [n/cm²·s]")
plt.contour(flux, colors='black', linewidths=0.5, extent=[-50, 50, -50, 50])
plt.xlabel("X [cm]")
plt.ylabel("Y [cm]")
plt.title("Spatial distribution of flow (XY)")
plt.savefig("flux_map_xy.png", dpi=300)
plt.close()
