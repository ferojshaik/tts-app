#!/bin/bash

# PDF to Speech Android APK Build Script
# This script builds the Android APK using buildozer

echo "Starting PDF to Speech APK build process..."

# Check if buildozer is installed
if ! command -v buildozer &> /dev/null; then
    echo "Buildozer not found. Installing buildozer..."
    pip install buildozer
fi

# Clean previous builds
echo "Cleaning previous builds..."
buildozer android clean

# Update buildozer.spec if needed
echo "Updating buildozer configuration..."

# Build the APK
echo "Building APK (this may take a while)..."
buildozer android debug

# Check if build was successful
if [ -f "bin/pdftospeech-1.0-debug.apk" ]; then
    echo "✅ APK built successfully!"
    echo "📱 APK location: bin/pdftospeech-1.0-debug.apk"
    echo "📁 You can download this file to your Android device"
else
    echo "❌ APK build failed. Check the logs above for errors."
    exit 1
fi

echo "Build process completed!"
