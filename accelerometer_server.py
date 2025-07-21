# Accelerometer Server for Temple Run Game Control
# Receives accelerometer data from WiFi-connected device and controls game movements
# Uses 3D plane movement: +Y (Jump) and -Z (Slide)

import socket
import json
import threading
import time
import pyautogui
from flask import Flask, render_template, Response
import cv2
import numpy as np
from config import *

app = Flask(__name__)

# Global variables for accelerometer data
accelerometer_data = {
    'x': 0.0,  # Left/Right tilt
    'y': 0.0,  # Forward/Backward tilt
    'z': 0.0,  # Up/Down movement
    'timestamp': time.time()
}

# Game control variables
current_action = None
action_lock = threading.Lock()
start = time.time()  # Initialize start variable

# By default each key press is followed by a 0.1 second pause
pyautogui.PAUSE = 0.0

# Create a blank canvas for visualization
W = CANVAS_WIDTH
H = CANVAS_HEIGHT
canvas = np.zeros((H, W, 3), dtype=np.uint8)

# Define the boundaries for visualization
up_boundary = 160
down_boundary = 320
left_boundary = 200
right_boundary = 440

def process_accelerometer_data():
    """Process accelerometer data and determine game actions"""
    global current_action, start, end
    
    while True:
        with action_lock:
            x = accelerometer_data['x']
            y = accelerometer_data['y']
            z = accelerometer_data['z']
            
            # Determine action based on accelerometer values
            action = None
            
            # X-axis controls left/right movement
            if x > X_THRESHOLD:
                action = "right"
            elif x < -X_THRESHOLD:
                action = "left"
            # Y-axis controls forward movement (jump)
            elif y > Y_THRESHOLD:
                action = "up"
            # Z-axis controls downward movement (slide)
            elif z < -Z_THRESHOLD:
                action = "down"
            
            current_action = action
        
        end = time.time()
        
        # Press the key if action is available and enough time has passed
        if action is not None and end - start > WAIT_TIME:
            print(f"Accelerometer Action: {action} (x={x:.2f}, y={y:.2f}, z={z:.2f})")
            pyautogui.press(action)
            start = time.time()
        
        time.sleep(PROCESSING_DELAY)

