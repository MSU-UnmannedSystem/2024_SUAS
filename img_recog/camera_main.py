import ultralytics
import torch
import time
import cv2
import asyncio
import websockets

# Global variabels
model = None

# Constant
CONFIDENCE_THRESHOLD = 0.5
RAW_WIDTH, RAW_HEIGHT = 2560, 1440
FRAME_WIDTH, FRAME_HEIGHT = 960, 540
SERVER_PORT = "8765"

# Common 16:9 resolutions
""" 640 360
    854 480
    960 540
    1024 57
    1280 720
    1366 768
    1600 900
    1920 1080
    2560 1440
    3200 1800
    3840 2160
    5120 2880
    7680 4320 """

async def report(message):
    try:
        async with websockets.connect(f"ws://localhost:{SERVER_PORT}") as websocket:
            await websocket.send(message)
            response = await websocket.recv()
            return response
    except:
        print("Server not found")
        exit()

def resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image

    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)

    else:
        r = width / float(w)
        dim = (width, int(h * r))

    resized = cv2.resize(image, dim, interpolation = inter)

    return resized

def init():
    global model

    try:
        torch.cuda.set_device(0)
        print("CUDA enabled")
    except:
        torch.device('cpu')
        print("CPU enabled")
    
    model = ultralytics.YOLO("model/yolov9t.pt")
    print("Model loaded")

def camera():
    # Setup webcam with openCV
    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, RAW_WIDTH)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, RAW_HEIGHT)

    print("Camera on")

    loop_counter, start_time, current_time, fps = 0, 0, 0, 0

    while True:
        if cv2.waitKey(1) == ord("q"):
            break
        
        class_label = ""
        bbox = []

        ret, frame = cam.read()
        frame = resize(frame, FRAME_WIDTH, FRAME_HEIGHT)
        results = model(frame, verbose = False, conf = CONFIDENCE_THRESHOLD)

        # Extract detection result from 1st object
        for result in results[0].boxes:
            class_id = int(result.cls)
            class_label = results[0].names[class_id]
            confidence = result.conf * 100
            bbox = result.xyxy[0].tolist()
            break
            
        # Show annotated frame with fps
        annotated_frame = results[0].plot()
        cv2.putText(img         = annotated_frame, 
                    text        = "FPS: " + str(fps),
                    org         = (25, 25),
                    fontFace    = cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale   = 0.5,
                    thickness   = 1,
                    color       = (255, 0, 0))
        
        cv2.imshow("YOLOv9 inference result: press q to quit", annotated_frame)

        # Calculate fps
        current_time = time.time()
        if (current_time - start_time) >= 1:
            fps = loop_counter
            start_time = current_time
            loop_counter = 0
            
            # Send detection result to server
            if class_label != "":
                message = class_label + "_" + " ".join(str(int(b)) for b in bbox)
                asyncio.get_event_loop().run_until_complete(report(message))

        loop_counter += 1

    # Close camera and openCV window
    cam.release()
    cv2.destroyAllWindows()

    print("Camera off")

def main():
    init()
    camera()

if __name__ == "__main__":
    main()