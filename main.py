from camera_control import OpenCVWebSocket

FLASK_SERVER_URL = "ws://10.251.4.78:4000/video"

streamer = OpenCVWebSocket(FLASK_SERVER_URL)
streamer.start()
