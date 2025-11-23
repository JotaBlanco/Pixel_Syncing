#!/usr/bin/env python3
"""
Configuration manager for PixelSync
Handles reading/writing config and setup wizard
"""

import json
import os
import sys
from typing import Dict, Any, Optional
from pixel_sync_core import get_connected_devices


CONFIG_FILE = 'pixelsync_config.json'

DEFAULT_CONFIG = {
    "source_folder": "../01_files_to_sink",  # Shared folder at repo root
    "pixel_path": "/sdcard/DCIM/Camera/",
    "device_id": None,
    "batch_size": 50,
    "max_storage_gb": 10.0,
    "sleep_minutes": 15,
    "keep_extensions": [".heic", ".mov", ".jpg", ".jpeg", ".png", ".mp4", ".gif", ".HEIC", ".MOV", ".JPG", ".JPEG", ".PNG", ".MP4", ".GIF"],
    "delete_extensions": [".aae", ".xmp", ".zip", ".DS_Store", ".dng", ".AAE", ".XMP", ".ZIP", ".DNG"]
}


def load_config() -> Optional[Dict[str, Any]]:
    """Load configuration from file."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️  Error loading config: {e}")
            return None
    return None


def save_config(config: Dict[str, Any]) -> bool:
    """Save configuration to file."""
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
        return True
    except Exception as e:
        print(f"❌ Error saving config: {e}")
        return False


def setup_wizard(adb_path: str = 'adb') -> Dict[str, Any]:
    """Interactive setup wizard for first-time configuration."""
    print("="*60)
    print("Welcome to PixelSync Setup Wizard!")
    print("="*60)
    print("\nThis wizard will help you configure PixelSync.\n")

    config = DEFAULT_CONFIG.copy()

    # 1. Detect Pixel device
    print("Step 1: Detecting Pixel device...")
    print("Please connect your Pixel phone via USB and enable USB debugging.")
    input("Press Enter when ready...")

    devices = get_connected_devices(adb_path)

    if not devices:
        print("\n❌ No devices found!")
        print("\nMake sure:")
        print("  1. USB debugging is enabled on your Pixel")
        print("  2. You've authorized your computer on the Pixel")
        print("  3. The USB cable is properly connected")
        print("\nRestart this setup after connecting your device.\n")
        sys.exit(1)
    elif len(devices) == 1:
        config['device_id'] = devices[0]
        print(f"✅ Found device: {devices[0]}")
    else:
        print(f"\n📱 Found {len(devices)} devices:")
        for idx, device in enumerate(devices, 1):
            print(f"  {idx}. {device}")

        while True:
            choice = input(f"\nSelect device (1-{len(devices)}): ")
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(devices):
                    config['device_id'] = devices[idx]
                    print(f"✅ Selected: {devices[idx]}")
                    break
            except ValueError:
                pass
            print("Invalid choice. Try again.")

    # 2. Source folder
    print(f"\nStep 2: Source folder")
    print(f"This is where you'll put photos/videos to sync.")
    print(f"Default: {DEFAULT_CONFIG['source_folder']}")

    custom_folder = input("\nUse default? (y/n): ").lower()
    if custom_folder == 'n':
        folder = input("Enter folder name: ").strip()
        if folder:
            config['source_folder'] = folder

    # Create source folder if it doesn't exist
    os.makedirs(config['source_folder'], exist_ok=True)
    print(f"✅ Source folder: {config['source_folder']}")

    # 3. Storage settings
    print(f"\nStep 3: Storage settings")
    print(f"Max storage on Pixel before pausing: {DEFAULT_CONFIG['max_storage_gb']} GB")
    print(f"Wait time when storage full: {DEFAULT_CONFIG['sleep_minutes']} minutes")

    custom_storage = input("\nUse default settings? (y/n): ").lower()
    if custom_storage == 'n':
        try:
            gb = input(f"Max storage (GB) [{DEFAULT_CONFIG['max_storage_gb']}]: ").strip()
            if gb:
                config['max_storage_gb'] = float(gb)

            mins = input(f"Sleep minutes [{DEFAULT_CONFIG['sleep_minutes']}]: ").strip()
            if mins:
                config['sleep_minutes'] = int(mins)
        except ValueError:
            print("Invalid input, using defaults")

    print(f"✅ Max storage: {config['max_storage_gb']} GB")
    print(f"✅ Sleep time: {config['sleep_minutes']} minutes")

    # 4. Batch size
    print(f"\nStep 4: Batch size")
    print(f"Number of files to transfer before pausing: {DEFAULT_CONFIG['batch_size']}")

    custom_batch = input("\nUse default? (y/n): ").lower()
    if custom_batch == 'n':
        try:
            batch = input(f"Batch size [{DEFAULT_CONFIG['batch_size']}]: ").strip()
            if batch:
                config['batch_size'] = int(batch)
        except ValueError:
            print("Invalid input, using default")

    print(f"✅ Batch size: {config['batch_size']}")

    # Save configuration
    print("\n" + "="*60)
    print("Configuration complete!")
    print("="*60)

    if save_config(config):
        print(f"\n✅ Configuration saved to {CONFIG_FILE}")
        print(f"\n📂 Put your photos/videos in: {config['source_folder']}/")
        print("🚀 Run PixelSync again to start syncing!\n")
    else:
        print("\n⚠️  Failed to save configuration")

    return config


def get_config(adb_path: str = 'adb') -> Dict[str, Any]:
    """Get configuration, running setup wizard if needed."""
    config = load_config()

    if config is None:
        print("No configuration found. Running setup wizard...\n")
        config = setup_wizard(adb_path)

    # Ensure source folder exists
    os.makedirs(config['source_folder'], exist_ok=True)

    return config


def reset_config() -> bool:
    """Delete existing configuration."""
    if os.path.exists(CONFIG_FILE):
        try:
            os.remove(CONFIG_FILE)
            print(f"✅ Configuration deleted: {CONFIG_FILE}")
            return True
        except Exception as e:
            print(f"❌ Error deleting config: {e}")
            return False
    else:
        print("No configuration file found")
        return True
