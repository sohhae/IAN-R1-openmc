# PlotRF.py
import openmc
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# === Abrir statepoint ===
sp = openmc.StatePoint("statepoint.200.h5")

# === Obtener tally radial ===
tally = sp.get_tally(name="radial_flux")
df = tally.get_pandas_dataframe()

print("Columnas disponibles:", df.columns)

# === Extraer radios y flujo ===
# Aquí 'mesh 3' es el nombre automático de tu malla cilíndrica
r = df[('mesh 3', 'x')].to_numpy()
flux = df['mean'].to_numpy()

# === Ajuste doble exponencial ===
def func(r, a, b, c, d):
    return a*np.exp(-b*r) + c*np.exp(-d*r)

popt, _ = curve_fit(func, r, flux, maxfev=10000)

# === Graficar ===
plt.figure(figsize=(6,5))
plt.semilogy(r, flux, 'ro', label="Monte Carlo")  # puntos simulados
plt.semilogy(r, func(r, *popt), 'b--', label="Función ajustada")  # curva ajustada

# Mostrar la ecuación ajustada en la gráfica
eq = fr"$\phi(r) = {popt[0]:.3e} e^{{-{popt[1]:.3f} r}} + {popt[2]:.3e} e^{{-{popt[3]:.3f} r}}$"
plt.text(0.5, 0.2, eq, transform=plt.gca().transAxes, fontsize=9, color="blue")

plt.xlabel("r [cm]")
plt.ylabel(r"$\phi(r)$ [n/cm$^2$]")
plt.title("Radial distribution of neutrons in the moderator")
plt.legend()
plt.grid(True, which="both", ls="--")

# Guardar la figura
plt.savefig("radial_flux.png", dpi=300)
plt.close()


