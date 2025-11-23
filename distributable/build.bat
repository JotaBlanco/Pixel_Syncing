@echo off
REM Build script for PixelSync on Windows

echo ================================
echo PixelSync Build Script
echo ================================
echo.

REM Check if pyinstaller is installed
pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo PyInstaller not found. Installing...
    pip install pyinstaller
)

REM Check if adb binaries exist
if not exist "adb" (
    echo WARNING: adb folder not found!
    echo Please download Android Platform Tools and extract to adb\ folder
    echo.
    echo Download from: https://developer.android.com/studio/releases/platform-tools
    echo.
    echo Expected structure:
    echo   adb\
    echo     mac\adb
    echo     windows\adb.exe
    echo     linux\adb
    echo.
    pause
)

REM Clean previous builds
echo Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.spec del /q *.spec

REM Build
echo.
echo Building PixelSync executable...
echo.

pyinstaller --name=PixelSync --onefile --console --add-data="adb;adb" pixelsync.py

if %errorlevel% equ 0 (
    echo.
    echo ================================
    echo Build successful!
    echo ================================
    echo.
    echo Executable location: dist\PixelSync.exe
    echo.
    echo To create distributable package:
    echo   1. Create a folder: PixelSync_Package
    echo   2. Copy dist\PixelSync.exe to it
    echo   3. Copy README.md to it
    echo   4. Zip the folder
    echo.
) else (
    echo.
    echo Build failed!
    pause
    exit /b 1
)

pause
