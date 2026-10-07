@echo off
setlocal enabledelayedexpansion

REM Set LIB directly in the batch script
set LIB=kk_batch_lib

REM Check if the LIB directory and config.txt file exist
if not exist "%LIB%" (
    echo The directory %LIB% does not exist.
    exit /b 1
)

if not exist "%LIB%\config.txt" (
    echo The configuration file %LIB%\config.txt does not exist.
    exit /b 1
)

REM Read parameters from the configuration file in the LIB directory
for /f "usebackq tokens=1,2 delims==" %%a in ("%LIB%\config.txt") do (
    echo Reading %%a=%%b
    set "%%a=%%b"
)

REM Create output file basename without ending underscore

if "%BASENAME:~-1%"=="_" (
    set OUTPUT_BASENAME=%BASENAME:~0,-1%
) else (
    set OUTPUT_BASENAME=%BASENAME%
)

set shouldDelete=0

if exist "Reflectivity_%OUTPUT_BASENAME%.dat" set shouldDelete=1
if exist "Phaseshift_%OUTPUT_BASENAME%.dat" set shouldDelete=1
if exist "Sigma1_%OUTPUT_BASENAME%.dat" set shouldDelete=1
if exist "Sigma2_%OUTPUT_BASENAME%.dat" set shouldDelete=1
if exist "Epsilon1_%OUTPUT_BASENAME%.dat" set shouldDelete=1
if exist "Epsilon2_%OUTPUT_BASENAME%.dat" set shouldDelete=1
if exist "Plot_Reflectivity_%OUTPUT_BASENAME%.png" set shouldDelete=1
if exist "Plot_Phaseshift_%OUTPUT_BASENAME%.png" set shouldDelete=1
if exist "Plot_Sigma1_%OUTPUT_BASENAME%.png" set shouldDelete=1
if exist "Plot_Sigma2_%OUTPUT_BASENAME%.png" set shouldDelete=1
if exist "Plot_Epsilon1_%OUTPUT_BASENAME%.png" set shouldDelete=1
if exist "Plot_Epsilon2_%OUTPUT_BASENAME%.png" set shouldDelete=1

if %shouldDelete%==1 (

	echo.
	echo Are you sure you want to delete previous calculations?
	pause

	del "Reflectivity_%OUTPUT_BASENAME%.dat"		
	del "Phaseshift_%OUTPUT_BASENAME%.dat"
	del "Sigma1_%OUTPUT_BASENAME%.dat"
	del "Sigma2_%OUTPUT_BASENAME%.dat"
	del "Epsilon1_%OUTPUT_BASENAME%.dat"
	del "Epsilon2_%OUTPUT_BASENAME%.dat"
	del "Plot_Reflectivity_%OUTPUT_BASENAME%.png"
	del "Plot_Phaseshift_%OUTPUT_BASENAME%.png"
	del "Plot_Sigma1_%OUTPUT_BASENAME%.png"
	del "Plot_Sigma2_%OUTPUT_BASENAME%.png"
	del "Plot_Epsilon1_%OUTPUT_BASENAME%.png"
	del "Plot_Epsilon2_%OUTPUT_BASENAME%.png"
) else (
	pause
)

echo.


set "LOG_FILE_DAT=DAT_file_list.txt"
set "LOG_FILE_RPH=RPH_file_list.txt"
set "LOG_FILE_S12=S12_file_list.txt"
set "LOG_FILE_E12=E12_file_list.txt"

REM Create temporary copy of Conductivity file
if %DC_EXTRAPOLATION%==-5 (
    if exist "%DC_CONDUCTIVITY_LIST_FILE%" (
        copy "%DC_CONDUCTIVITY_LIST_FILE%" "%DC_CONDUCTIVITY_LIST_FILE%_temp"
    ) else (
            echo The file %DC_CONDUCTIVITY_LIST_FILE%_temp does not exist.
            exit /b 1
        )
)

REM Process files with .0 extension
for %%X in (%BASENAME%*.0) do (
    echo Operating %%X...
    "%LIB%/opus2dat.py" %%X "." %CUT_LIMIT1% %CUT_LIMIT2% %AVERAGE_MOVING_WINDOW% %RESCALING_VALUE% %FILL_LOW_REFLECTIVITY_WITH_CONSTANT_VALUE%
)

