#!/bin/bash
# Uninstall systemd service for BerryPi Accelerometer Client

set -e

echo "=== Uninstalling BerryPi Accelerometer Client Systemd Service ==="

SERVICE_NAME="berrypi-accelerometer"

# Stop the service if it's running
if systemctl is-active --quiet "$SERVICE_NAME"; then
    echo "Stopping service..."
    systemctl stop "$SERVICE_NAME"
fi

# Disable the service
if systemctl is-enabled --quiet "$SERVICE_NAME"; then
    echo "Disabling service..."
    systemctl disable "$SERVICE_NAME"
fi

# Remove the service file
SERVICE_FILE="/etc/systemd/system/$SERVICE_NAME.service"
if [ -f "$SERVICE_FILE" ]; then
    echo "Removing service file..."
    rm "$SERVICE_FILE"
fi

# Reload systemd
echo "Reloading systemd..."
systemctl daemon-reload

echo ""
echo "=== Service Uninstallation Complete ==="
echo "The berrypi-accelerometer service has been removed."
echo "The accelerometer client will no longer start automatically on boot." 