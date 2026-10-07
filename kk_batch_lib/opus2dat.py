import sys
import argparse
import numpy as np
import os
import ast

# Function to calculate the moving average
def moving_average(x, N):
    x = np.array(x)
    cumsum = np.cumsum(np.insert(x, 0, 0))
    moving_avg = (cumsum[N:] - cumsum[:-N]) / float(N)

    # Create an array that maintains the original length
    result = np.zeros_like(x)

    # Fill the result with the central moving average values
    result[N//2: -N//2 + 1] = moving_avg

    # Fill the initial and final values with the first and last value of the moving average
    result[:N//2] = moving_avg[0]
    result[-N//2 + 1:] = moving_avg[-1]

    return result.tolist()

from brukeropusreader import read_file

# Function to extend the spectrum to zero with the same spacing
def extend_spectrum_to_zero(wavenumbers, reflectivity):
    min_wavenumber = wavenumbers[0]
    first_reflectivity_value = reflectivity[0]
    
    # Calculate the spacing between the first two wavenumbers
    spacing = wavenumbers[1] - wavenumbers[0]
    
    if min_wavenumber > 0:
        # Create new wavenumbers down to 0 with the same spacing
        new_wavenumbers = np.arange(0, min_wavenumber, spacing).tolist() + wavenumbers
        new_reflectivity = [first_reflectivity_value] * len(np.arange(0, min_wavenumber, spacing).tolist()) + reflectivity
        return new_wavenumbers, new_reflectivity
    else:
        return wavenumbers, reflectivity

# Function to cut the spectrum array based on given limits
def cut_spectrum(wavenumbers, reflectivity, cut_limit1, cut_limit2):
    if (type(cut_limit1) == int) and (type(cut_limit2) == int):
        cut_indexes = []
        
        # Find the index for cut_limit1 only if it is within the range
        if min(wavenumbers) < cut_limit1 < max(wavenumbers):
            for i, wavenumber in enumerate(wavenumbers):
                if wavenumber > cut_limit1:
                    cut_indexes.append(i)
                    break
        else:
            cut_indexes.append(0)  # Start from the beginning if cut_limit1 is out of range
        
        # Find the index for cut_limit2 only if it is within the range
        if min(wavenumbers) < cut_limit2 < max(wavenumbers):
            for i, wavenumber in enumerate(wavenumbers):
                if wavenumber > cut_limit2:
                    cut_indexes.append(i)
                    break
        else:
            cut_indexes.append(len(wavenumbers))  # Go to the end if cut_limit2 is out of range
        
        # Cut only if both indexes are found correctly
        if len(cut_indexes) == 2:
            wavenumbers = wavenumbers[cut_indexes[0]:cut_indexes[1]]
            reflectivity = reflectivity[cut_indexes[0]:cut_indexes[1]]
    return wavenumbers, reflectivity

def convertfile(filename, output_folder, cut_limit1, cut_limit2, moving_average_window, rescaling_value, fill_constant):
    opus_data = read_file(filename)
    
    wavenumbers_reflectivity = np.vstack((opus_data.get_range("AB"), opus_data["AB"]))

    # Sort the matrix with respect to the first row (wavenumbers)
    sorted_index = np.argsort(wavenumbers_reflectivity[0])
    wavenumbers_reflectivity = wavenumbers_reflectivity[:, sorted_index]

    # Separate the arrays
    wavenumbers = wavenumbers_reflectivity[0].tolist()
    reflectivity = wavenumbers_reflectivity[1].tolist()

    # Handle cutting the spectrum
    if (cut_limit1 != "n") and (cut_limit2 != "n"):
        wavenumbers, reflectivity = cut_spectrum(wavenumbers, reflectivity, cut_limit1, cut_limit2)
    elif not (cut_limit1 == "n" or cut_limit2 == "n"):
        print("ERROR::opus2dat: wrong argument for cut_limits!")

    # Handle moving average
    if (moving_average_window != "n"):
        if (type(moving_average_window) == int):
            reflectivity = moving_average(reflectivity, moving_average_window)
        else:
            print("ERROR::opus2dat: wrong argument for moving_average_window!")

    # Handle rescaling
    if (rescaling_value != "n"):
        if (type(rescaling_value) == float or type(rescaling_value) == int):
            reflectivity = (np.array(reflectivity) * rescaling_value).tolist()
        else:
            print("ERROR::opus2dat: wrong argument for rescaling_value!")

    # Handle fill constant
    if (fill_constant == "y"):
        wavenumbers, reflectivity = extend_spectrum_to_zero(wavenumbers, reflectivity)
    elif (fill_constant == "n"):
        pass
    else:
        print("ERROR::opus2dat: wrong argument for fill_low_reflectivity_with_constant_value!")


    # Write the file out again
    new_filename = output_folder + "/" + os.path.splitext(os.path.basename(filename))[0] + ".dat"
    os.makedirs(os.path.dirname(new_filename), exist_ok=True)
    with open(new_filename, 'w') as file:
        for i in range(len(wavenumbers)):
            file.write(f"{wavenumbers[i]} {reflectivity[i]}\n")

def main():
    num_args = len(sys.argv) - 1  # Number of arguments excluding the script name

    if (num_args <= 1) or (num_args > 7):
        print("ERROR::opus2dat needs six arguments!")
    else:
        # Check if sys.argv[3] is a string
        if (sys.argv[3] == "n") or (sys.argv[4] == "n"):
            arg3 = sys.argv[3]
            arg4 = sys.argv[4]
            # Do nothing and proceed to the next logic
            pass
        else:
            arg3 = ast.literal_eval(sys.argv[3])
            arg4 = ast.literal_eval(sys.argv[4])
        # Check if sys.argv[5] is a string
        if sys.argv[5] == "n":
            arg5 = sys.argv[5]
            # Do nothing and proceed to the next logic
            pass
        else:
            arg5 = ast.literal_eval(sys.argv[5])
        if sys.argv[6] == "n":
            arg6 = sys.argv[6]
            # Do nothing and proceed to the next logic
            pass
        else:
            arg6 = ast.literal_eval(sys.argv[6])
            
        convertfile(sys.argv[1], sys.argv[2], arg3, arg4, arg5, arg6, sys.argv[7])

if __name__ == "__main__":
    main()


        