REM Process files with .dat extension
for %%Y in (%BASENAME%*.dat) do (
    echo Operating %%Y...

    REM If DC_EXTRAPOLATION is -5, read the first value from the file and update DC_EXTRAPOLATION
    if "%DC_EXTRAPOLATION%"=="-5" (
        set /p DC_EXTRAPOLATION_TEMP=< %DC_CONDUCTIVITY_LIST_FILE%_temp
        echo DC-Conductivity set to !DC_EXTRAPOLATION_TEMP!

        "%LIB%/eliminate_first_line.py" %DC_CONDUCTIVITY_LIST_FILE%_temp

        "%LIB%/kkold" %%Y "/WA%FREE_ELECTRON_CROSSOVER_FREQUENCY%" "/D%HIGH_FREQUENCIES_EXTRAPOLATION_GRADE%" "/C!DC_EXTRAPOLATION_TEMP!" /q
    ) else (
        "%LIB%/kkold" %%Y "/WA%FREE_ELECTRON_CROSSOVER_FREQUENCY%" "/D%HIGH_FREQUENCIES_EXTRAPOLATION_GRADE%" "/C%DC_EXTRAPOLATION%" /q
    )
    echo %%Y >> "%LOG_FILE_DAT%"
)

REM eliminate temporary copy of Conductivity file
if exist "%DC_CONDUCTIVITY_LIST_FILE%_temp" (
	del "%DC_CONDUCTIVITY_LIST_FILE%_temp"
)


REM Calculate conductivity and dielectric function
for %%Z in (%BASENAME%*.RPH) do (
    echo Operating %%Z...
    "%LIB%/rph2s" %%Z
    "%LIB%/rph2e" %%Z
)

REM Modify RPH files
for %%Z in (%BASENAME%*.RPH) do (
    "%LIB%/modify_RPH.py" %%Z
    echo %%Z >> "%LOG_FILE_RPH%"
)

REM Modify S12 files
for %%W in (%BASENAME%*.S12) do (
    echo Modifying %%W...
    "%LIB%/modify_S12.py" %%W
    echo %%W >> "%LOG_FILE_S12%"
)

REM Modify E12 files
for %%W in (%BASENAME%*.E12) do (
    echo Modifying %%W...
    "%LIB%/modify_E12.py" %%W
    echo %%W >> "%LOG_FILE_E12%"
)

REM Run plotting scripts
echo Plotting and exporting results...
"%LIB%\Plot_and_export_DAT.py" "%LOG_FILE_DAT%" "%FREE_ELECTRON_CROSSOVER_FREQUENCY%" "%HIGH_FREQUENCIES_EXTRAPOLATION_GRADE%" "%DC_EXTRAPOLATION%" "Reflectivity_%OUTPUT_BASENAME%"
"%LIB%\Plot_and_export_RPH.py" "%LOG_FILE_RPH%" "%FREE_ELECTRON_CROSSOVER_FREQUENCY%" "%HIGH_FREQUENCIES_EXTRAPOLATION_GRADE%" "%DC_EXTRAPOLATION%" "Phaseshift_%OUTPUT_BASENAME%"
"%LIB%\Plot_and_export_S1.py" "%LOG_FILE_S12%" "%FREE_ELECTRON_CROSSOVER_FREQUENCY%" "%HIGH_FREQUENCIES_EXTRAPOLATION_GRADE%" "%DC_EXTRAPOLATION%" "Sigma1_%OUTPUT_BASENAME%"
"%LIB%\Plot_and_export_S2.py" "%LOG_FILE_S12%" "%FREE_ELECTRON_CROSSOVER_FREQUENCY%" "%HIGH_FREQUENCIES_EXTRAPOLATION_GRADE%" "%DC_EXTRAPOLATION%" "Sigma2_%OUTPUT_BASENAME%"
"%LIB%\Plot_and_export_E1.py" "%LOG_FILE_E12%" "%FREE_ELECTRON_CROSSOVER_FREQUENCY%" "%HIGH_FREQUENCIES_EXTRAPOLATION_GRADE%" "%DC_EXTRAPOLATION%" "Epsilon1_%OUTPUT_BASENAME%"
"%LIB%\Plot_and_export_E2.py" "%LOG_FILE_E12%" "%FREE_ELECTRON_CROSSOVER_FREQUENCY%" "%HIGH_FREQUENCIES_EXTRAPOLATION_GRADE%" "%DC_EXTRAPOLATION%" "Epsilon2_%OUTPUT_BASENAME%"

echo Removing temporary files...

REM Remove single .dat files
for %%X in (%BASENAME%*.dat) do del "%%X"

REM Remove single .rph files
for %%Y in (%BASENAME%*.RPH) do del "%%Y"

REM Remove single .s12 files
for %%Z in (%BASENAME%*.S12) do del "%%Z"

REM Remove single .e12 files
for %%W in (%BASENAME%*.E12) do del "%%W"

REM Move log files to their respective directories
del "%LOG_FILE_DAT%"
del "%LOG_FILE_RPH%"
del "%LOG_FILE_S12%"
del "%LOG_FILE_E12%"

echo Task Completed!

pause


