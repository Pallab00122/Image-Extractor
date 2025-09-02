@echo off
echo Image Capture and Text Extraction Tool
echo ======================================
echo.

if "%~1"=="" (
    echo Usage: run_capture.bat ^<image_path_or_gdrive_link^>
    echo.
    echo Examples:
    echo   run_capture.bat image.png
    echo   run_capture.bat https://drive.google.com/file/d/YOUR_FILE_ID/view
    echo.
    pause
    exit /b 1
)

echo Processing: %1
echo.
python capture.py "%1"
echo.
pause

