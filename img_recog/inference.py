import time
import cv2
from ultralytics import YOLO

# Global
cam = None

# Constant
CONFIDENCE_THRESHOLD = 0.5
RAW_WIDTH, RAW_HEIGHT = 640, 360
FRAME_WIDTH, FRAME_HEIGHT = 640, 360
FPS_CALC_INTERVAL_SEC = 1
SCREENSHOT_INTERVAL_SEC = 10
TAKE_SCREENSHOT = False
SHOW_INFERENCE_FRAME = False
PRINT_INFERENCE_TERMINAL = True
MAX_INIT_CAMERA_ATTEMP = 10

def main():
    # Load model
    model = YOLO("model/yolov9t.pt")
    # model = YOLO("model/yolov9t_edge_tpu_model/yolov9t_full_integer_quant_edgetpu.tflite", 
    #               task = "detect")
    print("Status:\tModel Loaded")

    # Setup webcam with openCV 
    global cam
    for attempt in range(MAX_INIT_CAMERA_ATTEMP):
        print("Status:\tStarting camera attempt {} / {}".format(attempt, MAX_INIT_CAMERA_ATTEMP))
        
        cam = cv2.VideoCapture(0)
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, RAW_WIDTH)
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, RAW_HEIGHT)
        
        try:
            _, frame = cam.read()
            break
        except:
            cam.release()
            cam = None
            time.sleep(2)

    print("Status:\tCamera On")
    print("Frame:\t{}x{}".format(FRAME_WIDTH, FRAME_HEIGHT))
    print()
    print("Ctrl + C to quit")
    print()

    loop_counter = current_time = fps = class_id = confidence = 0
    label_prev = class_label = ""
    annotated_frame = None
    bbox = bboex_format = []
    start_time1 = start_time2 = base_time = time.time()
    
    while True:
        _, frame = cam.read()
        # frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))
        results = model(frame, verbose = False, conf = CONFIDENCE_THRESHOLD)
        
        if cv2.waitKey(1) == ord('q'):
            break        

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
        if class_label != label_prev and PRINT_INFERENCE_TERMINAL:
            print("Name: {}".format(class_label))
            print("Bbox: {}".format(bboex_format))
            print("Conf: {}%".format(confidence))
            print("FPSs: {}fps".format(fps))
            print()
            
            if annotated_frame is not None and TAKE_SCREENSHOT:
                cv2.imwrite("screenshot/{}.png".format(int(current_time)), annotated_frame)
            
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
		
        if SHOW_INFERENCE_FRAME:
            cv2.imshow("Inference result", annotated_frame)

        # Calculate fps
        current_time = time.time()
        if (current_time - start_time1) >= FPS_CALC_INTERVAL_SEC:
            fps = loop_counter
            start_time1 = current_time
            loop_counter = 0
        
        # Save screenshot
        if(current_time - start_time2) > SCREENSHOT_INTERVAL_SEC and TAKE_SCREENSHOT:
            start_time2 = current_time
            cv2.imwrite("screenshot/{}.png".format(int(current_time)), annotated_frame)

        loop_counter += 1
    
    print()
    print("Status:\tCamera Off")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        cam.release()
        cv2.destroyAllWindows()
        print()
        print("Status:\tCamera Off")
