[app]
title = PDF to Speech Converter
package.name = pdftospeech
package.domain = com.example.pdftospeech

source.main = main.py
source.include_exts = py,png,jpg,kv,atlas

version = 1.0
version.name = 1.0

orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1

[requirements]
kivy>=2.1.0
python3
pyttsx3
pdfminer.six
Pillow
pyjnius
kivymd
requests
