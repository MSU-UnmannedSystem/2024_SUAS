import time
import cv2
from ultralytics import YOLO

# Constant
CONFIDENCE_THRESHOLD = 0.5
RAW_WIDTH, RAW_HEIGHT = 1920, 1080
FRAME_WIDTH, FRAME_HEIGHT = 640, 360

def main():
    # Load model
    model = YOLO("model/yolov9t.pt", task = "detect")

    # Setup webcam with openCV
    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, RAW_WIDTH)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, RAW_HEIGHT)

    loop_counter, start_time, current_time, fps = 0, 0, 0, 0

    while True:
        if cv2.waitKey(1) == ord("q"):
            break

        _, frame = cam.read()
        frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))
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

        loop_counter += 1

    # Close camera and openCV window
    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()