# PDF to Speech Android App - Build Guide

## Overview

This guide will help you build the PDF to Speech Android app into an APK file that you can install on your Android device.

## Prerequisites

### For Codespace (Recommended)
- GitHub Codespace with Ubuntu environment
- At least 4GB RAM and 2GB free disk space

### For Local Development
- Python 3.8+ installed
- Android SDK and NDK (or use buildozer to manage them)
- Git installed

## Quick Start (Codespace)

### 1. Open in Codespace
1. Open this repository in GitHub Codespace
2. Wait for the environment to initialize

### 2. Setup Environment
```bash
# Make setup script executable and run it
chmod +x setup_codespace.sh
./setup_codespace.sh
```

### 3. Activate Virtual Environment
```bash
source venv/bin/activate
```

### 4. Test the App
```bash
python test_app.py
```

### 5. Build APK
```bash
# Option 1: Use the build script
./build_apk.sh

# Option 2: Build manually
buildozer android debug
```

### 6. Download APK
The APK will be created in `bin/pdftospeech-1.0-debug.apk`. Download this file to your Android device.

## Manual Build Process

### 1. Install Dependencies

#### On Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv build-essential git wget unzip openjdk-11-jdk
pip3 install --user buildozer
```

#### On Windows:
```cmd
pip install buildozer
```

### 2. Initialize Buildozer
```bash
buildozer init
```

### 3. Configure Build (Optional)
Edit `buildozer.spec` to customize:
- App name and package
- Dependencies
- Permissions
- Icon and splash screen

### 4. Build APK
```bash
# Debug build (faster, larger file)
buildozer android debug

# Release build (smaller, optimized)
buildozer android release
```

## File Structure

```
├── main.py                 # Main Android application
├── buildozer.spec         # Buildozer configuration
├── requirements.txt       # Python dependencies
├── android_permissions.txt # Android permissions
├── build_apk.sh          # Linux/Mac build script
├── build_apk.bat         # Windows build script
├── setup_codespace.sh    # Codespace setup script
├── test_app.py           # Test script
├── README_Android.md     # App documentation
└── BUILD_GUIDE.md        # This file
```

## Configuration Files

### buildozer.spec
Main configuration file for the Android build:
- App metadata (name, version, package)
- Source files and dependencies
- Android-specific settings
- Permissions and features

### requirements.txt
Python packages needed for the app:
- kivy: Mobile UI framework
- pyttsx3: Text-to-speech engine
- pdfminer.six: PDF text extraction
- Additional Android dependencies

## Troubleshooting

### Common Build Issues

#### 1. "buildozer: command not found"
```bash
# Add to PATH
export PATH=$PATH:~/.local/bin
# Or reinstall
pip3 install --user buildozer
```

#### 2. "Java not found"
```bash
# Install Java
sudo apt-get install openjdk-11-jdk
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
```

#### 3. "Cython not found"
```bash
pip3 install --user Cython
```

#### 4. Build fails with memory error
- Increase Codespace memory to 8GB
- Close other applications
- Try building in smaller chunks

#### 5. "Permission denied" errors
```bash
# Fix file permissions
chmod +x *.sh
# Or run with sudo if necessary
```

### Runtime Issues

#### 1. App crashes on startup
- Check Android permissions
- Ensure all dependencies are installed
- Test with `python test_app.py`

#### 2. TTS not working
- Check device TTS settings
- Verify audio permissions
- Test with different voices

#### 3. PDF not loading
- Check file permissions
- Ensure PDF is not password-protected
- Verify file format

## Build Optimization

### Debug vs Release
- **Debug**: Faster build, larger APK, includes debug info
- **Release**: Slower build, smaller APK, optimized for production

### Reducing APK Size
1. Remove unused dependencies from `requirements.txt`
2. Use `--strip` option in buildozer
3. Optimize images and assets
4. Enable ProGuard for code shrinking

### Performance Tips
1. Use virtual environment to isolate dependencies
2. Clean build directory between builds
3. Use `buildozer android clean` before rebuilding
4. Monitor disk space during build

## Installation on Android

### 1. Enable Unknown Sources
- Go to Settings > Security > Unknown Sources
- Enable installation from unknown sources

### 2. Install APK
- Transfer APK to Android device
- Tap the APK file to install
- Grant required permissions when prompted

### 3. Required Permissions
- Storage (read/write)
- Audio (for TTS)
- Internet (for dependency downloads)

## Advanced Configuration

### Custom Icon
1. Add `icon.png` (512x512) to project root
2. Update `buildozer.spec`:
   ```
   [app]
   icon.filename = icon.png
   ```

### Custom Splash Screen
1. Add `splash.png` to project root
2. Update `buildozer.spec`:
   ```
   [app]
   splash.filename = splash.png
   ```

### Additional Permissions
Edit `android_permissions.txt` and `buildozer.spec` to add more permissions as needed.

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review buildozer logs in `.buildozer/`
3. Test individual components with `test_app.py`
4. Ensure all dependencies are properly installed

## Next Steps

After successful build:
1. Test the APK on your Android device
2. Customize the UI and functionality as needed
3. Consider creating a release build for distribution
4. Add app icon and splash screen for better user experience
