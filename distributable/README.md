# PixelSync - Unlimited Google Photos Backup

PixelSync helps you backup unlimited photos and videos to Google Photos using a Pixel phone's unlimited original quality storage.

## How It Works

1. Put your photos/videos from iPhone/camera in the `Photos_To_Sync` folder
2. PixelSync transfers them to your Pixel phone
3. Google Photos automatically backs them up (unlimited original quality on Pixel Gen 1)
4. Use "Free up space" in Google Photos to remove them from Pixel
5. Repeat!

## First Time Setup

### Prerequisites

1. **Pixel Phone** (Gen 1 with unlimited Google Photos backup)
2. **USB Cable** to connect Pixel to your computer
3. **USB Debugging** enabled on Pixel:
   - Go to Settings → About Phone
   - Tap "Build Number" 7 times to enable Developer Options
   - Go to Settings → System → Developer Options
   - Enable "USB Debugging"

### Installation

1. **Download** the PixelSync package for your platform:
   - **macOS**: `PixelSync_macOS.zip`
   - **Windows**: `PixelSync_Windows.zip`

2. **Extract** the zip file to a folder on your computer

3. **Run PixelSync** for the first time:
   - **macOS**: Double-click `PixelSync.app` (or run `./PixelSync` in Terminal)
   - **Windows**: Double-click `PixelSync.exe`

4. **Follow the setup wizard**:
   - Connect your Pixel phone via USB
   - The wizard will detect your device
   - Configure settings (or use defaults)
   - Setup complete!

## How to Use

### Regular Usage

1. **Put files to sync** in the `Photos_To_Sync` folder
   - Supported formats: HEIC, MOV, JPG, PNG, MP4, GIF
   - Unsupported files (.AAE, .XMP, .DNG) are automatically deleted

2. **Connect your Pixel** via USB (if not already connected)

3. **Run PixelSync**
   - **macOS**: Double-click `PixelSync.app`
   - **Windows**: Double-click `PixelSync.exe`

4. **Wait for sync** to complete
   - Files are transferred in batches
   - Progress is shown in real-time
   - Files are deleted from your computer after successful transfer

5. **On your Pixel**:
   - Open Google Photos app
   - Wait for backup to complete
   - Go to Settings → "Free up space" to remove local copies
   - Your files are now safely backed up to Google Photos!

## Configuration

### Settings

Configuration is stored in `pixelsync_config.json`. You can edit this file directly or reset it:

```bash
# Reset configuration and run setup wizard again
./PixelSync --reset  # macOS/Linux
PixelSync.exe --reset  # Windows
```

### Default Settings

- **Batch Size**: 50 files (number of files transferred before pausing)
- **Max Storage**: 10 GB (max storage on Pixel before pausing to wait for backup)
- **Sleep Time**: 15 minutes (wait time when storage is full)
- **Source Folder**: `Photos_To_Sync`

## Troubleshooting

### "No device connected"

- Make sure USB debugging is enabled on your Pixel
- Check if USB cable is properly connected
- On Pixel, tap "Allow" when prompted to authorize your computer
- Try a different USB cable or port

### "Device unauthorized"

- Disconnect and reconnect the USB cable
- On your Pixel, tap "Always allow from this computer" when prompted

### Google Photos not detecting files

- Force stop Google Photos app on Pixel
- Reopen Google Photos
- Wait 1-2 minutes for scanning
- Check backup status in Google Photos settings

### Files not transferring

- Check that files are in the correct folder (`Photos_To_Sync`)
- Make sure files are supported formats (HEIC, MOV, JPG, PNG, MP4, GIF)
- Ensure there's enough storage on your Pixel
- Check that USB debugging is still enabled

## Advanced Usage

### Command Line Options

```bash
pixelsync          # Run normal sync
pixelsync --reset  # Reset configuration
pixelsync --help   # Show help
```

### File Type Management

Edit `pixelsync_config.json` to customize which file types to keep or delete:

```json
{
  "keep_extensions": [".heic", ".mov", ".jpg", ".png", ".mp4"],
  "delete_extensions": [".aae", ".xmp", ".zip", ".dng"]
}
```

## Tips

1. **Large transfers**: For thousands of files, run PixelSync overnight
2. **Storage management**: Regularly use "Free up space" in Google Photos to keep Pixel storage available
3. **Batch size**: Reduce batch size if your Pixel freezes during transfer
4. **Multiple devices**: PixelSync will prompt you to choose if multiple Android devices are connected

## Support

If you encounter issues:

1. Try resetting configuration: `pixelsync --reset`
2. Check USB debugging is enabled
3. Restart both your computer and Pixel
4. Make sure Google Photos app is up to date on Pixel

## Building from Source

If you want to build PixelSync yourself:

```bash
# Install dependencies
pip install -r requirements.txt

# Download platform tools (adb) and extract to adb/ folder

# Build executable
pyinstaller build.spec

# Output will be in dist/ folder
```

---

**Enjoy unlimited photo backup! 📸☁️**