def start_accelerometer_server():
    """Start UDP server to receive accelerometer data"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('0.0.0.0', SERVER_PORT))
    print(f"[INFO] Accelerometer server listening on port {SERVER_PORT}")
    
    while True:
        try:
            data, addr = server_socket.recvfrom(1024)
            message = data.decode('utf-8')
            
            try:
                # Parse JSON data from accelerometer
                accel_data = json.loads(message)
                
                # Update global accelerometer data
                accelerometer_data['x'] = accel_data.get('x', 0.0)
                accelerometer_data['y'] = accel_data.get('y', 0.0)
                accelerometer_data['z'] = accel_data.get('z', 0.0)
                accelerometer_data['timestamp'] = time.time()
                
                print(f"Received from {addr}: x={accelerometer_data['x']:.2f}, y={accelerometer_data['y']:.2f}, z={accelerometer_data['z']:.2f}")
                
            except json.JSONDecodeError:
                print(f"Invalid JSON received: {message}")
                
        except Exception as e:
            print(f"Error receiving data: {e}")

# generate frames and yield to Response
def gen_frames():
    while True:
        # Get current action
        with action_lock:
            action = current_action
            x = accelerometer_data['x']
            y = accelerometer_data['y']
            z = accelerometer_data['z']
        
        # Create visualization
        canvas.fill(0)  # Clear canvas
        
        # Draw the boundary lines
        cv2.line(canvas, (0, up_boundary), (W, up_boundary), (255, 255, 255), 2)  # UP
        cv2.line(canvas, (0, down_boundary), (W, down_boundary), (255, 255, 255), 2)  # DOWN
        cv2.line(canvas, (left_boundary, up_boundary), (left_boundary, down_boundary), (255, 255, 255), 2)  # LEFT
        cv2.line(canvas, (right_boundary, up_boundary), (right_boundary, down_boundary), (255, 255, 255), 2)  # RIGHT
        
        # Draw labels for 3D plane movement
        cv2.putText(canvas, "JUMP (+Y)", (W//2 - 40, up_boundary - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.putText(canvas, "SLIDE (-Z)", (W//2 - 40, down_boundary + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.putText(canvas, "LEFT", (left_boundary - 40, H//2), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.putText(canvas, "RIGHT", (right_boundary + 10, H//2), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        # Draw 3D plane movement indicators
        cv2.putText(canvas, "Leg Forward (+Y)", (W//2 - 60, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
        cv2.putText(canvas, "Leg Downward (-Z)", (W//2 - 60, H - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
        
        # Highlight active region based on current action
        if action == "up":
            cv2.rectangle(canvas, (0, 0), (W, up_boundary), (0, 255, 0), -1)
        elif action == "down":
            cv2.rectangle(canvas, (0, down_boundary), (W, H), (0, 255, 0), -1)
        elif action == "left":
            cv2.rectangle(canvas, (0, up_boundary), (left_boundary, down_boundary), (0, 255, 0), -1)
        elif action == "right":
            cv2.rectangle(canvas, (right_boundary, up_boundary), (W, down_boundary), (0, 255, 0), -1)
        
        # Redraw boundary lines on top
        cv2.line(canvas, (0, up_boundary), (W, up_boundary), (255, 255, 255), 2)
        cv2.line(canvas, (0, down_boundary), (W, down_boundary), (255, 255, 255), 2)
        cv2.line(canvas, (left_boundary, up_boundary), (left_boundary, down_boundary), (255, 255, 255), 2)
        cv2.line(canvas, (right_boundary, up_boundary), (right_boundary, down_boundary), (255, 255, 255), 2)
        
        # Information to be displayed
        info = [
            ("Action", action if action else "None"),
            ("Accel X", f"{x:.2f}"),
            ("Accel Y", f"{y:.2f}"),
            ("Accel Z", f"{z:.2f}"),
            ("Status", "WiFi Connected"),
            ("Thresholds", f"X:{X_THRESHOLD} Y:{Y_THRESHOLD} Z:{Z_THRESHOLD}"),
            ("3D Plane", "+Y=Jump, -Z=Slide")
        ]
        
        # Draw the information on the frame
        for (i, (k, v)) in enumerate(info):
            text = "{}: {}".format(k, v)
            cv2.putText(canvas, text, (10, (i * 20) + 20),
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        
        # Generate a stream of frame bytes
        ret, buffer = cv2.imencode('.jpg', canvas)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Home Page
@app.route('/')
def index():
    return render_template('index.html')

# Video streaming route
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    print("[INFO] Accelerometer Game Controller Starting...")
    print(f"[INFO] Make sure your accelerometer device is sending data to this computer on port {SERVER_PORT}")
    print("[INFO] Expected JSON format: {\"x\": 0.0, \"y\": 0.0, \"z\": 0.0}")
    print(f"[INFO] Current thresholds - X: {X_THRESHOLD}, Y: {Y_THRESHOLD}, Z: {Z_THRESHOLD}")
    print("[INFO] 3D Plane Controls:")
    print("  - Move leg left/right: X-axis")
    print("  - Move leg forward (up): +Y-axis (Jump)")
    print("  - Move leg downward: -Z-axis (Slide)")
    
    # Start accelerometer data processing thread
    accel_thread = threading.Thread(target=process_accelerometer_data, daemon=True)
    accel_thread.start()
    
    # Start UDP server thread
    server_thread = threading.Thread(target=start_accelerometer_server, daemon=True)
    server_thread.start()
    
    print(f"[INFO] Web interface available at http://localhost:{WEB_PORT}")
    app.run(debug=True, host='0.0.0.0', port=WEB_PORT) 