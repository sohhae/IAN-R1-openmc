import openmc
import matplotlib.pyplot as plt

sp = openmc.StatePoint("statepoint.200.h5")
tally = sp.get_tally(name="multi_cell_spectrum")
df = tally.get_pandas_dataframe()

for cell_id in df['cell'].unique():
    sub = df[df['cell'] == cell_id]
    plt.step(sub['energy low [eV]'], sub['mean'], where='post', label=f"Cell {cell_id}")

styles = ['-', '--', '-.', ':']
colors = ['r', 'g', 'b', 'k', 'm', 'c']

for i, cell_id in enumerate(df['cell'].unique()):
    sub = df[df['cell'] == cell_id]
    plt.step(
        sub['energy low [eV]'],
        sub['mean'],
        where='post',
        label=f"Cell {cell_id}",
        linestyle=styles[i % len(styles)],
        color=colors[i % len(colors)]
    )

plt.xscale("log")
plt.yscale("log")
plt.xlabel("Energía [eV]")
plt.ylabel("Φ(E) [n/cm²·s·ΔE]")
plt.title("Energy spectra in irradiation channel")
plt.legend()
plt.grid(True, which="both", ls="--")
plt.show()

plt.savefig("spectra_irradiation.png", dpi=300)
plt.close()
