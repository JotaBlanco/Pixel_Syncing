#!/usr/bin/env python3
"""
PixelSync Core - Transfer engine for syncing photos to Google Photos via Pixel
"""

import subprocess
import os
import time
from typing import Optional, List, Set


def get_file_list(pixel_path: str, adb_cmd: List[str]) -> List[str]:
    """Get list of files from Pixel directory."""
    ls_cmd = adb_cmd + ['shell', 'find', pixel_path, '-type', 'f']
    result = subprocess.run(ls_cmd, capture_output=True, text=True)
    if result.returncode == 0:
        files = [f.strip() for f in result.stdout.strip().split('\n') if f.strip()]
        return files
    return []


def get_connected_devices(adb_path: str = 'adb') -> List[str]:
    """Get list of connected Android devices."""
    result = subprocess.run([adb_path, 'devices'], capture_output=True, text=True)
    if result.returncode != 0:
        return []

    devices = []
    for line in result.stdout.strip().split('\n')[1:]:  # Skip header
        if '\tdevice' in line:
            device_id = line.split('\t')[0]
            devices.append(device_id)
    return devices


def get_pixel_folder_size_mb(pixel_path: str, adb_cmd: List[str]) -> float:
    """Get total size of files in a Pixel directory in MB."""
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
    adb_path: str = 'adb',
    device_id: Optional[str] = None,
    batch_size: int = 50,
    max_size_gb: float = 10.0,
    sleep_minutes: int = 15,
    keep_extensions: Optional[Set[str]] = None,
    delete_extensions: Optional[Set[str]] = None
) -> bool:
    """
    Transfer files from computer to Pixel in batches, monitoring storage space.

    Returns:
        bool: True if successful, False otherwise
    """
    mac_folder = os.path.expanduser(mac_folder)
    keep_extensions = keep_extensions or {'.heic', '.mov', '.jpg', '.jpeg', '.png', '.mp4', '.gif'}
    delete_extensions = delete_extensions or {'.aae', '.xmp', '.zip', '.ds_store', '.dng'}

    # Normalize extensions to lowercase
    keep_extensions = {ext.lower() for ext in keep_extensions}
    delete_extensions = {ext.lower() for ext in delete_extensions}

    # Build adb command
    adb_cmd = [adb_path]
    if device_id:
        adb_cmd.extend(['-s', device_id])

    # Check device connection
    check_cmd = adb_cmd + ['devices']
    result = subprocess.run(check_cmd, capture_output=True, text=True)
    if 'device' not in result.stdout:
        print("❌ No device connected or device unauthorized")
        return False

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
        print(f"🗑️  Deleting {len(files_to_delete)} unwanted files...")
        for filepath in files_to_delete:
            try:
                os.remove(filepath)
            except Exception as e:
                print(f"   ⚠️  Failed to delete {os.path.basename(filepath)}: {e}")
        print()

    if not all_files:
        print("⚠️  No files to transfer")
        return True

    total_files = len(all_files)
    print(f"📦 Found {total_files} files to transfer\n")

    transferred = 0
    failed = []

    # Process files in batches
    for i in range(0, len(all_files), batch_size):
        batch = all_files[i:i + batch_size]

        # Check Pixel storage before each batch
        current_size_mb = get_pixel_folder_size_mb(pixel_path, adb_cmd)
        current_size_gb = current_size_mb / 1024

        print(f"📊 Current Pixel storage: {current_size_gb:.2f} GB / {max_size_gb} GB")

        # Wait if storage is too full
        while current_size_gb >= max_size_gb:
            print(f"⏸️  Storage full ({current_size_gb:.2f} GB >= {max_size_gb} GB)")
            print(f"💤 Sleeping for {sleep_minutes} minutes...")
            print(f"   💡 Good time to free up space!")
            time.sleep(sleep_minutes * 60)

            current_size_mb = get_pixel_folder_size_mb(pixel_path, adb_cmd)
            current_size_gb = current_size_mb / 1024
            print(f"📊 Rechecked storage: {current_size_gb:.2f} GB / {max_size_gb} GB")

        # Transfer batch
        print(f"\n🚀 Processing batch {(i // batch_size) + 1} ({len(batch)} files)...")

        for j, mac_file in enumerate(batch, 1):
            filename = os.path.basename(mac_file)
            pixel_file_path = f"{pixel_path.rstrip('/')}/{filename}"

            # Progress
            overall_progress = transferred + j
            percentage = (overall_progress / total_files) * 100
            progress_line = f"⬆️  [{overall_progress}/{total_files}] ({percentage:.1f}%) Uploading: {filename}"
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
                    print(f"\n⚠️  Failed to delete {filename} from computer: {e}")

                # Small delay between files
                time.sleep(0.5)
            else:
                failed.append(filename)
                print(f"\n⚠️  Failed to upload {filename}")

        print()  # New line after batch

        # Trigger media scanner
        print(f"📢 Notifying media scanner of new files...")
        touch_cmd = adb_cmd + ['shell', 'find /sdcard/DCIM/Camera -type f -exec touch {} \\;']
        subprocess.run(touch_cmd, capture_output=True, text=True)

        scan_cmd = adb_cmd + ['shell', 'am', 'broadcast', '-a', 'android.intent.action.MEDIA_SCANNER_SCAN_FILE', '-d', 'file:///sdcard/DCIM/Camera']
        subprocess.run(scan_cmd, capture_output=True, text=True)

        # Pause between batches
        if i + batch_size < len(all_files):
            pause_seconds = 10
            print(f"⏸️  Pausing {pause_seconds} seconds between batches...")
            print(f"   💡 Good time to check Google Photos sync status!")
            time.sleep(pause_seconds)

    # Final summary
    print(f"\n{'='*60}")
    print(f"✅ Successfully transferred: {transferred}/{total_files} files")

    if failed:
        print(f"⚠️  Failed to transfer {len(failed)} files:")
        for f in failed:
            print(f"   - {f}")

    final_size_mb = get_pixel_folder_size_mb(pixel_path, adb_cmd)
    final_size_gb = final_size_mb / 1024
    print(f"📊 Final Pixel storage: {final_size_gb:.2f} GB")
    print(f"{'='*60}\n")

    # Final media scanner trigger
    print("📢 Final media scanner notification...")
    touch_cmd = adb_cmd + ['shell', 'find /sdcard/DCIM/Camera -type f -exec touch {} \\;']
    subprocess.run(touch_cmd, capture_output=True, text=True)

    scan_cmd = adb_cmd + ['shell', 'am', 'broadcast', '-a', 'android.intent.action.MEDIA_SCANNER_SCAN_FILE', '-d', 'file:///sdcard/DCIM/Camera']
    subprocess.run(scan_cmd, capture_output=True, text=True)

    rescan_cmd = adb_cmd + ['shell', 'am', 'broadcast', '-a', 'android.intent.action.MEDIA_MOUNTED', '-d', 'file:///sdcard']
    subprocess.run(rescan_cmd, capture_output=True, text=True)

    print("\n📱 Next steps:")
    print("   1. On Pixel: Settings → Apps → Google Photos → Force Stop")
    print("   2. Open Google Photos app again")
    print("   3. Wait 1-2 minutes for it to scan")
    print("   4. Check backup status")
    print("   5. When backup complete, use 'Free up space'")

    if final_size_gb >= max_size_gb * 0.8:
        print(f"\n⚠️  Storage is {(final_size_gb/max_size_gb)*100:.0f}% full!")
        print("💡 Tip: Run 'Free up space' in Google Photos app!")

    return len(failed) == 0
