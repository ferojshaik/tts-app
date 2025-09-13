#!/bin/bash

# Setup script for PDF to Speech Android app in Codespace
echo "Setting up PDF to Speech Android development environment..."

# Update system packages
echo "Updating system packages..."
sudo apt-get update

# Install required system dependencies
echo "Installing system dependencies..."
sudo apt-get install -y \
    python3-pip \
    python3-venv \
    build-essential \
    git \
    wget \
    unzip \
    openjdk-11-jdk \
    zlib1g-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libreadline6-dev \
    libssl-dev \
    libsqlite3-dev \
    libgdbm-dev \
    libbz2-dev \
    liblzma-dev \
    libffi-dev \
    uuid-dev

# Set JAVA_HOME
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
echo 'export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64' >> ~/.bashrc

# Install buildozer
echo "Installing buildozer..."
pip3 install --user buildozer

# Add user bin to PATH
echo 'export PATH=$PATH:~/.local/bin' >> ~/.bashrc
export PATH=$PATH:~/.local/bin

# Install Cython (required for buildozer)
echo "Installing Cython..."
pip3 install --user Cython

# Create virtual environment for the project
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Initialize buildozer
echo "Initializing buildozer..."
buildozer init

echo "✅ Setup complete!"
echo ""
echo "To build the APK, run:"
echo "  source venv/bin/activate"
echo "  ./build_apk.sh"
echo ""
echo "Or manually:"
echo "  buildozer android debug"
