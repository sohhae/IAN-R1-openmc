# PlotZ.py
import openmc
import matplotlib.pyplot as plt
import numpy as np

# === Cargar resultados ===
sp = openmc.StatePoint("statepoint.200.h5")

# === Obtener tally axial ===
tally = sp.get_tally(name="z_mesh_flux")
df = tally.get_pandas_dataframe()

print("Columnas disponibles:", df.columns)

# === Extraer coordenadas z y flujo ===
z_bins = df[('mesh 2', 'z')].to_numpy()  # depende de cómo OpenMC lo exporte (ajustar 'mesh 2')
flux = df['mean'].to_numpy()

# Para centrar cada bin en z
# Como tienes 80 bins entre -50 y 50 cm:
z_centers = np.linspace(-50, 50, len(flux))

# === Graficar ===
plt.figure(figsize=(6,5))
plt.semilogy(z_centers, flux, 'ro-', label="Monte Carlo")

plt.xlabel("z [cm]")
plt.ylabel(r"$\phi(z)$ [n/cm$^2$]")
plt.title("Axial distribution of neutrons in the moderator")
plt.legend()
plt.grid(True, which="both", ls="--")

plt.savefig("axial_flux.png", dpi=300)
plt.close()

