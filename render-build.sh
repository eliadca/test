#!/usr/bin/env bash

# Install wkhtmltopdf and other required libraries
echo "Installing system dependencies..."
apt-get update && apt-get install -y \
    wkhtmltopdf \
    libxrender1 \
    libxext6 \
    libfontconfig1

# Install Python dependencies
pip install -r requirements.txt
