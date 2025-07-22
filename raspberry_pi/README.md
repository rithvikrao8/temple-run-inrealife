# Raspberry Pi BerryPi Accelerometer Setup

This directory contains the code and setup instructions for using a Raspberry Pi 2W with a BerryPi accelerometer card to control Temple Run.

## Hardware Requirements

- **Raspberry Pi 2W** (or any Raspberry Pi with WiFi)
- **BerryPi Accelerometer Card** (MPU6050-based)
- **MicroSD card** with Raspberry Pi OS
- **Power supply** for Raspberry Pi

## Hardware Connection

Connect the BerryPi accelerometer card to your Raspberry Pi:

1. **VCC** → 3.3V (Pin 1)
2. **GND** → Ground (Pin 6)
3. **SCL** → GPIO 3 (Pin 5) - I2C1 SCL
4. **SDA** → GPIO 2 (Pin 3) - I2C1 SDA

## Setup Instructions

### 1. Initial Setup

```bash
# Clone this repository to your Raspberry Pi
git clone https://github.com/rithvikrao8/temple-run-inrealife.git
cd temple-run-inrealife/raspberry_pi

# Make setup script executable
chmod +x setup.sh

# Run the setup script
./setup.sh
```

### 2. Configure Network

Update the server IP address in `accelerometer_client.py`:

```python
SERVER_IP = "192.168.1.100"  # Change to your computer's IP address
```

To find your computer's IP address:
- **Windows**: Run `ipconfig` in Command Prompt
- **Mac/Linux**: Run `ifconfig` or `ip addr` in Terminal

### 3. Test I2C Connection

```bash
# Check if the accelerometer is detected
i2cdetect -y 1
```

You should see the device at address `68` (MPU6050).

## Usage

### Option 1: Manual Running (for testing)

```bash
python3 accelerometer_client.py
```

The client will:
1. **Calibrate** the accelerometer (100 samples)
2. **Send data** to your computer at 50Hz
3. **Display** real-time X, Y, Z values

### Option 2: Install as Systemd Service (recommended for production)

Install the client as a systemd service that starts on boot and auto-restarts if it crashes:

```bash
# Install the service
sudo ./install_service.sh

# Start the service immediately
sudo systemctl start berrypi-accelerometer

# Check service status
sudo systemctl status berrypi-accelerometer

# View live logs
sudo journalctl -u berrypi-accelerometer -f
```

**Service Features:**
- ✅ **Auto-start on boot**
- ✅ **Auto-restart on crashes** (5-second delay)
- ✅ **Logging to systemd journal**
- ✅ **Runs as pi user** (no root privileges needed)

**Service Management Commands:**
```bash
sudo systemctl start berrypi-accelerometer    # Start the service
sudo systemctl stop berrypi-accelerometer     # Stop the service
sudo systemctl restart berrypi-accelerometer  # Restart the service
sudo systemctl status berrypi-accelerometer   # Check status
sudo journalctl -u berrypi-accelerometer -f   # View live logs
sudo journalctl -u berrypi-accelerometer      # View all logs
```

**To uninstall the service:**
```bash
sudo ./uninstall_service.sh
```

### Expected Output

```
=== BerryPi Accelerometer Client for Temple Run ===
Target server: 192.168.1.100:5001
Sample rate: 50 Hz

[INFO] BerryPi accelerometer initialized successfully
[INFO] Calibrating accelerometer with 100 samples...
[INFO] Calibration complete. Offsets: X=-0.023, Y=0.045, Z=-0.012
[INFO] Starting accelerometer client...
[INFO] Sending data to 192.168.1.100:5001
[INFO] Sample rate: 50 Hz
[INFO] Press Ctrl+C to stop
X:  0.123, Y: -0.045, Z:  0.234
```

## Troubleshooting

### I2C Device Not Found

1. **Check connections**: Ensure all wires are properly connected
2. **Enable I2C**: Run `sudo raspi-config` → Interface Options → I2C → Enable
3. **Check device**: Run `i2cdetect -y 1` to see if device appears at address `68`

### Connection Errors

1. **Check IP address**: Ensure SERVER_IP is correct
2. **Check network**: Both devices must be on same WiFi network
3. **Check firewall**: Ensure port 5001 is open on your computer
4. **Check server**: Make sure `accelerometer_server.py` is running on your computer

### Calibration Issues

1. **Keep sensor still** during calibration
2. **Check sensor orientation** - ensure it's mounted correctly
3. **Restart client** if calibration values look wrong

## Configuration

### Sample Rate

Change the sample rate in `accelerometer_client.py`:

```python
SAMPLE_RATE = 50  # Hz (50 samples per second)
```

### I2C Bus

If using a different I2C bus:

```python
BUS_NUMBER = 1  # Change to 0 for older Raspberry Pi models
```

### Accelerometer Range

The code is configured for ±2g range. For different ranges, modify the sensitivity in `read_accelerometer()`:

```python
# For ±4g range: use 8192.0 instead of 16384.0
# For ±8g range: use 4096.0 instead of 16384.0
# For ±16g range: use 2048.0 instead of 16384.0
```

## Performance Tips

1. **Use WiFi 5GHz** for better performance
2. **Reduce sample rate** if experiencing lag (try 25Hz)
3. **Keep Raspberry Pi cool** to maintain performance
4. **Use a good power supply** (2.5A or higher recommended)

## Files

- `accelerometer_client.py` - Main client code
- `requirements.txt` - Python dependencies
- `setup.sh` - Automated setup script
- `install_service.sh` - Install systemd service for auto-start/restart
- `uninstall_service.sh` - Remove systemd service
- `README.md` - This file 