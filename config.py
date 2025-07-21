# Configuration file for accelerometer-based Temple Run game

# Accelerometer sensitivity thresholds
# Adjust these values based on your device's sensitivity
X_THRESHOLD = 0.3    # Left/Right tilt sensitivity (higher = less sensitive)
Y_THRESHOLD = 0.3    # Forward/Backward tilt sensitivity (higher = less sensitive)
Z_THRESHOLD = 0.3    # Up/Down movement sensitivity (higher = less sensitive)

# Network configuration
SERVER_PORT = 5001   # UDP port for receiving accelerometer data
WEB_PORT = 5000      # HTTP port for web interface

# Game control settings
WAIT_TIME = 0.1      # Minimum time between key presses (seconds)
PROCESSING_DELAY = 0.05  # Delay in accelerometer processing loop (seconds)

# Visualization settings
CANVAS_WIDTH = 640
CANVAS_HEIGHT = 480

# 3D Plane Control Mapping
# X-axis: Left/Right movement
# Y-axis: Forward movement (positive Y = Jump)
# Z-axis: Downward movement (negative Z = Slide)

# Control mapping for 3D plane:
# Tilt left:  x < -X_THRESHOLD  -> "left"
# Tilt right: x > X_THRESHOLD   -> "right"
# Move forward (leg up): y > Y_THRESHOLD -> "up" (jump)
# Move downward (leg down): z < -Z_THRESHOLD -> "down" (slide)

# Example accelerometer values for 3D plane:
# Move leg left:  x < -X_THRESHOLD  -> "left"
# Move leg right: x > X_THRESHOLD   -> "right"
# Lift leg up: y > Y_THRESHOLD -> "up" (jump)
# Move leg down: z < -Z_THRESHOLD -> "down" (slide) 