#!/usr/bin/env python3
"""
PixelSync - Simple Photo/Video Sync to Google Photos via Pixel Phone
Main entry point for the application
"""

import sys
import os
import platform
from config_manager import get_config, reset_config
from pixel_sync_core import transfer_to_pixel


def get_adb_path() -> str:
    """Get the path to the bundled adb executable."""
    # Check if running as PyInstaller bundle
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    # Determine platform
    system = platform.system()

    if system == 'Darwin':  # macOS
        adb_path = os.path.join(base_path, 'adb', 'mac', 'adb')
    elif system == 'Windows':
        adb_path = os.path.join(base_path, 'adb', 'windows', 'adb.exe')
    else:  # Linux
        adb_path = os.path.join(base_path, 'adb', 'linux', 'adb')

    # If bundled adb doesn't exist, try system adb
    if not os.path.exists(adb_path):
        return 'adb'

    # Make executable on Unix-like systems
    if system != 'Windows':
        os.chmod(adb_path, 0o755)

    return adb_path


def print_banner():
    """Print application banner."""
    print("\n" + "="*60)
    print("PixelSync - Unlimited Google Photos Backup")
    print("="*60)
    print()


def main():
    """Main application entry point."""
    print_banner()

    # Check for command-line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] in ['--reset', '-r']:
            print("Resetting configuration...\n")
            reset_config()
            print("\nRun PixelSync again to create a new configuration.\n")
            return
        elif sys.argv[1] in ['--help', '-h']:
            print("PixelSync - Sync photos/videos to Google Photos via Pixel phone\n")
            print("Usage:")
            print("  pixelsync          Run the sync process")
            print("  pixelsync --reset  Reset configuration and run setup again")
            print("  pixelsync --help   Show this help message\n")
            return

    # Get adb path
    adb_path = get_adb_path()

    # Get or create configuration
    config = get_config(adb_path)

    # Show current configuration
    print("\nCurrent Configuration:")
    print(f"  📂 Source folder: {config['source_folder']}")
    print(f"  📱 Device ID: {config['device_id']}")
    print(f"  📦 Batch size: {config['batch_size']} files")
    print(f"  💾 Max storage: {config['max_storage_gb']} GB")
    print(f"  ⏱️  Sleep time: {config['sleep_minutes']} minutes")
    print()

    # Check if source folder has files
    source_folder = config['source_folder']
    if not os.path.exists(source_folder):
        os.makedirs(source_folder)

    file_count = len([f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))])

    if file_count == 0:
        print(f"📭 No files found in {source_folder}/")
        print(f"\n💡 Put your photos/videos in the '{source_folder}' folder and run PixelSync again.\n")
        input("Press Enter to exit...")
        return

    print(f"📦 Found {file_count} files to process")
    print("\n🚀 Starting sync process...\n")
    input("Press Enter to continue (or Ctrl+C to cancel)...")
    print()

    # Run the sync
    try:
        success = transfer_to_pixel(
            mac_folder=config['source_folder'],
            pixel_path=config['pixel_path'],
            adb_path=adb_path,
            device_id=config['device_id'],
            batch_size=config['batch_size'],
            max_size_gb=config['max_storage_gb'],
            sleep_minutes=config['sleep_minutes'],
            keep_extensions=set(config['keep_extensions']),
            delete_extensions=set(config['delete_extensions'])
        )

        if success:
            print("\n🎉 Sync completed successfully!")
        else:
            print("\n⚠️  Sync completed with some errors.")

    except KeyboardInterrupt:
        print("\n\n⚠️  Sync cancelled by user.")
    except Exception as e:
        print(f"\n❌ Error during sync: {e}")
        import traceback
        traceback.print_exc()

    print()
    input("Press Enter to exit...")


if __name__ == "__main__":
    main()
