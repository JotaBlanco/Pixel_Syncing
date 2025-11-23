#!/bin/bash
# Build script for PixelSync

echo "================================"
echo "PixelSync Build Script"
echo "================================"
echo ""

# Check if pyinstaller is installed
if ! command -v pyinstaller &> /dev/null; then
    echo "PyInstaller not found. Installing..."
    pip install pyinstaller
fi

# Check if adb binaries exist
if [ ! -d "adb" ]; then
    echo "⚠️  WARNING: adb folder not found!"
    echo "Please download Android Platform Tools and extract to adb/ folder"
    echo ""
    echo "Download from: https://developer.android.com/studio/releases/platform-tools"
    echo ""
    echo "Expected structure:"
    echo "  adb/"
    echo "    mac/adb"
    echo "    windows/adb.exe"
    echo "    linux/adb"
    echo ""
    read -p "Press Enter to continue anyway or Ctrl+C to cancel..."
fi

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build dist *.spec 2>/dev/null

# Build for current platform
echo ""
echo "Building PixelSync executable..."
echo ""

pyinstaller --name=PixelSync \
    --onefile \
    --console \
    --add-data="adb:adb" \
    pixelsync.py

if [ $? -eq 0 ]; then
    echo ""
    echo "================================"
    echo "✅ Build successful!"
    echo "================================"
    echo ""
    echo "Executable location: dist/PixelSync"
    echo ""
    echo "To create distributable package:"
    echo "  1. Create a folder: PixelSync_Package"
    echo "  2. Copy dist/PixelSync to it"
    echo "  3. Copy README.md to it"
    echo "  4. Zip the folder"
    echo ""
else
    echo ""
    echo "❌ Build failed!"
    exit 1
fi
