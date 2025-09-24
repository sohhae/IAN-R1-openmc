import openmc
import matplotlib.pyplot as plt
import numpy as np

# === Abrir statepoint ===
sp = openmc.StatePoint("/root/openmc_project/Results/statepoint.200.h5")

# === Obtener tally con fisiones y absorciones ===
tally = sp.get_tally(name="flux_fission_absorption_by_material")
df = tally.get_pandas_dataframe()

materials = df['material'].unique()
f_values = []
labels = []

for mat in materials:
    sub = df[df['material'] == mat]
    fission = sub[sub['score'] == 'fission']['mean'].sum()
    absorption = sub[sub['score'] == 'absorption']['mean'].sum()

    if fission > 0:  # solo materiales con fisión
        f_eff = fission / absorption if absorption > 0 else 0.0
        f_values.append(f_eff)
        labels.append(f"Material {mat}")

# === Graficar ===
fig, ax = plt.subplots(figsize=(6,5))

bars = ax.bar(labels, f_values, color="royalblue", edgecolor="black")

# Añadir valores encima de cada barra
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 0.02,
            f"{height:.2f}", ha='center', va='bottom', fontsize=10, fontweight="bold")

ax.set_ylabel("f-effective (Fission / Absorption)")
ax.set_title("f-effective by material in IAN-R1", fontsize=13, fontweight="bold")
ax.set_ylim(0, 1)  # rango de 0 a 1 para claridad
ax.grid(True, axis="y", ls="--", alpha=0.7)

plt.tight_layout()
plt.savefig("f_effective_by_material_improved.png", dpi=300)
plt.show()

