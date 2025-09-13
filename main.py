# main.py - Android PDF to Speech App
import os
import json
import logging
import re
import threading
import time
from pathlib import Path
from typing import List
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.progressbar import ProgressBar
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.slider import Slider
from kivy.clock import Clock
from kivy.utils import platform
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner

# Android-specific imports
if platform == 'android':
    from android.permissions import request_permissions, Permission
    from android.storage import primary_external_storage_path
    from jnius import autoclass
    from android import activity

# PDF processing
try:
    from pdfminer.high_level import extract_text
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

# TTS
try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger("pdf_tts_android")

class PDFToSpeechApp(App):
    def build(self):
        # Request Android permissions
        if platform == 'android':
            self.request_android_permissions()
        
        # Set window size for better mobile experience
        Window.size = (400, 600)
        
        # Main layout
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Title
        title = Label(
            text='PDF to Speech Converter',
            size_hint_y=None,
            height=50,
            font_size=24,
            bold=True
        )
        main_layout.add_widget(title)
        
        # File selection
        file_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        self.file_input = TextInput(
            hint_text='Select PDF file...',
            multiline=False,
            readonly=True
        )
        self.file_button = Button(
            text='Choose PDF',
            size_hint_x=None,
            width=100
        )
        self.file_button.bind(on_press=self.show_file_chooser)
        file_layout.add_widget(self.file_input)
        file_layout.add_widget(self.file_button)
        main_layout.add_widget(file_layout)
        
        # Voice settings
        voice_layout = GridLayout(cols=2, size_hint_y=None, height=120, spacing=10)
        
        # Voice selection
        voice_layout.add_widget(Label(text='Voice:', size_hint_x=None, width=100))
        self.voice_spinner = Spinner(
            text='Default',
            values=['Default'],
            size_hint_x=None,
            width=200
        )
        voice_layout.add_widget(self.voice_spinner)
        
        # Speech rate
        voice_layout.add_widget(Label(text='Rate:', size_hint_x=None, width=100))
        rate_layout = BoxLayout(orientation='horizontal')
        self.rate_slider = Slider(min=50, max=300, value=175, step=5)
        self.rate_label = Label(text='175 WPM', size_hint_x=None, width=80)
        self.rate_slider.bind(value=self.on_rate_change)
        rate_layout.add_widget(self.rate_slider)
        rate_layout.add_widget(self.rate_label)
        voice_layout.add_widget(rate_layout)
        
        # Volume
        voice_layout.add_widget(Label(text='Volume:', size_hint_x=None, width=100))
        volume_layout = BoxLayout(orientation='horizontal')
        self.volume_slider = Slider(min=0.1, max=1.0, value=1.0, step=0.1)
        self.volume_label = Label(text='100%', size_hint_x=None, width=80)
        self.volume_slider.bind(value=self.on_volume_change)
        volume_layout.add_widget(self.volume_slider)
        volume_layout.add_widget(self.volume_label)
        voice_layout.add_widget(volume_layout)
        
        main_layout.add_widget(voice_layout)
        
        # Progress
        self.progress_label = Label(
            text='Ready to convert',
            size_hint_y=None,
            height=30
        )
        main_layout.add_widget(self.progress_label)
        
        self.progress_bar = ProgressBar(
            max=100,
            value=0,
            size_hint_y=None,
            height=30
        )
        main_layout.add_widget(self.progress_bar)
        
        # Control buttons
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        
        self.convert_button = Button(text='Convert to Speech')
        self.convert_button.bind(on_press=self.start_conversion)
        self.convert_button.disabled = not PDF_AVAILABLE or not TTS_AVAILABLE
        
        self.stop_button = Button(text='Stop', disabled=True)
        self.stop_button.bind(on_press=self.stop_conversion)
        
        button_layout.add_widget(self.convert_button)
        button_layout.add_widget(self.stop_button)
        main_layout.add_widget(button_layout)
        
        # Status text
        self.status_text = TextInput(
            text='App ready. Select a PDF file to begin.',
            multiline=True,
            readonly=True,
            size_hint_y=0.3
        )
        main_layout.add_widget(self.status_text)
        
        # Initialize TTS engine
        self.tts_engine = None
        self.conversion_thread = None
        self.stop_conversion_flag = False
        self.selected_file = None
        
        # Load available voices
        self.load_voices()
        
        return main_layout
    
    def request_android_permissions(self):
        """Request necessary Android permissions"""
        permissions = [
            Permission.READ_EXTERNAL_STORAGE,
            Permission.WRITE_EXTERNAL_STORAGE,
            Permission.RECORD_AUDIO
        ]
        request_permissions(permissions)
    
    def load_voices(self):
        """Load available TTS voices"""
        if not TTS_AVAILABLE:
            return
        
        try:
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            voice_names = ['Default']
            
            for i, voice in enumerate(voices):
                name = getattr(voice, 'name', f'Voice {i}')
                voice_names.append(f'{i}: {name}')
            
            self.voice_spinner.values = voice_names
            engine.stop()
        except Exception as e:
            self.log_message(f"Error loading voices: {e}")
    
    def on_rate_change(self, instance, value):
        """Update rate label when slider changes"""
        self.rate_label.text = f'{int(value)} WPM'
    
    def on_volume_change(self, instance, value):
        """Update volume label when slider changes"""
        self.volume_label.text = f'{int(value * 100)}%'
    
    def show_file_chooser(self, instance):
        """Show file chooser for PDF selection"""
        content = BoxLayout(orientation='vertical', spacing=10)
        
        file_chooser = FileChooserListView(
            path=self.get_documents_path(),
            filters=['*.pdf']
        )
        
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        
        select_button = Button(text='Select')
        select_button.bind(on_press=lambda x: self.select_file(file_chooser, popup))
        
        cancel_button = Button(text='Cancel')
        cancel_button.bind(on_press=lambda x: popup.dismiss())
        
        button_layout.add_widget(select_button)
        button_layout.add_widget(cancel_button)
        
        content.add_widget(file_chooser)
        content.add_widget(button_layout)
        
        popup = Popup(
            title='Select PDF File',
            content=content,
            size_hint=(0.9, 0.9)
        )
        popup.open()
    
    def get_documents_path(self):
        """Get the documents directory path"""
        if platform == 'android':
            try:
                return primary_external_storage_path()
            except:
                return '/storage/emulated/0/Download'
        else:
            return str(Path.home() / 'Downloads')
    
    def select_file(self, file_chooser, popup):
        """Handle file selection"""
        if file_chooser.selection:
            self.selected_file = file_chooser.selection[0]
            self.file_input.text = os.path.basename(self.selected_file)
            self.log_message(f"Selected: {self.selected_file}")
        popup.dismiss()
    
    def log_message(self, message):
        """Add message to status text"""
        self.status_text.text += f"\n{message}"
        # Auto-scroll to bottom
        self.status_text.cursor = (len(self.status_text.text), 0)
    
    def start_conversion(self, instance):
        """Start PDF to speech conversion"""
        if not self.selected_file:
            self.log_message("Please select a PDF file first")
            return
        
        if not os.path.exists(self.selected_file):
            self.log_message("Selected file does not exist")
            return
        
        self.convert_button.disabled = True
        self.stop_button.disabled = False
        self.stop_conversion_flag = False
        
        # Start conversion in a separate thread
        self.conversion_thread = threading.Thread(target=self.convert_pdf_to_speech)
        self.conversion_thread.daemon = True
        self.conversion_thread.start()
    
    def stop_conversion(self, instance):
        """Stop the conversion process"""
        self.stop_conversion_flag = True
        self.log_message("Stopping conversion...")
    
    def convert_pdf_to_speech(self):
        """Convert PDF to speech (runs in separate thread)"""
        try:
            # Initialize TTS engine
            if not TTS_AVAILABLE:
                Clock.schedule_once(lambda dt: self.log_message("TTS not available"))
                return
            
            self.tts_engine = pyttsx3.init()
            
            # Set voice
            if self.voice_spinner.text != 'Default':
                try:
                    voice_index = int(self.voice_spinner.text.split(':')[0])
                    voices = self.tts_engine.getProperty('voices')
                    self.tts_engine.setProperty('voice', voices[voice_index].id)
                except:
                    pass
            
            # Set rate and volume
            self.tts_engine.setProperty('rate', int(self.rate_slider.value))
            self.tts_engine.setProperty('volume', self.volume_slider.value)
            
            # Extract text from PDF
            Clock.schedule_once(lambda dt: self.log_message("Extracting text from PDF..."))
            pages = self.read_pdf_pages(self.selected_file)
            
            if not pages:
                Clock.schedule_once(lambda dt: self.log_message("No text found in PDF"))
                return
            
            # Create output directory
            output_dir = self.get_output_directory()
            os.makedirs(output_dir, exist_ok=True)
            
            # Convert each page
            total_pages = len(pages)
            for i, page_text in enumerate(pages):
                if self.stop_conversion_flag:
                    break
                
                # Update progress
                progress = (i / total_pages) * 100
                Clock.schedule_once(lambda dt, p=progress: self.update_progress(p))
                Clock.schedule_once(lambda dt, p=i+1, t=total_pages: self.log_message(f"Processing page {p}/{t}"))
                
                # Clean and process text
                clean_text = self.normalize_text(page_text)
                if not clean_text:
                    continue
                
                # Split into chunks
                chunks = self.split_into_chunks(clean_text)
                
                # Generate audio for each chunk
                for j, chunk in enumerate(chunks):
                    if self.stop_conversion_flag:
                        break
                    
                    output_file = os.path.join(output_dir, f"page_{i+1:04d}_chunk_{j+1:02d}.wav")
                    self.tts_save(chunk, output_file)
                
                Clock.schedule_once(lambda dt, p=i+1: self.log_message(f"Completed page {p}"))
            
            if not self.stop_conversion_flag:
                Clock.schedule_once(lambda dt: self.log_message(f"Conversion complete! Files saved to: {output_dir}"))
                Clock.schedule_once(lambda dt: self.update_progress(100))
            else:
                Clock.schedule_once(lambda dt: self.log_message("Conversion stopped by user"))
        
        except Exception as e:
            Clock.schedule_once(lambda dt, error=str(e): self.log_message(f"Error: {error}"))
        
        finally:
            # Reset UI
            Clock.schedule_once(lambda dt: self.reset_ui())
            if self.tts_engine:
                self.tts_engine.stop()
    
    def read_pdf_pages(self, pdf_path):
        """Extract text from PDF pages"""
        if not PDF_AVAILABLE:
            return []
        
        try:
            full_text = extract_text(pdf_path)
            pages = full_text.split('\f')
            return [p for p in pages if p.strip()]
        except Exception as e:
            self.log_message(f"Error reading PDF: {e}")
            return []
    
    def normalize_text(self, text):
        """Clean up text formatting"""
        text = text.replace('\r', '\n')
        text = re.sub(r'[ \t]+', ' ', text)
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = '\n'.join(line.strip() for line in text.splitlines())
        return text.strip()
    
    def split_into_chunks(self, text, max_chars=1500):
        """Split text into TTS-friendly chunks"""
        if not text:
            return []
        
        sentences = re.split(r'(?<=[.!?])\s+', text)
        chunks = []
        buf = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            if len(sentence) > max_chars:
                # Split long sentences
                start = 0
                while start < len(sentence):
                    end = min(start + max_chars, len(sentence))
                    chunks.append(sentence[start:end])
                    start = end
                continue
            
            tentative = ' '.join(buf + [sentence]).strip()
            if len(tentative) <= max_chars:
                buf.append(sentence)
            else:
                if buf:
                    chunks.append(' '.join(buf).strip())
                buf = [sentence]
        
        if buf:
            chunks.append(' '.join(buf).strip())
        
        return [c for c in chunks if c.strip()]
    
    def tts_save(self, text, output_file):
        """Save text to speech as WAV file"""
        try:
            self.tts_engine.save_to_file(text, output_file)
            self.tts_engine.runAndWait()
        except Exception as e:
            self.log_message(f"TTS error: {e}")
    
    def get_output_directory(self):
        """Get output directory for audio files"""
        if platform == 'android':
            base_path = primary_external_storage_path()
            return os.path.join(base_path, 'PDFtoSpeech', 'output')
        else:
            return os.path.join(os.path.expanduser('~'), 'PDFtoSpeech', 'output')
    
    def update_progress(self, value):
        """Update progress bar"""
        self.progress_bar.value = value
        self.progress_label.text = f'Progress: {int(value)}%'
    
    def reset_ui(self):
        """Reset UI after conversion"""
        self.convert_button.disabled = False
        self.stop_button.disabled = True
        self.progress_bar.value = 0
        self.progress_label.text = 'Ready to convert'

if __name__ == '__main__':
    PDFToSpeechApp().run()
