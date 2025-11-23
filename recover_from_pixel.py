#!/usr/bin/env python3
"""
Recovery script to pull files back from Pixel to Mac for manual verification.
Use this when Google Photos doesn't detect files properly.
"""

from pixel_transfer import transfer_files_from_pixel

# Configuration
PIXEL_PATH = '/sdcard/DCIM/Camera/'
MAC_RECOVERY_FOLDER = '02_files_to_doublecheck'
DEVICE_ID = 'HT6940202447'

if __name__ == "__main__":
    print("="*60)
    print("Pixel → Mac Recovery Tool")
    print("Pull files back from Pixel for manual verification")
    print("="*60)
    print()
    print("⚠️  WARNING: This will move ALL files from Pixel Camera to Mac!")
    print("   The files will be DELETED from Pixel after transfer.")
    print()

    response = input("Are you sure you want to continue? (yes/no): ")

    if response.lower() != 'yes':
        print("❌ Recovery cancelled.")
        exit(0)

    print("\n🔄 Starting recovery process...\n")

    success = transfer_files_from_pixel(
        pixel_path=PIXEL_PATH,
        mac_path=MAC_RECOVERY_FOLDER,
        device_id=DEVICE_ID
    )

    if success:
        print("\n✅ Recovery complete!")
        print(f"\n📂 Files are now in: {MAC_RECOVERY_FOLDER}/")
        print("\n📝 Next steps:")
        print("   1. Check each file in Finder")
        print("   2. Search for them manually in Google Photos web/app")
        print("   3. Delete files from this folder once verified in Google Photos")
        print("   4. Or re-transfer files that weren't backed up\n")
    else:
        print("\n⚠️  Some files failed to transfer. Check the errors above.")
