#!/usr/bin/env python3
"""
Main script to sync iPhone photos from Mac to Pixel for unlimited Google Photos backup.

Usage:
    python3 sync_to_pixel.py

This will automatically:
1. Delete unwanted files (.aae)
2. Transfer photos/videos to Pixel in batches
3. Rename files with _pixel suffix
4. Monitor Pixel storage and pause when full
5. Resume automatically after you free up space
"""

import os
from pixel_transfer import transfer_to_pixel

# Get absolute paths based on script location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)

# Configuration
MAC_FOLDER = os.path.join(REPO_ROOT, '01_files_to_sink')  # Shared folder at repo root
PIXEL_PATH = '/sdcard/DCIM/Camera/'
DEVICE_ID = 'HT6940202447'  # Your Pixel XL

# Transfer settings
BATCH_SIZE = 50  # Files per batch
MAX_SIZE_GB = 15.0  # Maximum GB on Pixel before pausing
SLEEP_MINUTES = 15  # Minutes to wait when storage is full

# File types to transfer (Google Photos compatible)
KEEP_EXTENSIONS = {
    '.heic', '.HEIC',  # Apple High Efficiency Image Format
    '.mov', '.MOV',     # QuickTime videos
    '.jpg', '.JPG', '.jpeg', '.JPEG',  # JPEG images
    '.png', '.PNG',     # PNG images
    '.mp4', '.MP4',     # MP4 videos
    '.gif', '.GIF',     # GIF animations
}

# File types to delete without transferring (metadata/system files)
DELETE_EXTENSIONS = {
    '.aae', '.AAE',         # Apple edit metadata
    '.xmp', '.XMP',         # Adobe metadata sidecar files
    '.zip', '.ZIP',         # Archive files
    '.nomedia',             # Android system file
    '.DS_Store',            # macOS system file
    '.dng', '.DNG',         # RAW files (optional - Google Photos supports but takes space)
}

if __name__ == "__main__":
    print("="*60)
    print("iPhone → Mac → Pixel → Google Photos Sync")
    print("Unlimited Photo Backup Automation")
    print("="*60)
    print()

    transfer_to_pixel(
        mac_folder=MAC_FOLDER,
        pixel_path=PIXEL_PATH,
        device_id=DEVICE_ID,
        batch_size=BATCH_SIZE,
        max_size_gb=MAX_SIZE_GB,
        sleep_minutes=SLEEP_MINUTES,
        keep_extensions=KEEP_EXTENSIONS,
        delete_extensions=DELETE_EXTENSIONS,
        add_suffix=False  # Set to True if you want to add _pixel suffix to filenames
    )

    print("\n🎉 Sync complete!")
    print("\n📝 Next steps:")
    print("   1. Open Google Photos app on Pixel")
    print("   2. Check that photos are syncing/synced")
    print("   3. Go to Settings → Free up space")
    print("   4. Run this script again if you have more files!\n")
