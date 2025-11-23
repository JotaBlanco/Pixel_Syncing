# Pixel Photo Sync System

Automated system to backup iPhone photos to Google Photos using a Pixel phone's unlimited original quality storage.

## Repository Structure

```
Pixel_Syncing/
├── 01_files_to_sink/        # Source folder for files to sync (shared)
├── 02_files_to_doublecheck/ # Recovery folder (shared)
│
├── python_scripts/          # Python development scripts
│   ├── pixel_transfer.py    # Core transfer functions
│   ├── sync_to_pixel.py     # Main sync script
│   ├── recover_from_pixel.py # Recovery tool
│   ├── delete_from_pixel.py  # Deletion tool
│   └── .venv/               # Python virtual environment
│
└── distributable/           # User-friendly standalone version
    ├── pixelsync.py         # Main application
    ├── pixel_sync_core.py   # Transfer engine
    ├── config_manager.py    # Setup wizard
    ├── build.sh / build.bat # Build scripts
    └── README.md            # User documentation
```

## For Developers (You)

### Setup

```bash
cd python_scripts
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### Configure

Edit `sync_to_pixel.py` to set your:
- Device ID
- Folder paths
- Batch size
- Storage limits

### Run

```bash
cd python_scripts
python3 sync_to_pixel.py
```

## For Non-Technical Users (Your Friends)

See the `distributable/` folder for a user-friendly standalone version that doesn't require Python knowledge.

### Build Distributable Version

```bash
cd distributable
./build.sh  # macOS/Linux
# or
build.bat   # Windows
```

See `distributable/BUILDING.md` for detailed instructions.

## Workflow

1. **Export photos** from iPhone to Mac
2. **Put files** in `01_files_to_sink/` (at repo root)
3. **Run** `cd python_scripts && python3 sync_to_pixel.py`
4. Files transfer to Pixel → Google Photos backs them up
5. **Free up space** in Google Photos app on Pixel
6. Repeat!

## Tools

- **sync_to_pixel.py** - Main sync script (Mac → Pixel)
- **recover_from_pixel.py** - Pull files back from Pixel for verification
- **delete_from_pixel.py** - Delete files from Pixel (with double confirmation)
- **pixel_transfer.py** - Core transfer functions (library)

## Requirements

- Python 3.7+
- Pixel phone (Gen 1) with USB debugging enabled
- Android Platform Tools (adb)
  - macOS: `brew install android-platform-tools`
  - Windows: Download from Google

## License

Personal use only.
