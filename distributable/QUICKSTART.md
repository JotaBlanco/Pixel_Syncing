# PixelSync Quick Start Guide

## What You Need

✅ A Pixel phone (Gen 1) with unlimited Google Photos backup
✅ A USB cable
✅ Your computer (Mac or Windows)
✅ Photos/videos you want to backup

## Setup (First Time Only)

### 1. Enable USB Debugging on Your Pixel

1. Open **Settings** on your Pixel
2. Go to **About Phone**
3. Tap **Build Number** 7 times (you'll see "You are now a developer!")
4. Go back to **Settings** → **System** → **Developer Options**
5. Turn on **USB Debugging**

### 2. Install PixelSync

1. Download `PixelSync_macOS.zip` (Mac) or `PixelSync_Windows.zip` (Windows)
2. Extract the zip file
3. Open the extracted folder

### 3. First Run

1. **Connect your Pixel** to computer via USB cable
2. **On your Pixel**: Tap "Allow" when it asks to allow USB debugging
3. **Run PixelSync**:
   - **Mac**: Double-click `PixelSync` (or `PixelSync.app`)
   - **Windows**: Double-click `PixelSync.exe`
4. **Follow the setup wizard**:
   - It will detect your Pixel automatically
   - Press Enter to accept default settings (recommended)
   - Setup complete!

## Daily Use

### Every Time You Want to Backup Photos:

1. **Put your photos/videos** in the `Photos_To_Sync` folder
   - Just drag and drop your iPhone photos export here

2. **Connect your Pixel** via USB (if not connected)

3. **Run PixelSync** (double-click the app)

4. **Press Enter** to start the sync

5. **Wait** - PixelSync will:
   - Transfer files to your Pixel
   - Delete them from your computer (they're on Pixel now!)
   - Show progress as it works

6. **On your Pixel**:
   - Open **Google Photos** app
   - Wait for the backup to complete (you'll see it uploading)
   - Go to **Settings** (in Google Photos) → **Free up space**
   - This deletes the local copies from Pixel (they're in the cloud now!)

7. **Done!** Your photos are backed up to Google Photos with unlimited original quality! 🎉

## Tips

💡 **First time?** Start with just a few photos to test
💡 **Got thousands of photos?** Leave it running overnight
💡 **Pixel storage full?** PixelSync will pause - just use "Free up space" in Google Photos
💡 **Want to change settings?** Run `PixelSync --reset` to start setup again

## Common Issues

### "No device connected"
- Check USB cable is plugged in
- Make sure USB debugging is enabled
- Try tapping "Allow" again on your Pixel

### "Photos not showing in Google Photos"
- Force stop Google Photos app on Pixel
- Open it again
- Wait a minute for it to scan
- Check Settings → Backup status

### "Pixel storage full"
- Open Google Photos on Pixel
- Go to Settings → Free up space
- PixelSync will continue automatically

## Need Help?

Check the full README.md for detailed instructions and troubleshooting.

---

**That's it! Enjoy your unlimited photo backup! 📸☁️**
