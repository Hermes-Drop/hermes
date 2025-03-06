from camera import OpenCVWebSocket

FLASK_SERVER_URL = "ws://localhost:4000/video"

streamer = OpenCVWebSocket(FLASK_SERVER_URL)
streamer.start()
