# handle camera and opencv connections here
import cv2
import numpy as np
import asyncio
import websockets
import os
import base64
import picamera2 as Picamera2

class OpenCVWebSocket:
    def __init__(self, server_url):
        self.server_url = server_url
        self.pi = Picamera2()
        config = self.pi.create_preview_configuration(main={"format": "RGB888", "size": (140, 140)})
        self.pi.configure(config)
        self.pi.start()

        self.net = cv2.dnn.readNet("/home/hermes/Desktop/camera/yolov3-tiny.weights", "/home/hermes/Desktop/camera/yolov3-tiny.cfg")
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

        with open("/home/hermes/Desktop/camera/coco.names", "r") as f:
            self.classes = f.read().strip().split("\n")

        self.TARGET_CLASSES = {"person", "building"}

    def detect_objects(self, frame):
        height, width = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 1/255.0, (160, 160), swapRB=True, crop=False)
        self.net.setInput(blob)

        layer_names = self.net.getUnconnectedOutLayersNames()
        detections = self.net.forward(layer_names)

        for output in detections:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                if confidence > 0.1 and self.classes[class_id] in self.TARGET_CLASSES:
                    box = detection[0:4] * np.array([width, height, width, height])
                    (centerX, centerY, w, h) = box.astype("int")

                    startX = int(centerX - (w / 2))
                    startY = int(centerY - (h / 2))
                    endX = startX + int(w)
                    endY = startY + int(h)

                    label = f"{self.classes[class_id]}: {confidence:.2f}"
                    color = (0, 255, 0) if self.classes[class_id] == "person" else (255, 0, 0)

                    cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
                    cv2.putText(frame, label, (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        return frame
    
    async def send_video(self):
        async with websockets.connect(self.server_url) as websocket:
            while True:
                frame = self.picam2.capture_array()
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = self.detect_objects(frame)

                _, buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
                image = base64.b64encode(buffer).decode("utf-8")

                await websocket.send(image)
                await asyncio.sleep(0.2)

    def start(self):
        asyncio.run(self.send_video())