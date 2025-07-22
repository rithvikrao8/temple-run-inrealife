#!/usr/bin/env python3
"""
Raspberry Pi Accelerometer Client for Temple Run
Uses BerryPi accelerometer card to send movement data to the main server
"""

import time
import socket
import json
import threading
from typing import Dict, Any
import smbus2 as smbus

# Configuration
SERVER_IP = "192.168.1.100"  # Change to your computer's IP address
SERVER_PORT = 5001
SAMPLE_RATE = 50  # Hz (50 samples per second)
BUS_NUMBER = 1  # I2C bus number (usually 1 for Raspberry Pi)

# BerryPi Accelerometer I2C Address (MPU6050)
MPU6050_ADDR = 0x68

# MPU6050 Register Addresses
PWR_MGMT_1 = 0x6B
CONFIG = 0x1A
GYRO_CONFIG = 0x1B
ACCEL_CONFIG = 0x1C
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
TEMP_OUT_H = 0x41
GYRO_XOUT_H = 0x43
GYRO_YOUT_H = 0x45
GYRO_ZOUT_H = 0x47

class BerryPiAccelerometer:
    """BerryPi Accelerometer interface using MPU6050"""
    
    def __init__(self, bus_number: int = 1, address: int = MPU6050_ADDR):
        self.bus = smbus.SMBus(bus_number)
        self.address = address
        self.initialize_sensor()
        
    def initialize_sensor(self):
        """Initialize the MPU6050 sensor"""
        try:
            # Wake up the sensor
            self.bus.write_byte_data(self.address, PWR_MGMT_1, 0)
            time.sleep(0.1)
            
            # Configure accelerometer (±2g range)
            self.bus.write_byte_data(self.address, ACCEL_CONFIG, 0x00)
            time.sleep(0.1)
            
            # Configure gyroscope (±250°/s range)
            self.bus.write_byte_data(self.address, GYRO_CONFIG, 0x00)
            time.sleep(0.1)
            
            print("[INFO] BerryPi accelerometer initialized successfully")
            
        except Exception as e:
            print(f"[ERROR] Failed to initialize accelerometer: {e}")
            raise
    
    def read_raw_data(self, register: int) -> int:
        """Read raw 16-bit data from sensor register"""
        high = self.bus.read_byte_data(self.address, register)
        low = self.bus.read_byte_data(self.address, register + 1)
        value = (high << 8) | low
        
        # Convert to signed 16-bit
        if value > 32767:
            value -= 65536
        return value
    
    def read_accelerometer(self) -> Dict[str, float]:
        """Read accelerometer data and return normalized values"""
        try:
            # Read raw accelerometer data
            accel_x = self.read_raw_data(ACCEL_XOUT_H)
            accel_y = self.read_raw_data(ACCEL_YOUT_H)
            accel_z = self.read_raw_data(ACCEL_ZOUT_H)
            
            # Convert to g-force (assuming ±2g range)
            # MPU6050 sensitivity: 16384 LSB/g for ±2g range
            x_g = accel_x / 16384.0
            y_g = accel_y / 16384.0
            z_g = accel_z / 16384.0
            
            # Normalize to -1.0 to 1.0 range
            # Apply calibration offsets and scaling
            x_norm = max(-1.0, min(1.0, x_g * 2.0))  # Scale to ±1.0
            y_norm = max(-1.0, min(1.0, y_g * 2.0))
            z_norm = max(-1.0, min(1.0, z_g * 2.0))
            
            return {
                'x': x_norm,
                'y': y_norm,
                'z': z_norm,
                'timestamp': time.time()
            }
            
        except Exception as e:
            print(f"[ERROR] Failed to read accelerometer: {e}")
            return {'x': 0.0, 'y': 0.0, 'z': 0.0, 'timestamp': time.time()}
    
    def calibrate(self, samples: int = 100):
        """Calibrate the accelerometer by taking multiple samples"""
        print(f"[INFO] Calibrating accelerometer with {samples} samples...")
        
        x_sum = y_sum = z_sum = 0
        
        for i in range(samples):
            data = self.read_accelerometer()
            x_sum += data['x']
            y_sum += data['y']
            z_sum += data['z']
            time.sleep(0.01)
        
        # Calculate offsets
        self.x_offset = x_sum / samples
        self.y_offset = y_sum / samples
        self.z_offset = z_sum / samples
        
        print(f"[INFO] Calibration complete. Offsets: X={self.x_offset:.3f}, Y={self.y_offset:.3f}, Z={self.z_offset:.3f}")

class AccelerometerClient:
    """Client that sends accelerometer data to the main server"""
    
    def __init__(self, server_ip: str, server_port: int):
        self.server_ip = server_ip
        self.server_port = server_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.running = False
        
        # Initialize BerryPi accelerometer
        self.accelerometer = BerryPiAccelerometer(BUS_NUMBER)
        
    def send_data(self, data: Dict[str, Any]):
        """Send accelerometer data to server"""
        try:
            message = json.dumps(data)
            self.socket.sendto(message.encode('utf-8'), (self.server_ip, self.server_port))
        except Exception as e:
            print(f"[ERROR] Failed to send data: {e}")
    
    def run(self):
        """Main loop to read and send accelerometer data"""
        self.running = True
        
        # Calibrate the sensor first
        self.accelerometer.calibrate()
        
        print(f"[INFO] Starting accelerometer client...")
        print(f"[INFO] Sending data to {self.server_ip}:{self.server_port}")
        print(f"[INFO] Sample rate: {SAMPLE_RATE} Hz")
        print("[INFO] Press Ctrl+C to stop")
        
        try:
            while self.running:
                # Read accelerometer data
                data = self.accelerometer.read_accelerometer()
                
                # Apply calibration offsets
                data['x'] -= self.accelerometer.x_offset
                data['y'] -= self.accelerometer.y_offset
                data['z'] -= self.accelerometer.z_offset
                
                # Send data to server
                self.send_data(data)
                
                # Print current values (for debugging)
                print(f"X: {data['x']:6.3f}, Y: {data['y']:6.3f}, Z: {data['z']:6.3f}", end='\r')
                
                # Wait for next sample
                time.sleep(1.0 / SAMPLE_RATE)
                
        except KeyboardInterrupt:
            print("\n[INFO] Stopping accelerometer client...")
        except Exception as e:
            print(f"\n[ERROR] Unexpected error: {e}")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        self.running = False
        if hasattr(self, 'socket'):
            self.socket.close()
        print("[INFO] Accelerometer client stopped")

def main():
    """Main function"""
    print("=== BerryPi Accelerometer Client for Temple Run ===")
    print(f"Target server: {SERVER_IP}:{SERVER_PORT}")
    print(f"Sample rate: {SAMPLE_RATE} Hz")
    print()
    
    # Create and run client
    client = AccelerometerClient(SERVER_IP, SERVER_PORT)
    client.run()

if __name__ == "__main__":
    main() 