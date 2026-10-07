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

if exist "Epsilon2_%OUTPUT_BASENAME%.dat" (
    del "Epsilon2_%OUTPUT_BASENAME%.dat"
) else (
    echo File not found: "Epsilon2_%OUTPUT_BASENAME%.dat"
)

if exist "Plot_Reflectivity_%OUTPUT_BASENAME%.png" (
    del "Plot_Reflectivity_%OUTPUT_BASENAME%.png"
) else (
    echo File not found: "Plot_Reflectivity_%OUTPUT_BASENAME%.png"
)

if exist "Plot_Phaseshift_%OUTPUT_BASENAME%.png" (
    del "Plot_Phaseshift_%OUTPUT_BASENAME%.png"
) else (
    echo File not found: "Plot_Phaseshift_%OUTPUT_BASENAME%.png"
)

if exist "Plot_Sigma1_%OUTPUT_BASENAME%.png" (
    del "Plot_Sigma1_%OUTPUT_BASENAME%.png"
) else (
    echo File not found: "Plot_Sigma1_%OUTPUT_BASENAME%.png"
)

if exist "Plot_Sigma2_%OUTPUT_BASENAME%.png" (
    del "Plot_Sigma2_%OUTPUT_BASENAME%.png"
) else (
    echo File not found: "Plot_Sigma2_%OUTPUT_BASENAME%.png"
)

if exist "Plot_Epsilon1_%OUTPUT_BASENAME%.png" (
    del "Plot_Epsilon1_%OUTPUT_BASENAME%.png"
) else (
    echo File not found: "Plot_Epsilon1_%OUTPUT_BASENAME%.png"
)

if exist "Plot_Epsilon2_%OUTPUT_BASENAME%.png" (
    del "Plot_Epsilon2_%OUTPUT_BASENAME%.png"
) else (
    echo File not found: "Plot_Epsilon2_%OUTPUT_BASENAME%.png"
)

:: Indicate that the task is completed
echo Task Completed!

pause
