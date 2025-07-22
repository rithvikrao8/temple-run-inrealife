#!/bin/bash
# Install systemd service for BerryPi Accelerometer Client
# This script creates a service that starts on boot and auto-restarts on crashes

set -e

echo "=== Installing BerryPi Accelerometer Client as Systemd Service ==="

# Get the current directory (where this script is located)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLIENT_SCRIPT="$SCRIPT_DIR/accelerometer_client.py"

# Check if the client script exists
if [ ! -f "$CLIENT_SCRIPT" ]; then
    echo "[ERROR] accelerometer_client.py not found in $SCRIPT_DIR"
    exit 1
fi

# Make the client script executable
chmod +x "$CLIENT_SCRIPT"

# Create the systemd service file
SERVICE_FILE="/etc/systemd/system/berrypi-accelerometer.service"

echo "Creating systemd service file..."

cat > "$SERVICE_FILE" << EOF
[Unit]
Description=BerryPi Accelerometer Client for Temple Run
After=network.target
Wants=network.target

[Service]
Type=simple
User=pi
Group=pi
WorkingDirectory=$SCRIPT_DIR
ExecStart=/usr/bin/python3 $CLIENT_SCRIPT
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

# Environment variables
Environment=PYTHONUNBUFFERED=1

# Security settings
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ReadWritePaths=$SCRIPT_DIR

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd to recognize the new service
echo "Reloading systemd..."
systemctl daemon-reload

# Enable the service to start on boot
echo "Enabling service to start on boot..."
systemctl enable berrypi-accelerometer.service

echo ""
echo "=== Service Installation Complete ==="
echo ""
echo "Service Details:"
echo "- Service Name: berrypi-accelerometer"
echo "- Status: Enabled (will start on boot)"
echo "- Auto-restart: Yes (5 second delay)"
echo "- Working Directory: $SCRIPT_DIR"
echo ""
echo "Useful Commands:"
echo "  sudo systemctl start berrypi-accelerometer    # Start the service"
echo "  sudo systemctl stop berrypi-accelerometer     # Stop the service"
echo "  sudo systemctl status berrypi-accelerometer   # Check service status"
echo "  sudo systemctl restart berrypi-accelerometer  # Restart the service"
echo "  sudo journalctl -u berrypi-accelerometer -f   # View live logs"
echo "  sudo journalctl -u berrypi-accelerometer      # View all logs"
echo ""
echo "The service will automatically:"
echo "- Start when the Raspberry Pi boots up"
echo "- Restart if the client crashes"
echo "- Log all output to systemd journal"
echo ""
echo "To start the service now, run:"
echo "  sudo systemctl start berrypi-accelerometer" 