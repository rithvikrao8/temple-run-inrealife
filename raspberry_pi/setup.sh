#!/bin/bash
# Raspberry Pi Setup Script for BerryPi Accelerometer
# Run this script on your Raspberry Pi to set up the accelerometer

echo "=== Raspberry Pi BerryPi Accelerometer Setup ==="

# Update system
echo "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Enable I2C interface
echo "Enabling I2C interface..."
sudo raspi-config nonint do_i2c 0

# Install Python dependencies
echo "Installing Python dependencies..."
sudo apt install -y python3-pip python3-dev
pip3 install -r requirements.txt

# Install I2C tools for debugging
echo "Installing I2C tools..."
sudo apt install -y i2c-tools

# Check I2C devices
echo "Checking I2C devices..."
i2cdetect -y 1

echo ""
echo "=== Setup Complete ==="
echo "To test the accelerometer, run:"
echo "  python3 accelerometer_client.py"
echo ""
echo "Make sure to:"
echo "1. Update SERVER_IP in accelerometer_client.py to your computer's IP"
echo "2. Connect the BerryPi accelerometer card to the I2C pins"
echo "3. Ensure both devices are on the same WiFi network" 