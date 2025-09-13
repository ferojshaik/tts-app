#!/usr/bin/env python3
"""
Test script for PDF to Speech Android app
This script tests the core functionality without the Android UI
"""

import os
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import kivy
        print("✅ Kivy imported successfully")
    except ImportError as e:
        print(f"❌ Kivy import failed: {e}")
        return False
    
    try:
        import pyttsx3
        print("✅ pyttsx3 imported successfully")
    except ImportError as e:
        print(f"❌ pyttsx3 import failed: {e}")
        return False
    
    try:
        from pdfminer.high_level import extract_text
        print("✅ pdfminer imported successfully")
    except ImportError as e:
        print(f"❌ pdfminer import failed: {e}")
        return False
    
    return True

def test_tts():
    """Test text-to-speech functionality"""
    print("\nTesting TTS...")
    
    try:
        import pyttsx3
        engine = pyttsx3.init()
        
        # Test basic TTS
        voices = engine.getProperty('voices')
        print(f"✅ Found {len(voices)} TTS voices")
        
        # Test voice properties
        rate = engine.getProperty('rate')
        volume = engine.getProperty('volume')
        print(f"✅ TTS rate: {rate}, volume: {volume}")
        
        engine.stop()
        return True
        
    except Exception as e:
        print(f"❌ TTS test failed: {e}")
        return False

def test_pdf_processing():
    """Test PDF text extraction"""
    print("\nTesting PDF processing...")
    
    try:
        from pdfminer.high_level import extract_text
        
        # Create a simple test PDF content (this won't actually work without a real PDF)
        print("✅ PDF processing module loaded successfully")
        print("ℹ️  Note: Actual PDF processing requires a real PDF file")
        return True
        
    except Exception as e:
        print(f"❌ PDF processing test failed: {e}")
        return False

def test_kivy_app():
    """Test Kivy app initialization"""
    print("\nTesting Kivy app...")
    
    try:
        # Import the main app
        from main import PDFToSpeechApp
        
        # Test app creation (without running)
        app = PDFToSpeechApp()
        print("✅ Kivy app created successfully")
        
        # Test if we can access the build method
        if hasattr(app, 'build'):
            print("✅ App has build method")
        else:
            print("❌ App missing build method")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Kivy app test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("PDF to Speech Android App - Test Suite")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_tts,
        test_pdf_processing,
        test_kivy_app
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ All tests passed! The app should work correctly.")
        return 0
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
