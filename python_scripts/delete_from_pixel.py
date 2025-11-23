#!/usr/bin/env python3
"""
Delete files from Pixel Camera folder.
USE WITH EXTREME CAUTION - This permanently deletes files!

Use this after you've verified files are backed up to Google Photos.
"""

import subprocess
import os
from typing import Optional, List


def get_file_list(pixel_path: str, adb_cmd: List[str]) -> List[str]:
    """Get list of files from Pixel directory."""
    ls_cmd = adb_cmd + ['shell', 'find', pixel_path, '-type', 'f']
    result = subprocess.run(ls_cmd, capture_output=True, text=True)
    if result.returncode == 0:
        files = [f.strip() for f in result.stdout.strip().split('\n') if f.strip()]
        return files
    return []


def delete_files_from_pixel(pixel_path: str, device_id: Optional[str] = None) -> bool:
    """
    Delete ALL files from Pixel phone Camera folder.

    Args:
        pixel_path: Path on the Pixel phone (e.g., '/sdcard/DCIM/Camera/')
        device_id: Optional device ID if multiple devices connected

    Returns:
        bool: True if successful, False otherwise
    """
    # Build adb command
    adb_cmd = ['adb']
    if device_id:
        adb_cmd.extend(['-s', device_id])

    # Check if device is connected
    check_cmd = adb_cmd + ['devices']
    result = subprocess.run(check_cmd, capture_output=True, text=True)

    if 'device' not in result.stdout:
        print("❌ No device connected or device unauthorized")
        print(result.stdout)
        return False

    print(f"📱 Connected to Pixel device")

    # Get list of files
    print(f"📋 Getting file list from {pixel_path}...")
    files = get_file_list(pixel_path, adb_cmd)

    if not files:
        print(f"✅ No files found in {pixel_path} - nothing to delete")
        return True

    total_files = len(files)
    print(f"📦 Found {total_files} files to DELETE\n")

    # Show first few files as preview
    print("Preview of files to be deleted:")
    for i, file_path in enumerate(files[:5], 1):
        filename = os.path.basename(file_path)
        print(f"   {i}. {filename}")
    if total_files > 5:
        print(f"   ... and {total_files - 5} more files")
    print()

    # Delete files one by one
    deleted = 0
    failed = []

    for i, file_path in enumerate(files, 1):
        filename = os.path.basename(file_path)

        # Show progress on same line
        percentage = (i / total_files) * 100
        progress_msg = f"🗑️  [{i}/{total_files}] ({percentage:.1f}%) Deleting: {filename}"

        # Print with carriage return to overwrite
        print(f"\r{progress_msg:<120}", end='', flush=True)

        # Delete file - quote path to handle special characters
        rm_cmd = adb_cmd + ['shell', 'rm', f'"{file_path}"']
        result = subprocess.run(rm_cmd, capture_output=True, text=True)

        if result.returncode == 0:
            deleted += 1
        else:
            print(f"\n⚠️  Failed to delete {filename}")
            print(f"    Error: {result.stderr}")
            failed.append(filename)

    # Clear the line and print final summary
    print(f"\r{' ' * 120}\r", end='')
    print(f"✅ Successfully deleted {deleted}/{total_files} files")

    if failed:
        print(f"⚠️  Failed to delete {len(failed)} files:")
        for f in failed:
            print(f"   - {f}")

    # Clean up empty directories on phone
    print(f"🗑️  Cleaning up empty directories on phone...")
    cleanup_cmd = adb_cmd + ['shell', f'find {pixel_path} -type d -empty -delete']
    subprocess.run(cleanup_cmd, capture_output=True, text=True)

    return len(failed) == 0


# Configuration
PIXEL_PATH = '/sdcard/DCIM/Camera/'
DEVICE_ID = 'HT6940202447'

if __name__ == "__main__":
    print("="*60)
    print("⚠️  DELETE FILES FROM PIXEL ⚠️")
    print("PERMANENT DELETION TOOL")
    print("="*60)
    print()
    print("🚨 WARNING: This will PERMANENTLY DELETE files from Pixel!")
    print("   Make sure files are backed up to Google Photos first!")
    print()

    # First confirmation
    response1 = input("Are you sure you want to DELETE all files from Pixel Camera? (yes/no): ")

    if response1.lower() != 'yes':
        print("❌ Deletion cancelled.")
        exit(0)

    print()
    print("🚨 SECOND CONFIRMATION REQUIRED")
    print("   This action CANNOT be undone!")
    print()

    # Second confirmation
    response2 = input("Type 'DELETE' in ALL CAPS to confirm permanent deletion: ")

    if response2 != 'DELETE':
        print("❌ Deletion cancelled.")
        exit(0)

    print("\n🗑️  Starting deletion process...\n")

    success = delete_files_from_pixel(
        pixel_path=PIXEL_PATH,
        device_id=DEVICE_ID
    )

    if success:
        print("\n✅ Deletion complete!")
        print("\n📝 Files have been permanently removed from Pixel")
    else:
        print("\n⚠️  Some files failed to delete. Check the errors above.")
