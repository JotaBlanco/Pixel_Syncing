#!/usr/bin/env python3
"""
Pixel Phone to Mac File Transfer Script
Moves files from Pixel phone to macOS using adb.
Also handles syncing from Mac to Pixel for unlimited Google Photos backup!
"""

import subprocess
import os
import sys
import time
from pathlib import Path
from typing import Optional, List, Set


def get_file_list(pixel_path: str, adb_cmd: List[str]) -> List[str]:
    """Get list of files from Pixel directory."""
    ls_cmd = adb_cmd + ['shell', 'find', pixel_path, '-type', 'f']
    result = subprocess.run(ls_cmd, capture_output=True, text=True)
    if result.returncode == 0:
        files = [f.strip() for f in result.stdout.strip().split('\n') if f.strip()]
        return files
    return []


def transfer_files_from_pixel(pixel_path: str, mac_path: str, device_id: Optional[str] = None) -> bool:
    """
    Cut (move) files from Pixel phone to Mac with verbose progress.

    Args:
        pixel_path: Path on the Pixel phone (e.g., '/sdcard/DCIM/Camera/')
        mac_path: Destination path on Mac (e.g., '/Users/javiquix/Pictures/')
        device_id: Optional device ID if multiple devices connected (e.g., 'HT6940202447')

    Returns:
        bool: True if successful, False otherwise

    Example:
        transfer_files_from_pixel('/sdcard/DCIM/Camera/', '~/Pictures/Pixel_Photos/')
    """

    # Expand user path if needed (e.g., ~ to /Users/username)
    mac_path = os.path.expanduser(mac_path)

    # Create destination directory if it doesn't exist
    os.makedirs(mac_path, exist_ok=True)

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
        print(f"⚠️  No files found in {pixel_path}")
        return True

    total_files = len(files)
    print(f"📦 Found {total_files} files to transfer\n")

    # Transfer files one by one
    transferred = 0
    failed = []

    for i, file_path in enumerate(files, 1):
        filename = os.path.basename(file_path)

        # Show progress on same line
        percentage = (i / total_files) * 100
        progress_msg = f"⬇️  [{i}/{total_files}] ({percentage:.1f}%) Transferring: {filename}"

        # Print with carriage return to overwrite
        print(f"\r{progress_msg}", end='', flush=True)

        # Pull individual file directly to destination (flatten structure)
        destination_file = os.path.join(mac_path, filename)
        pull_cmd = adb_cmd + ['pull', file_path, destination_file]
        result = subprocess.run(pull_cmd, capture_output=True, text=True)

        if result.returncode == 0:
            # Delete from phone after successful transfer
            # Quote the file path to handle special characters like parentheses
            rm_cmd = adb_cmd + ['shell', 'rm', f'"{file_path}"']
            rm_result = subprocess.run(rm_cmd, capture_output=True, text=True)

            if rm_result.returncode == 0:
                transferred += 1
            else:
                # Pull succeeded but delete failed
                print(f"\n⚠️  Pulled {filename} but failed to delete from phone")
                print(f"    Error: {rm_result.stderr}")
                failed.append(filename)
        else:
            failed.append(filename)

    # Clear the line and print final summary
    print(f"\r{' ' * 100}\r", end='')  # Clear the line
    print(f"✅ Successfully transferred {transferred}/{total_files} files")

    if failed:
        print(f"⚠️  Failed to transfer {len(failed)} files:")
        for f in failed:
            print(f"   - {f}")

    # Clean up empty directories on phone
    print(f"🗑️  Cleaning up empty directories on phone...")
    cleanup_cmd = adb_cmd + ['shell', f'find {pixel_path} -type d -empty -delete']
    subprocess.run(cleanup_cmd, capture_output=True, text=True)

    return len(failed) == 0


def get_pixel_folder_size_mb(pixel_path: str, device_id: Optional[str] = None) -> float:
    """
    Get total size of files in a Pixel directory in MB.

    Args:
        pixel_path: Path on the Pixel phone
        device_id: Optional device ID if multiple devices connected

    Returns:
        float: Size in megabytes
    """
    adb_cmd = ['adb']
    if device_id:
        adb_cmd.extend(['-s', device_id])

    # Use du to get size in KB, then convert to MB
    du_cmd = adb_cmd + ['shell', f'du -sk {pixel_path}']

    try:
        result = subprocess.run(du_cmd, capture_output=True, text=True, check=True)
        size_kb = int(result.stdout.split()[0])
        size_mb = size_kb / 1024
        return size_mb
    except (subprocess.CalledProcessError, ValueError, IndexError):
        return 0.0


