import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

def dat_to_np(filename):
    data = np.genfromtxt(filename, delimiter=' ')
    return data

def plot_spectra_with_color_gradient(temperatures):
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

temperatures = (10, 40, 100, 140, 200, 240, 300)
plot_spectra_with_color_gradient(temperatures)



