KK-Batch
04.11.2023 - Luca Malucelli (luca.malucelli@gmail.com)

Batch program for calculating optic conductivity and dielectric function from Bruker Opus spectra, using datan software (more on http://www.phys.ufl.edu/~tanner/datan.html) and brukeropusreader (https://github.com/qedsoftware/brukeropusreader).

Python and some Python libraries as brukeropusreader should be installed. Follow the errors and install what you need! Important: Python has to be added to the ambient variables on your pc.
(Should be easily done with a quick Google-first-link-opening search).


1. Copy the files kk_batch.bat and kk_clear_batch.bat and the directory kk_batch_lib in the same directory that contains your .0 Opus files (They must be .0!)
2. Open the file config.txt in the directory kk_batch_lib and set the parameters:
	- BASENAME 		--> 	Prefix of your files. Es: "FeSn_100K.0" has prefix "FeSn_". This will rename all future files and directories accordingly.
					All the files you want to process must have the same prefix! If BASENAME is set as empty, all .0 files will be processed
					and no prefix will be set for files and directories names.
	- CUT_LIMIT(1/2)	-->	Low and high limits for cutting spectra in terms of inverse centimeters. Can also be out of the wavenumbers range,
					so that the spectra won't be cut. Another option is to seth both limits as "n", then there won't be any cutting either.
	- AVERAGE_MOVING_WINDOW	-->	If no moving average is to be operated, this value can be set as "n". Else, the length of the window of the moving average
					has to be given. (It is good to do it, so that the first and last values of the spectra will be constant and there isn't the danger
					that the high and low extrapolation start at a noise peak/valley.
	- FREE_ELECTRON_	-->	Frequency at which free electron behaviour begins.
	  CROSSOVER_FREQUENCY
	- HIGH_FREQUENCIES_	-->	Grade of extrapolation for high frequencies, with a power law a+b1/w.... This means that negative grades will give a power law of type a+bw...
	  EXTRAPOLATION_GRADE

	- DC_EXTRAPOLATION	-->	Low frequency extrapolation between: 	known conductivity value (in Ohm^-1cm^-1), 0 (constant reflectance assumed), -1 (metallic),
										-2 (two-fluid model), -3 (marginal Fermi liquid), -4 (superconducting), -5 (parameter file, to be
										specified in DC_CONDUCTIVITY_LIST_FILE).
	- DC_CONDUCTIVITY_
	  LIST_FILE		-->	Parameter file name with path (best thing is putting the parameter file in the same folder as kk_batch program and then leave the file's
					path out of games. The file has to be built like the DC_conductivity_list_file_example.txt contained in /kk_batch_lib.
					Attention! For every .0 file, there MUST be a line in DC_conductivity_list_file_example.txt.
	- RESCALING_VALUE	-->	If the spectra has to be rescaled, the scaling value can be inserted here. The reflectivity spectra will be multiplied by this value.
					If no rescaling is needed, this value can be set as "n"
	- FILL_LOW_REFLECTIVITY_
	  WITH_CONSTANT_VALUE	-->	If set to "y", the low-energy part of the reflectivity spectra down to wavenumber 0 will be filled up with values equal to the first
					value of the spectra. It is good to use the AVERAGE_MOVING_WINDOW over described, if this filling has to be performed.
					If set to "n", the filling will be turned out.


3. Launch the program kk_batch.bat
4. For retrying, you can eliminate all the created files and directories by launching the program kk_clear_batch

The given plots represent the modified reflectivity with cuts and moving average, the phase-shift of the reflectivity and the real and imaginary parts of the
conductivity (Sigma1 and Sigma2) and dielectric function (Epsilon1 and Epsilon2). The corresponding data is to be found in the corresponding .dat files.