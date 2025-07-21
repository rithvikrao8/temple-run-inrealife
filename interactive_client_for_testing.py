# Interactive Accelerometer Client
# Simulates accelerometer data by sending JSON when WASD keys are pressed
# Perfect for testing the 3D plane movement system

import socket
import json
import time
import threading
from pynput import keyboard
from config import *

# Server configuration
SERVER_IP = "127.0.0.1"  # Change this to your computer's IP address
SERVER_PORT = 5001

# Create UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Global variables for key states
key_states = {
    'w': False,  # Jump (+Y)
    'a': False,  # Left (-X)
    's': False,  # Slide (-Z)
    'd': False   # Right (+X)
}

def send_accelerometer_data(x, y, z):
    """Send accelerometer data to the server"""
    data = {
        "x": x,
        "y": y,
        "z": z,
        "timestamp": time.time()
    }
    
    message = json.dumps(data)
    try:
        client_socket.sendto(message.encode('utf-8'), (SERVER_IP, SERVER_PORT))
        print(f"Sent: x={x:.2f}, y={y:.2f}, z={z:.2f}")
    except Exception as e:
        print(f"Error sending data: {e}")

def on_press(key):
    """Handle key press events"""
    try:
        key_char = key.char.lower()
        if key_char in key_states:
            key_states[key_char] = True
            print(f"Key pressed: {key_char.upper()}")
    except AttributeError:
        pass

def on_release(key):
    """Handle key release events"""
    try:
        key_char = key.char.lower()
        if key_char in key_states:
            key_states[key_char] = False
            print(f"Key released: {key_char.upper()}")
        
        # Stop listener on 'q' key
        if key == keyboard.Key.esc:
            return False
    except AttributeError:
        pass

def calculate_accelerometer_values():
    """Calculate accelerometer values based on key states"""
    x = 0.0
    y = 0.0
    z = 0.0
    
    # X-axis: Left/Right movement
    if key_states['a']:  # Left
        x = -0.8
    elif key_states['d']:  # Right
        x = 0.8
    
    # Y-axis: Forward movement (Jump)
    if key_states['w']:  # Jump
        y = 0.8
    
    # Z-axis: Downward movement (Slide)
    if key_states['s']:  # Slide
        z = -0.8
    
    return x, y, z

def main():
    print("[INFO] Interactive Accelerometer Client Starting...")
    print(f"[INFO] Connecting to server at {SERVER_IP}:{SERVER_PORT}")
    print("[INFO] 3D Plane Controls:")
    print("  - W: Jump (+Y axis)")
    print("  - A: Move Left (-X axis)")
    print("  - S: Slide (-Z axis)")
    print("  - D: Move Right (+X axis)")
    print("  - ESC: Exit")
    print("[INFO] Press keys to simulate accelerometer movements...")
    
    # Start keyboard listener
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    
    try:
        while True:
            # Calculate accelerometer values based on current key states
            x, y, z = calculate_accelerometer_values()
            
            # Send data if any key is pressed
            if any(key_states.values()):
                send_accelerometer_data(x, y, z)
            
            # Small delay to prevent overwhelming the server
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\n[INFO] Client stopped by user")
    finally:
        listener.stop()
        client_socket.close()
        print("[INFO] Interactive client closed")

if __name__ == "__main__":
    main() 