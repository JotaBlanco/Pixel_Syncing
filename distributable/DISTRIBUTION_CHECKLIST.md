# Distribution Checklist

Use this checklist when preparing PixelSync for your friend.

## Pre-Build

- [ ] Decide which platform(s) to build for:
  - [ ] macOS (if your friend uses Mac)
  - [ ] Windows (if your friend uses Windows)
  - [ ] Linux (if needed)

## Download ADB

### For macOS Build:
- [ ] Download: https://dl.google.com/android/repository/platform-tools-latest-darwin.zip
- [ ] Extract and copy `adb` to `adb/mac/adb`
- [ ] Make executable: `chmod +x adb/mac/adb`

### For Windows Build:
- [ ] Download: https://dl.google.com/android/repository/platform-tools-latest-windows.zip
- [ ] Extract and copy these files to `adb/windows/`:
  - [ ] `adb.exe`
  - [ ] `AdbWinApi.dll`
  - [ ] `AdbWinUsbApi.dll`

### For Linux Build (optional):
- [ ] Download: https://dl.google.com/android/repository/platform-tools-latest-linux.zip
- [ ] Extract and copy `adb` to `adb/linux/adb`
- [ ] Make executable: `chmod +x adb/linux/adb`

## Build

- [ ] Install PyInstaller: `pip install pyinstaller`
- [ ] Run build script:
  - [ ] macOS: `./build.sh`
  - [ ] Windows: `build.bat`
- [ ] Check `dist/` folder for executable
- [ ] Test executable on your machine

## Test

- [ ] Create test folder and copy executable
- [ ] Run setup wizard
- [ ] Test with a few sample files
- [ ] Verify files transfer to Pixel
- [ ] Check config saves correctly
- [ ] Test `--reset` flag
- [ ] Test `--help` flag

## Package

### For macOS:
- [ ] Create folder: `PixelSync_macOS`
- [ ] Copy `dist/PixelSync` to folder
- [ ] Copy `README.md` to folder
- [ ] Copy `QUICKSTART.md` to folder
- [ ] Zip: `zip -r PixelSync_macOS.zip PixelSync_macOS/`
- [ ] Test zip extracts correctly

### For Windows:
- [ ] Create folder: `PixelSync_Windows`
- [ ] Copy `dist/PixelSync.exe` to folder
- [ ] Copy `README.md` to folder
- [ ] Copy `QUICKSTART.md` to folder
- [ ] Create zip file
- [ ] Test zip extracts correctly

## Final Checks

- [ ] Executable runs without Python installed
- [ ] Setup wizard works
- [ ] Device detection works
- [ ] File transfer works
- [ ] Config persistence works
- [ ] Error messages are clear
- [ ] Documentation is accurate

## Share with Friend

- [ ] Send them the zip file
- [ ] Point them to QUICKSTART.md
- [ ] Explain the basic workflow:
  1. Enable USB debugging (one time)
  2. Run setup wizard (first time)
  3. Drop files in folder → Run PixelSync → Free up space
- [ ] Be available for questions!

## Post-Distribution

- [ ] Ask for feedback
- [ ] Fix any issues they encounter
- [ ] Update documentation if needed
- [ ] Consider improvements for next version

## File Sizes to Expect

- macOS: ~40-50 MB
- Windows: ~35-45 MB
- Linux: ~40-50 MB

(These are normal - they include Python runtime + adb binaries)

## Common Issues to Prepare For

1. **Antivirus false positive**
   - PyInstaller executables sometimes trigger antivirus
   - Solution: Add exception or sign the executable

2. **"USB debugging not working"**
   - They might need to revoke USB debugging authorizations
   - Solution: Developer Options → Revoke USB debugging → Reconnect

3. **"Can't find config file"**
   - They ran executable from different location
   - Solution: Always run from same folder

4. **"Files not transferring"**
   - Wrong folder or unsupported file types
   - Solution: Check they're using `Photos_To_Sync` folder

## Notes

- First-time users should start with just 10-20 photos to test
- Encourage them to read QUICKSTART.md before starting
- Remind them to regularly use "Free up space" in Google Photos
- Device ID is saved in config, so they don't need to find it again

---

Good luck! 🚀
