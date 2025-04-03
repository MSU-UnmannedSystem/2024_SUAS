import time
import cv2
import socket
from ultralytics import YOLO

# Camera object that will init later
camera = None

# See model/coco.yaml for id & class
valid_objects = [
    0,  # person
    32, # sports ball
]

# Constant
CONFIDENCE_THRESHOLD = 0.5
FRAME_WIDTH, FRAME_HEIGHT = 640, 360
FPS_CALC_INTERVAL_SEC = 1
SCREENSHOT_INTERVAL_SEC = 10
USE_SOCKET = False
TAKE_SCREENSHOT = True
SHOW_INFERENCE_FRAME = False
PRINT_INFERENCE_TERMINAL = True
INIT_CAMERA_ATTEMPT = 10
IS_CENTER_TOLERANCE = 0.50

def at_center(bbox: list):
    x1, y1, x2, y2 = bbox[0], bbox[1], bbox[2], bbox[3]
    center_x = (x1 + abs(x2 - x1)) / FRAME_WIDTH
    center_y = (y1 - abs(y2 - y1)) / FRAME_HEIGHT
    x_true = abs(center_x - 0.5) <= IS_CENTER_TOLERANCE
    y_true = abs(center_y - 0.5) <= IS_CENTER_TOLERANCE
    return x_true and y_true

def main():	
    # Load model using pure CPU
    # model = YOLO("model/yolov9t.pt")
    
    # Load model using Coral Accelerator
    model = YOLO("model/yolov9t_coral/yolov9t_full_integer_quant_edgetpu.tflite",
                  task = "detect")
       
    print("\nStatus:\tModel Loaded")
    print("\nLooking for: {}".format(valid_objects))

    # Init socket server
    if USE_SOCKET:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        server_address = ('localhost', 12345)
        server_socket.bind(server_address)
        server_socket.listen(5)
        print("\nServer Waiting on {}".format(server_address))
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}\n")

    # Setup camera with opencv
    global camera
    for attempt in range(INIT_CAMERA_ATTEMPT):
        print("Status:\tStarting Camera Attempt {} / {}".format(attempt, INIT_CAMERA_ATTEMPT))
        
        camera = cv2.VideoCapture(0)
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
        
        try:
            _, frame = camera.read()
            break
        except:
            camera.release()
            camera = None
            time.sleep(2)

    print("Status:\tCamera On")
    print("Frame:\t{}x{}\n".format(FRAME_WIDTH, FRAME_HEIGHT))
    print("Ctrl + C to Quit\n")

    loop_counter = current_time = fps = class_id = confidence = 0
    label_prev = class_label = ""
    annotated_frame = None
    bbox = bboex_format = []
    start_time1 = start_time2 = time.time()
    
    while True:
        _, frame = camera.read()
        # frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))
        results = model(frame, verbose = False, conf = CONFIDENCE_THRESHOLD)
        
        if cv2.waitKey(1) == ord('q'):
            break        

        if len(results[0].boxes) == 0:
            class_id = -1
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
        
        # Ignore objects not interested
        if class_id in valid_objects:
            # Only print to console when objects in frame changes
            if class_label != label_prev and PRINT_INFERENCE_TERMINAL:
                print("\nName: {}".format(class_label))
                print("Conf: {}%".format(confidence))
                
            # Save newly detected object screenshot
            if annotated_frame is not None and TAKE_SCREENSHOT:
                cv2.imwrite("screenshot/{}.png".format(int(current_time)), annotated_frame)

            # Move servo and drop item when object at frame center
            if at_center(bboex_format):
                if USE_SOCKET:
                    try:
                        client_socket.send("Drop".encode())
                    except:
                        server_socket.close()
                        client_socket.close()

                # If item aligned for drop, add comment text and save screenshot                            
                if annotated_frame is not None and TAKE_SCREENSHOT:
                    cv2.imwrite("screenshot/{}-drop.png".format(int(current_time)), annotated_frame)

                print("\nItem Dropped")
                # break
            
        label_prev = class_label

        # Calculate fps
        current_time = time.time()
        if (current_time - start_time1) >= FPS_CALC_INTERVAL_SEC:
            fps = loop_counter
            start_time1 = current_time
            loop_counter = 0
        
        # Save screenshot
        # if(current_time - start_time2) > SCREENSHOT_INTERVAL_SEC and TAKE_SCREENSHOT:
            # start_time2 = current_time
            # cv2.imwrite("screenshot/{}.png".format(int(current_time)), annotated_frame)

        loop_counter += 1

    print("\nStatus:\tCamera Off")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        camera.release()
        cv2.destroyAllWindows()
        print("\nStatus:\tCamera Off")
