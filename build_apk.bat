@echo off
REM PDF to Speech Android APK Build Script for Windows
REM This script builds the Android APK using buildozer

echo Starting PDF to Speech APK build process...

REM Check if buildozer is installed
where buildozer >nul 2>nul
if %errorlevel% neq 0 (
    echo Buildozer not found. Installing buildozer...
    pip install buildozer
)

REM Clean previous builds
echo Cleaning previous builds...
buildozer android clean

REM Update buildozer.spec if needed
echo Updating buildozer configuration...

REM Build the APK
echo Building APK (this may take a while)...
buildozer android debug

REM Check if build was successful
if exist "bin\pdftospeech-1.0-debug.apk" (
    echo ✅ APK built successfully!
    echo 📱 APK location: bin\pdftospeech-1.0-debug.apk
    echo 📁 You can download this file to your Android device
) else (
    echo ❌ APK build failed. Check the logs above for errors.
    exit /b 1
)

echo Build process completed!
pause
