# PDF to Speech Android App

This Android application converts PDF files to speech audio files using text-to-speech technology.

## Features

- 📱 **Mobile-friendly interface** - Clean, intuitive UI designed for Android devices
- 📄 **PDF text extraction** - Extracts text from PDF files using pdfminer
- 🔊 **Text-to-Speech** - Converts extracted text to audio using pyttsx3
- ⚙️ **Customizable settings** - Adjust voice, speech rate, and volume
- 📊 **Progress tracking** - Real-time progress updates during conversion
- 💾 **File management** - Easy file selection and output management
- ⏸️ **Stop/Resume** - Ability to stop conversion process

## Building the APK

### Prerequisites

1. **Python 3.8+** installed
2. **Buildozer** for Android APK building
3. **Android SDK** and **NDK** (automatically handled by buildozer)

### Quick Build

1. **Install buildozer:**
   ```bash
   pip install buildozer
   ```

2. **Run the build script:**
   ```bash
   chmod +x build_apk.sh
   ./build_apk.sh
   ```

3. **Or build manually:**
   ```bash
   buildozer android debug
   ```

### Build Process

The build process will:
- Download and configure Android SDK/NDK
- Install Python dependencies
- Compile the Android APK
- Output the APK to `bin/pdftospeech-1.0-debug.apk`

## Installation

1. **Download the APK** from the `bin/` directory after building
2. **Enable "Unknown Sources"** in your Android device settings
3. **Install the APK** by tapping on it
4. **Grant permissions** when prompted (Storage, Audio)

## Usage

1. **Launch the app** from your Android device
2. **Select a PDF file** using the "Choose PDF" button
3. **Adjust settings** (voice, rate, volume) if desired
4. **Tap "Convert to Speech"** to start the process
5. **Monitor progress** in the status area
6. **Find audio files** in your device's storage under `PDFtoSpeech/output/`

## File Structure

```
├── main.py                 # Main Android application
├── buildozer.spec         # Buildozer configuration
├── requirements.txt       # Python dependencies
├── android_permissions.txt # Android permissions
├── build_apk.sh          # Build script
└── README_Android.md     # This file
```

## Dependencies

- **kivy** - Mobile UI framework
- **pyttsx3** - Text-to-speech engine
- **pdfminer.six** - PDF text extraction
- **Pillow** - Image processing
- **pyjnius** - Python-Java bridge for Android

## Troubleshooting

### Build Issues
- Ensure you have enough disk space (buildozer needs ~2GB)
- Check that Python 3.8+ is installed
- Verify internet connection for dependency downloads

### Runtime Issues
- Grant all required permissions
- Ensure PDF files are not password-protected
- Check available storage space for audio output

### Performance
- Large PDFs may take time to process
- Consider splitting very large files
- Monitor device storage during conversion

## Output

Audio files are saved as WAV format in:
- **Android**: `/storage/emulated/0/PDFtoSpeech/output/`
- **Files**: `page_XXXX_chunk_XX.wav`

## Notes

- The app works offline once built
- Supports most standard PDF files
- Audio quality depends on device TTS engine
- Progress is saved and can be resumed
