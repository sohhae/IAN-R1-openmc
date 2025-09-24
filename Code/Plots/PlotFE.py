import openmc
import matplotlib.pyplot as plt

# === Abrir statepoint ===
sp = openmc.StatePoint("/root/openmc_project/Results/statepoint.200.h5")
tally = sp.get_tally(name="multi_cell_spectrum")
df = tally.get_pandas_dataframe()

# === Filtrar solo las celdas 14, 15 y 16 ===
cells_to_plot = [14, 15, 16]
df = df[df['cell'].isin(cells_to_plot)]

# === Estilos y colores ===
styles = ['-', '--', '-.']
colors = ['r', 'g', 'b']

# === Graficar ===
for i, cell_id in enumerate(cells_to_plot):
    sub = df[df['cell'] == cell_id]
    plt.step(
        sub['energy low [eV]'],
        sub['mean'],
        where='post',
        label=f"Cell {cell_id}",
        linestyle=styles[i % len(styles)],
        color=colors[i % len(colors)]
    )

# === Configuración ===
plt.xscale("log")
plt.yscale("log")
plt.xlabel("Energía [eV]")
plt.ylabel("Φ(E) [n/cm²·s·ΔE]")
plt.title("Energy spectra in irradiation channel")
plt.legend()
plt.grid(True, which="both", ls="--")

# === Guardar y mostrar ===
plt.savefig("spectra_irradiation_cells_1.png", dpi=300)
plt.show()
plt.close()
