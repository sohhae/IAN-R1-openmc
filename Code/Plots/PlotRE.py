import openmc
import numpy as np
import matplotlib.pyplot as plt

# Cargar resultados
sp = openmc.StatePoint("statepoint.200.h5")
tally = sp.get_tally(name="radial_flux")
df = tally.get_pandas_dataframe()

# Extraer coordenadas x, y y calcular r
x = df[('mesh 3', 'x')].to_numpy()
y = df[('mesh 3', 'y')].to_numpy()
r = np.sqrt(x**2 + y**2)

# Flujo
flux = df[('mean', '')].to_numpy()

# Agrupar por r (porque varios puntos pueden dar el mismo r)
r_unique = np.unique(r)
flux_avg = [flux[r == val].mean() for val in r_unique]

# Graficar
plt.figure()
plt.semilogy(r_unique, flux_avg, 'ro-', label="Monte Carlo")
plt.xlabel("r [cm]")
plt.ylabel("ϕ(r) [n/cm²]")
plt.title("Radial distribution of neutrons in the moderator")
plt.legend()
plt.grid(True, which="both", ls="--")
plt.show()

plt.savefig("RadialExtended", dpi=300)
plt.close()
