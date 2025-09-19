import openmc
import matplotlib.pyplot as plt

sp = openmc.StatePoint("statepoint.200.h5")
tally = sp.get_tally(name="spectrum_by_material")
df = tally.get_pandas_dataframe()

for mat_id in df['material'].unique():
    sub = df[df['material'] == mat_id]
    plt.step(sub['energy low [eV]'], sub['mean'], where='post', label=f"Material {mat_id}")

plt.xscale("log")
plt.yscale("log")
plt.xlabel("Energía [eV]")
plt.ylabel("Φ(E) [n/cm²·s·ΔE]")
plt.title("Energy spectra by material")
plt.legend()
plt.grid(True, which="both", ls="--")
plt.show()

plt.savefig("SpectrumMaterials", dpi=300)
plt.close()