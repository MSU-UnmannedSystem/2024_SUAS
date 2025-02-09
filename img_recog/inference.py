import keyboard
import time
import cv2
from ultralytics import YOLO

# Constant
CONFIDENCE_THRESHOLD = 0.5
RAW_WIDTH, RAW_HEIGHT = 640, 360
FRAME_WIDTH, FRAME_HEIGHT = 640, 360
FPS_CALC_INTERVAL_SEC, SCREENSHOT_INTERVAL_SEC = 1, 10

def main():
    # Load model
    model = YOLO("model/yolov9t.pt")
    # model = YOLO("model/yolov9t_edge_tpu_model/yolov9t_full_integer_quant_edgetpu.tflite", 
    #               task = "detect")
    print(f"Status:\tModel Loaded")

    # Setup webcam with openCV
    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, RAW_WIDTH)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, RAW_HEIGHT)

    print(f"Status:\tCamera On")
    print(f"Frame:\t{FRAME_WIDTH}x{FRAME_HEIGHT}")
    print()

    loop_counter = current_time = fps = class_id = confidence = 0
    label_prev = class_label = ""
    bbox = bboex_format = []
    start_time1 = start_time2 = base_time = time.time()
    
    while True:
        if keyboard.is_pressed('q'):
            break

        _, frame = cam.read()
        # frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))
        results = model(frame, verbose = False, conf = CONFIDENCE_THRESHOLD)

        if len(results[0].boxes) == 0:
            class_label = "Nothing"
            confidence = -1
            bboex_format = [-1, -1, -1, -1]

        # Extract detection result from 1st object
        for result in results[0].boxes:
            class_id = int(result.cls)
            class_label = results[0].names[class_id]
            confidence = int(result.conf * 100)
            bbox = result.xyxy[0].tolist()
            bboex_format = [int(bbox[0]), int(bbox[2]), int(bbox[2]), int(bbox[3])]
            break
        
        # Only print to console when objects in frame changes
        if class_label != label_prev:
            print(f"Name: {class_label}")
            print(f"Bbox: {bboex_format}")
            print(f"Conf: {confidence}%")
            print()
        label_prev = class_label
            
        # Show annotated frame with fps
        annotated_frame = results[0].plot()
        cv2.putText(img         = annotated_frame, 
                    text        = "FPS: " + str(fps),
                    org         = (25, 25),
                    fontFace    = cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale   = 0.5,
                    thickness   = 1,
                    color       = (255, 0, 0))

        # cv2.imshow("YOLOv9 inference result: press q to quit", annotated_frame)

        # Calculate fps
        current_time = time.time()
        if (current_time - start_time1) >= FPS_CALC_INTERVAL_SEC:
            fps = loop_counter
            start_time1 = current_time
            loop_counter = 0
        
        # Save screenshot
        if(current_time - start_time2) > SCREENSHOT_INTERVAL_SEC:
            start_time2 = current_time
            cv2.imwrite(f"screenshot/{int(current_time)}.png", annotated_frame)

        loop_counter += 1

    # Close camera and openCV window
    cam.release()
    cv2.destroyAllWindows()
    runtime = int(current_time - base_time)

    print(f"Status:\tCamera Off")
    print(f"Uptime:\t{runtime} sec")
    print(f"Speed:\t{fps} fps")

if __name__ == "__main__":
    main()
