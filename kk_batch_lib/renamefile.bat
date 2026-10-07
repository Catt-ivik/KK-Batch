@echo off
setlocal enabledelayedexpansion

rem Directory containing the files
set "dir=."

rem Loop through all the files with the pattern Co3SnInS2_Merged_raw_Ellb_*K.0
for %%f in (%dir%\Co3SnInS2_Merged_raw_Ellb_*K.0) do (
    rem Get the full path of the file
    set "filepath=%%f"
    
    rem Extract the filename without extension
    set "filename=%%~nxf"
    
    rem Replace "raw_Ellb_" with "smooth_cut_Ellb_" in the filename
    set "newfilename=!filename:raw_Ellb_=smooth_cut_Ellb_!"
    
    rem Rename the file
    ren "%%f" "!newfilename!"
)

echo Done!
pause

