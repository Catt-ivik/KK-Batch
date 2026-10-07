import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import re

def dat_to_np(filename):
    data = np.genfromtxt(filename, delimiter=' ')
    return data

def plot_spectra_with_color_gradient(file_name_list, temperatures):
    fig, ax = plt.subplots(figsize=(17, 10))

    # Genera un gradiente di colori
    colormap = plt.cm.plasma
    normalize = colors.Normalize(vmin=0, vmax=len(temperatures)-1)

    for i, T in enumerate(temperatures):
        filename = 'Co3SnInS2_Merged_smooth_cut_Ellb_' + str(T) + 'K.S12'
        spectrum = dat_to_np(filename)

        # Assegna il colore in base al gradiente
        color = colormap(normalize(i))

        # Plotta lo spettro con il colore assegnato
        ax.plot(spectrum[:, 0], spectrum[:, 1], color=color)

    # Aggiungi una cornice completa al grafico
    ax.set_frame_on(True)

    # Aggiungi una griglia principale
    ax.grid(True, linestyle='-', linewidth=0.5)

    # Aggiungi una subgrid tratteggiata
    ax.minorticks_on()
    ax.grid(which='minor', linestyle=':', linewidth=0.5)

    # Aggiungi la barra del colore per indicare il gradiente
    sm = plt.cm.ScalarMappable(cmap=colormap, norm=normalize)
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax)
    cbar.set_ticks(np.linspace(0, len(temperatures)-1, len(temperatures)))
    cbar.set_ticklabels(temperatures)
    cbar.set_label('Temperature (K)')

    # Aggiungi titoli agli assi
    ax.set_xlabel('Inverse Wavelength [1/cm]')
    ax.set_ylabel('Reflectance [arb. units]')

    # Esporta il grafico in un file
    plt.savefig('spectrum_plot.png', dpi=300, bbox_inches='tight')

    plt.show()

# Definisci il percorso del file di log
log_file_path = "S12_file_list.txt"

# Inizializza una lista vuota per memorizzare i nomi dei file
file_names = []

# Inizializza una lista vuota per memorizzare le temperature
temperatures = []

# Espressione regolare per trovare la temperatura nel nome del file
pattern = r"(\d+)K"

# Leggi il file di log e memorizza i nomi dei file nella lista
with open(log_file_path, 'r') as file:
    for line in file:
        file_names.append(line.strip())
        match = re.search(pattern, line)
        if match:
            temperature = int(match.group(1))
            temperatures.append(temperature)

# Converti le temperature in numeri interi
temperatures = [int(temperature) for temperature in temperatures]

# Ordina le temperature in ordine crescente
temperatures.sort()

plot_spectra_with_color_gradient(file_names, temperatures)



