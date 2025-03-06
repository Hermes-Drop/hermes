from camera_control.camera import OpenCVWebSocket

FLASK_SERVER_URL = "ws://172.20.10.4:4000/video"

streamer = OpenCVWebSocket(FLASK_SERVER_URL)
streamer.start()
