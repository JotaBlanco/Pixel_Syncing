# PixelSync - Developer Notes

## What This Is

PixelSync is a user-friendly, distributable version of your Pixel photo sync system. It's designed for non-technical users to easily backup photos to Google Photos using a Pixel phone.

## What's Different from Your Version

### Your Version (Pixel_Syncing/)
- Python scripts you run directly
- Config in Python files
- Manual setup of device ID, folders, etc.
- Requires Python knowledge

### Distributable Version (PixelSync_Distributable/)
- Standalone executable (no Python needed)
- Interactive setup wizard
- Config in JSON file
- User-friendly for non-technical people
- Auto-detects Pixel device
- Bundled adb binaries

## Files Overview

### Core Files
- **pixelsync.py** - Main entry point, handles CLI and orchestration
- **pixel_sync_core.py** - Transfer engine (same logic as your pixel_transfer.py)
- **config_manager.py** - Configuration and setup wizard
- **requirements.txt** - Python dependencies (only PyInstaller for building)

### Build Files
- **build.sh** - macOS/Linux build script
- **build.bat** - Windows build script
- **build.spec** - PyInstaller specification (if needed)

### Documentation
- **README.md** - User documentation
- **QUICKSTART.md** - Simple guide for non-technical users
- **BUILDING.md** - Instructions for you to build executables
- **FOR_DEVELOPER.md** - This file

## How to Build

1. **Download adb binaries** for Mac, Windows, Linux (see BUILDING.md)
2. **Install PyInstaller**: `pip install pyinstaller`
3. **Run build script**:
   - Mac: `./build.sh`
   - Windows: `build.bat`
4. **Package the executable** with README.md
5. **Share** with your friend!

## Key Features for Non-Technical Users

✅ **No Python needed** - Standalone executable
✅ **Auto-detect device** - Finds Pixel automatically
✅ **Setup wizard** - Interactive first-time configuration
✅ **Persistent config** - Settings saved in JSON file
✅ **Simple workflow** - Drop files in folder → Run app → Done
✅ **Progress tracking** - Shows what's happening in real-time
✅ **Error messages** - Clear explanations if something goes wrong

## What Your Friend Needs to Do

1. **One-time setup**:
   - Enable USB debugging on Pixel (guided in QUICKSTART.md)
   - Run PixelSync first time (setup wizard)

2. **Every time**:
   - Put photos in `Photos_To_Sync` folder
   - Connect Pixel via USB
   - Run PixelSync
   - Use "Free up space" in Google Photos when done

## Technical Details

### Auto-Detection
- Uses `adb devices` to find connected Pixels
- If multiple devices, prompts user to choose
- Saves device ID to config

### Configuration
- Stored in `pixelsync_config.json`
- User can reset with `--reset` flag
- Defaults are beginner-friendly

### ADB Bundling
- Includes adb for Mac, Windows, Linux
- Auto-selects correct version for platform
- Falls back to system adb if bundled not found

### File Management
- Creates `Photos_To_Sync` folder automatically
- Deletes files from computer after successful transfer
- Filters unwanted files (.AAE, .XMP, etc.)

## Customization

Your friend can customize by editing `pixelsync_config.json`:

```json
{
  "source_folder": "Photos_To_Sync",
  "pixel_path": "/sdcard/DCIM/Camera/",
  "device_id": "HT6940202447",
  "batch_size": 50,
  "max_storage_gb": 10.0,
  "sleep_minutes": 15,
  "keep_extensions": [".heic", ".mov", ".jpg", ...],
  "delete_extensions": [".aae", ".xmp", ...]
}
```

## Distribution Checklist

Before sharing with your friend:

- [ ] Download adb binaries for their platform
- [ ] Build executable for their platform (Mac or Windows)
- [ ] Test on a clean machine without Python
- [ ] Package with README.md and QUICKSTART.md
- [ ] Zip it up
- [ ] Share!

## Future Enhancements (Optional)

Ideas if you want to improve it later:

1. **GUI** - Add tkinter interface instead of CLI
2. **Auto-updates** - Check for new versions
3. **Multiple profiles** - Support different Pixel devices
4. **Scheduling** - Auto-run at specific times
5. **Cloud storage** - Direct upload option
6. **Error logging** - Save logs to file for debugging

## Differences in Code

### Simplified
- Removed `add_suffix` parameter (always false for user version)
- Removed `list_pixel_directory` (not needed for end users)
- Removed `transfer_files_from_pixel` (user only needs Mac→Pixel)
- Simplified error messages

### Enhanced
- Added device auto-detection
- Added setup wizard
- Added config persistence
- Added platform-specific adb path detection
- Added "Press Enter to exit" for better UX on Windows

## Support

If your friend has issues:

1. Check QUICKSTART.md
2. Check README.md troubleshooting section
3. Run with `--reset` to reconfigure
4. Check USB debugging is enabled
5. Try different USB cable/port

## Notes

- The executable is ~40-50MB (includes Python runtime + adb)
- No network connection needed (except for Google Photos backup on Pixel)
- Config file is human-readable JSON
- All source code is included if they want to inspect it
- No telemetry or tracking

Enjoy! 🚀
