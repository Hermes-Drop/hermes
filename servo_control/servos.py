# handle arduino code here (assuming python)
# make them functions that are callable
#
# 1) convert x,y direction to degrees
#       degrees is then used to tell arduino to make servos rotate X degrees
#       assume that any instructions you get will purely be translational not rotational
#
# 2) actually sending the degrees into the arduino
#
# arduino-python3 0.6
# pyserial
import serial

arduino = serial.Serial(port="/dev/ttyUSB0", baudrate=9600, timeout=1)

def convert_to_degrees(key):
    x, y = 0, 0
    if key == "ArrowUp":
        y = 10
    elif key == "ArrowDown":
        y = -10
    elif key == "ArrowLeft":
        x = -10
    elif key == "ArrowRight":
        x = 10
    return x, y

def send_to_arduino(x, y):
    command = f"X:{x},Y:{y}\n"
    arduino.write(command.encode())
    print(f"Sent to Arduino: {command.strip()}")

def handle_servo_input(key, action):
    if action == "down":
        x, y = convert_to_degrees(key)
        send_to_arduino(x, y)