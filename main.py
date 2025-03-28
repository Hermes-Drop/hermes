from flask import Flask
from flask_socketio import SocketIO
from camera_control.camera import OpenCVWebSocket
from servo_control.servo import handle_servo_input

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

FLASK_SERVER_URL = "ws://172.20.10.4:4000/video"
streamer = OpenCVWebSocket(FLASK_SERVER_URL)

@socketio.on("connect")
def connect():
    print("Hermes connected to user control")

@socketio.on("keyboard_event")
def handle_keyboard_event(data):
    key = data.get("key")
    action = data.get("action")

    # only want to process arrow keys
    if action == "down" and key in ["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"]:
        print(f"Key pressed: {key}, Action: {action}")
        socketio.emit("keyboard_event", {"key": key, "action": action})

if __name__ == "__main__":
    import threading
    threading.Thread(target=streamer.start, daemon=True).start()

    socketio.run(app, host="0.0.0.0", port=5000)