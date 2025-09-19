import openmc
import matplotlib.pyplot as plt

# Abrir el último statepoint
sp = openmc.StatePoint("statepoint.200.h5")

# Leer tally
tally = sp.get_tally(name="flux_fission_absorption_by_material")
df = tally.get_pandas_dataframe()

# Graficar absorciones por material
materials = df['material'].unique()
abs_values = []
labels = []

for mat in materials:
    sub = df[df['material'] == mat]
    absorption = sub[sub['score'] == 'absorption']['mean'].sum()
    abs_values.append(absorption)
    labels.append(str(mat))

plt.bar(labels, abs_values, color="orange")
plt.xticks(rotation=45, ha="right")
plt.ylabel("Absorptions [n/cm²]")
plt.title("Absorptions by material in IAN-R1")
plt.tight_layout()
plt.show()

plt.savefig("Absorptionplot.png", dpi=300)
plt.close()