def transfer_to_pixel(
    mac_folder: str,
    pixel_path: str,
    device_id: Optional[str] = None,
    batch_size: int = 10,
    max_size_gb: float = 2.0,
    sleep_minutes: int = 30,
    keep_extensions: Optional[Set[str]] = None,
    delete_extensions: Optional[Set[str]] = None,
    add_suffix: bool = False
) -> None:
    """
    Transfer files from Mac to Pixel in batches, monitoring storage space.
    Optionally renames files with _pixel suffix before extension.

    Args:
        mac_folder: Source folder on Mac (e.g., '01_files_to_sink')
        pixel_path: Destination path on Pixel (e.g., '/sdcard/DCIM/Camera/')
        device_id: Optional device ID
        batch_size: Number of files to transfer per batch
        max_size_gb: Maximum size in GB before waiting for sync
        sleep_minutes: Minutes to wait when size limit reached
        keep_extensions: Set of extensions to transfer (e.g., {'.heic', '.mov'})
        delete_extensions: Set of extensions to delete without transferring (e.g., {'.aae'})
        add_suffix: If True, adds '_pixel' suffix to filenames before extension (default: False)
    """
    mac_folder = os.path.expanduser(mac_folder)
    keep_extensions = keep_extensions or {'.heic', '.mov', '.jpg', '.jpeg', '.png', '.mp4'}
    delete_extensions = delete_extensions or {'.aae'}

    # Normalize extensions to lowercase
    keep_extensions = {ext.lower() for ext in keep_extensions}
    delete_extensions = {ext.lower() for ext in delete_extensions}

    # Build adb command
    adb_cmd = ['adb']
    if device_id:
        adb_cmd.extend(['-s', device_id])

    # Check device connection
    check_cmd = adb_cmd + ['devices']
    result = subprocess.run(check_cmd, capture_output=True, text=True)
    if 'device' not in result.stdout:
        print("❌ No device connected or device unauthorized")
        return

    print(f"📱 Connected to Pixel device")
    print(f"📁 Source: {mac_folder}")
    print(f"📁 Destination: {pixel_path}")
    print(f"⚙️  Batch size: {batch_size} files")
    print(f"⚙️  Max storage: {max_size_gb} GB")
    print(f"⚙️  Sleep time: {sleep_minutes} minutes when full\n")

    # Get all files to process
    all_files = []
    files_to_delete = []

    for filename in os.listdir(mac_folder):
        filepath = os.path.join(mac_folder, filename)
        if not os.path.isfile(filepath):
            continue

        ext = os.path.splitext(filename)[1].lower()

        if ext in delete_extensions:
            files_to_delete.append(filepath)
        elif ext in keep_extensions:
            all_files.append(filepath)

    # Delete unwanted files first
    if files_to_delete:
        print(f"🗑️  Deleting {len(files_to_delete)} unwanted files ({', '.join(delete_extensions)})...")
        for filepath in files_to_delete:
            try:
                os.remove(filepath)
                print(f"   Deleted: {os.path.basename(filepath)}")
            except Exception as e:
                print(f"   ⚠️  Failed to delete {os.path.basename(filepath)}: {e}")
        print()

    if not all_files:
        print("⚠️  No files to transfer")
        return

    total_files = len(all_files)
    print(f"📦 Found {total_files} files to transfer\n")

    transferred = 0
    failed = []

    # Process files in batches
    for i in range(0, len(all_files), batch_size):
        batch = all_files[i:i + batch_size]

        # Check Pixel storage before each batch
        current_size_mb = get_pixel_folder_size_mb(pixel_path, device_id)
        current_size_gb = current_size_mb / 1024

        print(f"📊 Current Pixel storage: {current_size_gb:.2f} GB / {max_size_gb} GB")

        # Wait if storage is too full
        while current_size_gb >= max_size_gb:
            print(f"⏸️  Storage full ({current_size_gb:.2f} GB >= {max_size_gb} GB)")
            print(f"💤 Sleeping for {sleep_minutes} minutes...")
            print(f"   👉 Use this time to run 'Free up space' in Google Photos app on Pixel!")
            time.sleep(sleep_minutes * 60)

            current_size_mb = get_pixel_folder_size_mb(pixel_path, device_id)
            current_size_gb = current_size_mb / 1024
            print(f"📊 Rechecked storage: {current_size_gb:.2f} GB / {max_size_gb} GB")

        # Transfer batch
        print(f"\n🚀 Processing batch {(i // batch_size) + 1} ({len(batch)} files)...")

        for j, mac_file in enumerate(batch, 1):
            filename = os.path.basename(mac_file)

            # Optionally add _pixel suffix before extension
            if add_suffix:
                name, ext = os.path.splitext(filename)
                pixel_filename = f"{name}_pixel{ext}"
            else:
                pixel_filename = filename
            pixel_file_path = f"{pixel_path.rstrip('/')}/{pixel_filename}"

            # Progress
            overall_progress = transferred + j
            percentage = (overall_progress / total_files) * 100
            progress_line = f"⬆️  [{overall_progress}/{total_files}] ({percentage:.1f}%) Uploading: {pixel_filename}"
            # Clear line and print progress (pad with spaces to ensure previous text is overwritten)
            print(f"\r{progress_line:<120}", end='', flush=True)

            # Push to Pixel
            push_cmd = adb_cmd + ['push', mac_file, pixel_file_path]
            result = subprocess.run(push_cmd, capture_output=True, text=True)

            if result.returncode == 0:
                # Delete from Mac after successful transfer
                try:
                    os.remove(mac_file)
                    transferred += 1
                except Exception as e:
                    print(f"\n⚠️  Failed to delete {filename} from Mac: {e}")

                # Small delay between files to prevent overwhelming the device
                time.sleep(0.5)
            else:
                failed.append(filename)
                print(f"\n⚠️  Failed to upload {filename}")

        print()  # New line after batch

        # Trigger media scanner to help Google Photos detect new files
        print(f"📢 Notifying media scanner of new files...")
        # Touch files to update timestamps (helps media scanner)
        if add_suffix:
            touch_cmd = adb_cmd + ['shell', 'find /sdcard/DCIM/Camera -name "*_pixel*" -exec touch {} \\;']
        else:
            # Touch all files in the Camera directory
            touch_cmd = adb_cmd + ['shell', 'find /sdcard/DCIM/Camera -type f -exec touch {} \\;']
        subprocess.run(touch_cmd, capture_output=True, text=True)

        # Broadcast media scanner intent to force re-scan
        scan_cmd = adb_cmd + ['shell', 'am', 'broadcast', '-a', 'android.intent.action.MEDIA_SCANNER_SCAN_FILE', '-d', 'file:///sdcard/DCIM/Camera']
        subprocess.run(scan_cmd, capture_output=True, text=True)

        # Pause between batches to let Pixel breathe and sync to Google Photos
        if i + batch_size < len(all_files):  # Don't pause after last batch
            pause_seconds = 30
            print(f"⏸️  Pausing {pause_seconds} seconds between batches to let Pixel sync...")
            print(f"   💡 Good time to check Google Photos sync status or free up space!")
            time.sleep(pause_seconds)

    # Final summary
    print(f"\n{'='*60}")
    print(f"✅ Successfully transferred: {transferred}/{total_files} files")

    if failed:
        print(f"⚠️  Failed to transfer {len(failed)} files:")
        for f in failed:
            print(f"   - {f}")

    final_size_mb = get_pixel_folder_size_mb(pixel_path, device_id)
    final_size_gb = final_size_mb / 1024
    print(f"📊 Final Pixel storage: {final_size_gb:.2f} GB")
    print(f"{'='*60}\n")

    # Final media scanner trigger
    print("📢 Final media scanner notification...")
    if add_suffix:
        touch_cmd = adb_cmd + ['shell', 'find /sdcard/DCIM/Camera -name "*_pixel*" -exec touch {} \\;']
    else:
        touch_cmd = adb_cmd + ['shell', 'find /sdcard/DCIM/Camera -type f -exec touch {} \\;']
    subprocess.run(touch_cmd, capture_output=True, text=True)

    # Broadcast media scanner intent to force full re-scan
    scan_cmd = adb_cmd + ['shell', 'am', 'broadcast', '-a', 'android.intent.action.MEDIA_SCANNER_SCAN_FILE', '-d', 'file:///sdcard/DCIM/Camera']
    subprocess.run(scan_cmd, capture_output=True, text=True)

    # Also try triggering a full media re-scan
    rescan_cmd = adb_cmd + ['shell', 'am', 'broadcast', '-a', 'android.intent.action.MEDIA_MOUNTED', '-d', 'file:///sdcard']
    subprocess.run(rescan_cmd, capture_output=True, text=True)

    print("\n📱 Next steps to ensure Google Photos detects all files:")
    print("   1. On Pixel: Settings → Apps → Google Photos → Force Stop")
    print("   2. Open Google Photos app again")
    print("   3. Wait 1-2 minutes for it to scan")
    print("   4. Check backup status (should show all files)")
    print("   5. When backup complete, use 'Free up space'")

    if final_size_gb >= max_size_gb * 0.8:  # Warn if 80% full
        print(f"\n⚠️  Storage is {(final_size_gb/max_size_gb)*100:.0f}% full!")
        print("💡 Tip: Run 'Free up space' in Google Photos app to free storage!")


def list_pixel_directory(pixel_path: str, device_id: Optional[str] = None) -> None:
    """
    List contents of a directory on the Pixel phone.

    Args:
        pixel_path: Path on the Pixel phone
        device_id: Optional device ID if multiple devices connected
    """
    adb_cmd = ['adb']
    if device_id:
        adb_cmd.extend(['-s', device_id])

    ls_cmd = adb_cmd + ['shell', 'ls', '-lah', pixel_path]

    try:
        result = subprocess.run(ls_cmd, capture_output=True, text=True, check=True)
        print(f"📂 Contents of {pixel_path}:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error listing directory: {e}")
        print(f"stderr: {e.stderr}")


if __name__ == "__main__":
    # Example usage

    # First, let's see what's in the camera folder
    print("Checking Pixel camera folder...\n")
    list_pixel_directory('/sdcard/DCIM/Camera/')

    # Example: Transfer camera photos
    # Uncomment to use:
    # transfer_files_from_pixel(
    #     pixel_path='/sdcard/DCIM/Camera/',
    #     mac_path='~/Desktop/Pixel_Photos/',
    #     device_id='HT6940202447'  # Your Pixel's ID
    # )
