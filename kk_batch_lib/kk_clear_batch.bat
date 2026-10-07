@echo off
setlocal enabledelayedexpansion

:: Set the location of executable files
set LIB=kk_batch_lib

:: Read parameters from the configuration file in the LIB directory
for /f "usebackq tokens=1,2 delims==" %%a in ("%LIB%\config.txt") do (
    set "%%a=%%b"
)

:: Prompt the user to confirm deletion of all calculations
echo Sure you want to delete all calculations?
pause

REM Create output file basename without ending underscore

if "%BASENAME:~-1%"=="_" (
    set OUTPUT_BASENAME=%BASENAME:~0,-1%
) else (
    set OUTPUT_BASENAME=%BASENAME%
)

:: Delete files if they exist, otherwise print a message

if exist "Reflectivity_%OUTPUT_BASENAME%.dat" (
    del "Reflectivity_%OUTPUT_BASENAME%.dat"
) else (
    echo File not found: "Reflectivity_%OUTPUT_BASENAME%.dat"
)

if exist "Phaseshift_%OUTPUT_BASENAME%.dat" (
    del "Phaseshift_%OUTPUT_BASENAME%.dat"
) else (
    echo File not found: "Epsilon1_%OUTPUT_BASENAME%.dat"
)

if exist "Sigma1_%OUTPUT_BASENAME%.dat" (
    del "Sigma1_%OUTPUT_BASENAME%.dat"
) else (
    echo File not found: "Sigma1_%OUTPUT_BASENAME%.dat"
)

if exist "Sigma2_%OUTPUT_BASENAME%.dat" (
    del "Sigma2_%OUTPUT_BASENAME%.dat"
) else (
    echo File not found: "Sigma2_%OUTPUT_BASENAME%.dat"
)

if exist "Epsilon1_%OUTPUT_BASENAME%.dat" (
    del "Epsilon1_%OUTPUT_BASENAME%.dat"
) else (
    echo File not found: "Epsilon1_%OUTPUT_BASENAME%.dat"
)

if exist "DAT_plot.png" (
    del "DAT_plot.png"
) else (
    echo File not found: "DAT_plot.png"
)

if exist "RPH_plot.png" (
    del "RPH_plot.png"
) else (
    echo File not found: "RPH_plot.png"
)

if exist "S1_plot.png" (
    del "S1_plot.png"
) else (
    echo File not found: "S1_plot.png"
)

if exist "S2_plot.png" (
    del "S2_plot.png"
) else (
    echo File not found: "S2_plot.png"
)

if exist "E1_plot.png" (
    del "E1_plot.png"
) else (
    echo File not found: "E1_plot.png"
)

if exist "E2_plot.png" (
    del "E2_plot.png"
) else (
    echo File not found: "E2_plot.png"
)

:: Indicate that the task is completed
echo Task Completed!

pause
