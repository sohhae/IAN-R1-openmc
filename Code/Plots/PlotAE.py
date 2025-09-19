import openmc
import matplotlib.pyplot as plt

sp = openmc.StatePoint("statepoint.200.h5")
tally = sp.get_tally(name="axial_flux_extended")
df = tally.get_pandas_dataframe()

# Mostrar las columnas disponibles
print("Columnas en DataFrame:", df.columns)

# Detectar la columna de z automáticamente
z_col = [col for col in df.columns if "z" in str(col)]
if not z_col:
    raise KeyError(f"No encontré columna de z en: {df.columns}")
z = df[z_col[0]].to_numpy()

flux = df['mean'].to_numpy()

plt.semilogy(z, flux, 'ro-', label="Monte Carlo")
plt.xlabel("z [cm]")
plt.ylabel("ϕ(z) [n/cm²]")
plt.title("Axial distribution of neutrons in the moderator (extended)")
plt.legend()
plt.grid(True, which="both", ls="--")
plt.show()

plt.savefig("Axialdistribution.png", dpi=300)
plt.close()
