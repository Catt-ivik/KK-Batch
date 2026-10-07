import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import re
import sys

def dat_to_np(filename):
    data = np.genfromtxt(filename, delimiter=' ')
    return data

def kk_header(free_electron_crossover_frequency, high_frequencies_extrapolation_grade, dc_extrapolation):

    kk_header_string = "Calculated from reflectivity spectra through Kramers-Kronig transformation, with\n-> Free-electron crossover frequency: " + str(free_electron_crossover_frequency + "rad " + "\n-> High frequencies have been extrapolated as omega^-" + str(high_frequencies_extrapolation_grade) + "\n-> DC conductivity has been ")
    
    match dc_extrapolation:
        case "0":
            kk_header_string += "assumed constant"
        case "-1":
            kk_header_string += "extrapolated as metallic"
        case "-2":
            kk_header_string += "extrapolated as a two fluid model"
        case "-3":
            kk_header_string += "extrapolated as marginal Fermi liquid"
        case "-4":
            kk_header_string += "extrapolated as a superconductor"
        case "-5":
            kk_header_string += "taken from a parameter file"
        case _:
            kk_header_string += "fixed, with value sigma_DC=" + str(dc_extrapolation) + "Ohm^-1cm^-1"
        

def plot_and_export(file_name_list, temperatures, free_electron_crossover_frequency, high_frequencies_extrapolation_grade, dc_extrapolation, output_filename):

    kk_header_string = "Calculated from reflectivity spectra through Kramers-Kronig transformation, with\n-> Free-electron crossover frequency: " + str(free_electron_crossover_frequency + "rad " + "\n-> High frequencies have been extrapolated as omega^-" + str(high_frequencies_extrapolation_grade) + "\n-> DC conductivity has been ")
    
    match dc_extrapolation:
        case "0":
            kk_header_string += "assumed constant"
        case "-1":
            kk_header_string += "extrapolated as metallic"
        case "-2":
            kk_header_string += "extrapolated as a two fluid model"
        case "-3":
            kk_header_string += "extrapolated as marginal Fermi liquid"
        case "-4":
            kk_header_string += "extrapolated as a superconductor"
        case "-5":
            kk_header_string += "taken from a parameter file"
        case _:
            kk_header_string += "fixed, with value sigma_DC=" + str(dc_extrapolation) + "Ohm^-1cm^-1"
        

    fig, ax = plt.subplots(figsize=(17, 10))

    # Genera un gradiente di colori
    colormap = plt.cm.plasma
    normalize = colors.Normalize(vmin=0, vmax=len(temperatures)-1)

    spectrum_0 = dat_to_np(file_name_list[0])
    spectra = np.empty((0, len(spectrum_0[:, 0])))

    for i, T in enumerate(temperatures):
        
        filename = file_name_list[i]
        spectrum = dat_to_np(filename)

        if i == 0:
            spectra = np.vstack([spectra, spectrum[:, 0]])

        spectra = np.vstack([spectra, spectrum[:, 2]])

        # Assegna il colore in base al gradiente
        color = colormap(normalize(i))

        # Plotta lo spettro con il colore assegnato
        ax.plot(spectrum[:, 0], spectrum[:, 2], color=color)

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
    ax.set_xlabel('Wavenumber (1/cm)')
    ax.set_ylabel('Epsilon2')

    # Esporta il grafico in un file
    plt.savefig('Plot_'+output_filename+'.png', dpi=300, bbox_inches='tight')

    header = "DIELECTRIC FUNCTION (Imaginary part)\n\n" + kk_header_string + "\n\n"
    
    with open(output_filename+'.dat', 'w') as file:
        file.write(header)

    indexes = 'Wavenumber(1/cm)'
    for T in temperatures:
        new_temperature = " " + str(T) + "K"
        indexes += new_temperature
    with open(output_filename + ".dat", "a") as file:
        file.write(indexes + "\n")


        
        for j in range(len(spectrum_0[:, 0])):
            for i in range(len(temperatures)+1):
                if i == len(temperatures):
                    file.write(str(spectra[i][j]))
                else:
                    file.write(str(spectra[i][j]) + " ")
            file.write("\n")

    

def main():
    
    # Definisci il percorso del file di log
    log_file_name = sys.argv[1]

    free_electron_crossover_frequency = sys.argv[2]
    high_frequencies_extrapolation_grade = sys.argv[3]
    dc_extrapolation = sys.argv[4]
    output_filename = sys.argv[5]

    # Inizializza una lista vuota per memorizzare i nomi dei file
    file_names = []

    # Inizializza una lista vuota per memorizzare le temperature
    temperatures = []

    # Espressione regolare per trovare la temperatura nel nome del file
    pattern = r"(\d+)K"

    # Leggi il file di log e memorizza i nomi dei file nella lista
    with open(log_file_name, 'r') as file:
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

    plot_and_export(file_names, temperatures, free_electron_crossover_frequency, high_frequencies_extrapolation_grade, dc_extrapolation, output_filename)


if __name__ == "__main__":
    main()
