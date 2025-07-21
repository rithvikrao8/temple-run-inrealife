# Hands-free Temple Run
Temple fun is temple run re-imagined into real life where I take the idea of temple run by making you control your character using real life actions. 

## why real life actions? what is the real world problem this addresses?
 it addresses obesity and helps kid move more without being extremely physically demanding like other sports. Ex: basketball and soccer


## why not use a VR head set
you can use a VR headset, but we want to create an option for a cheaper alternative that still gives you the feeling of being active. Also people cannot use a VR headset for long without feeling claustro phobic.


## why not Kinect?
Kinect was buggy, required a lot of space, was expensive and honestly not made at the right time because the industry wasnt really moving in that direction yet. 

## game mechanics 
To run, you need to spot jog  
to jump, you need to actually jump  
to step left , you need to jump left  
to step right, you need to jump right 

***

<img src="media/1.gif" width="100%">

## Prerequisites

Download and install Python 3.x ([link](https://www.python.org/downloads/))

Clone the repository

    git clone https://github.com/priyanksharma7/temple-run.git

(Optional) Create and activate a virtual environment

    python -m venv virtual_env
    .\virtual_env\Scripts\activate

Install dependencies

    pip install opencv-contrib-python pyautogui flask pynput

## How to run

### Web-based Accelerometer Controller

`accelerometer_server.py` : Web-based accelerometer game controller with Flask interface.

    python accelerometer_server.py
Note: Press 'Ctrl+C' in the terminal to exit.

## Controls

### Accelerometer Controls (3D Plane Movement)
- **Move leg left** : Move left
- **Move leg right** : Move right
- **Move leg forward (up)** : Jump (+Y axis)
- **Move leg downward** : Slide (-Z axis)

## 3D Plane Movement System

The accelerometer system uses a **3D plane** for intuitive leg-based controls:

### **X-axis (Left/Right)**
- **Move leg left** → Character moves left
- **Move leg right** → Character moves right

### **Y-axis (Forward)**
- **Move leg forward (lift up)** → Character jumps (+Y)

### **Z-axis (Downward)**
- **Move leg downward** → Character slides (-Z)

## Accelerometer Setup

### 1. Configure Your Device
1. Find your computer's IP address (e.g., `192.168.1.100`)
2. Update your accelerometer device code with your computer's IP address
3. Adjust sensitivity thresholds in `config.py` if needed

### 2. Send Accelerometer Data
Your accelerometer device should send JSON data to your computer on port 5001:

```json
{
    "x": 0.0,  // Left/Right movement (-1.0 to 1.0)
    "y": 0.0,  // Forward movement (-1.0 to 1.0)
    "z": 0.0   // Up/Down movement (-1.0 to 1.0)
}
```

### 3. Example Client Code
Use this as a template for your device:

```python
# Example for ESP32, Arduino, or other WiFi-enabled device
import socket
import json

# Send accelerometer data
data = {"x": x_value, "y": y_value, "z": z_value}
message = json.dumps(data)
client_socket.sendto(message.encode('utf-8'), (SERVER_IP, 5001))
```

## Configuration

Edit `config.py` to adjust:
- **Sensitivity thresholds** (X_THRESHOLD, Y_THRESHOLD, Z_THRESHOLD)
- **Network ports** (SERVER_PORT, WEB_PORT)
- **Game control timing** (WAIT_TIME, PROCESSING_DELAY)

## Troubleshooting

1. **No accelerometer data received**: Check firewall settings and ensure port 5001 is open
2. **Too sensitive/not sensitive enough**: Adjust thresholds in `config.py`
3. **Network issues**: Verify both devices are on the same WiFi network
4. **Game not responding**: Check that Temple Run is the active window
5. **Slide not working**: Ensure your leg movement downward exceeds the -Z_THRESHOLD value
6. **Jump not working**: Ensure your leg movement forward exceeds the +Y_THRESHOLD value

## Leg Movement Tips

- **For jumping**: Lift your leg forward/upward (+Y axis)
- **For sliding**: Move your leg downward (-Z axis)
- **For left movement**: Move your leg to the left
- **For right movement**: Move your leg to the right
- **Adjust sensitivity**: If movements are too sensitive, increase threshold values in `config.py`

## 3D Movement Examples

```python
# Jump: Move leg forward/upward
{"x": 0.0, "y": 0.5, "z": 0.0}  # +Y triggers jump

# Slide: Move leg downward  
{"x": 0.0, "y": 0.0, "z": -0.5}  # -Z triggers slide

# Move left
{"x": -0.5, "y": 0.0, "z": 0.0}  # -X triggers left

# Move right
{"x": 0.5, "y": 0.0, "z": 0.0}   # +X triggers right
```

***

### Acknowledgements

Thanks to https://github.com/priyanksharma7/temple-run for the original code!!!
