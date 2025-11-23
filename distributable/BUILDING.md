# Building PixelSync

This guide explains how to build standalone executables of PixelSync for distribution.

## Prerequisites

1. **Python 3.7+** installed
2. **PyInstaller** (`pip install pyinstaller`)
3. **Android Platform Tools** (adb) downloaded

## Step 1: Download ADB

Download Android Platform Tools for all platforms:

- **Official source**: https://developer.android.com/studio/releases/platform-tools

### For macOS:
```bash
# Download and extract
curl -o platform-tools-latest-darwin.zip https://dl.google.com/android/repository/platform-tools-latest-darwin.zip
unzip platform-tools-latest-darwin.zip
mkdir -p adb/mac
cp platform-tools/adb adb/mac/
chmod +x adb/mac/adb
```

### For Windows:
```powershell
# Download from https://dl.google.com/android/repository/platform-tools-latest-windows.zip
# Extract and copy adb.exe, AdbWinApi.dll, AdbWinUsbApi.dll to adb/windows/
```

### For Linux:
```bash
# Download and extract
wget https://dl.google.com/android/repository/platform-tools-latest-linux.zip
unzip platform-tools-latest-linux.zip
mkdir -p adb/linux
cp platform-tools/adb adb/linux/
chmod +x adb/linux/adb
```

### Expected folder structure:
```
PixelSync_Distributable/
├── adb/
│   ├── mac/
│   │   └── adb
│   ├── windows/
│   │   ├── adb.exe
│   │   ├── AdbWinApi.dll
│   │   └── AdbWinUsbApi.dll
│   └── linux/
│       └── adb
├── pixelsync.py
├── pixel_sync_core.py
├── config_manager.py
└── ...
```

## Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 3: Build

### On macOS:
```bash
./build.sh
```

This creates `dist/PixelSync` executable.

### On Windows:
```cmd
build.bat
```

This creates `dist\PixelSync.exe` executable.

### On Linux:
```bash
chmod +x build.sh
./build.sh
```

## Step 4: Create Distribution Package

### For macOS:
```bash
mkdir PixelSync_macOS
cp dist/PixelSync PixelSync_macOS/
cp README.md PixelSync_macOS/
zip -r PixelSync_macOS.zip PixelSync_macOS/
```

### For Windows:
```cmd
mkdir PixelSync_Windows
copy dist\PixelSync.exe PixelSync_Windows\
copy README.md PixelSync_Windows\
# Use 7-Zip or Windows Explorer to create PixelSync_Windows.zip
```

## Step 5: Test

1. Extract the zip on a clean machine (or VM)
2. Run PixelSync
3. Follow setup wizard
4. Test with a few sample files

## Distribution Checklist

- [ ] Built for macOS
- [ ] Built for Windows
- [ ] Built for Linux (if needed)
- [ ] README.md included
- [ ] Tested on clean machine
- [ ] All adb binaries included
- [ ] No Python installation required
- [ ] Setup wizard works
- [ ] File transfer works
- [ ] Config saves/loads correctly

## Troubleshooting Build Issues

### "adb not found" error
- Make sure adb folder exists with binaries for all platforms
- Check folder structure matches expected layout

### "Module not found" error
- Install missing module: `pip install <module>`
- Check requirements.txt is complete

### Executable too large
- PyInstaller bundles Python runtime (~30-50 MB is normal)
- Use `--onefile` flag (already in build scripts)

### antivirus false positive
- Common with PyInstaller executables
- Sign the executable (requires certificate)
- Or warn users to add exception

## File Sizes

Expected file sizes after build:

- **macOS**: ~40-50 MB
- **Windows**: ~35-45 MB
- **Linux**: ~40-50 MB

(Size includes Python runtime + adb binaries)

## Advanced: Custom Icons

To add a custom icon:

1. Create icon file:
   - **macOS**: .icns file
   - **Windows**: .ico file
   - **Linux**: .png file

2. Update build scripts:
   ```bash
   pyinstaller --icon=icon.icns ...  # macOS
   pyinstaller --icon=icon.ico ...   # Windows
   ```

## Notes

- The executable is platform-specific (build on Mac for Mac, Windows for Windows)
- Users don't need Python installed
- First run creates `Photos_To_Sync` folder and `pixelsync_config.json`
- Configuration persists between runs
