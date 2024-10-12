import ultralytics
import torch
import time
import cv2

def configure_cuda():
    try:
        torch.cuda.set_device(0)
        print("\nModel runing on Cuda")
    except:
        torch.device('cpu')
        print("\nCuda device not found")

def main():
    # Run model on Cuda
    configure_cuda()

    # Import the model
    model = ultralytics.YOLO("model/yolov9t.pt")

    # Setup webcam with openCV
    cam = cv2.VideoCapture(0)
    frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print("Camera on")

    confidence_threshold = 0.5
    loop_counter, start_time, current_time, fps = 0, 0, 0, 0

    while True:
        current_time = time.time()
        if (current_time - start_time) >= 1:
            fps = loop_counter
            start_time = current_time
            loop_counter = 0
        loop_counter += 1

        ret, frame = cam.read()
        results = model(frame, verbose = False, conf = confidence_threshold)
        
        # Extracting actual useful stuff for future use
        for result in results[0].boxes:
            # The object structure of 'boxes' is messy AF
            class_id = int(result.cls)
            class_label = results[0].names[class_id]
            confidence = result.conf * 100
            bbox = result.xyxy[0].tolist()

        # Show annotated frame with fps
        annotated_frame = results[0].plot()
        cv2.putText(img = annotated_frame, 
                          text      = "FPS: " + str(fps), 
                          org       = (frame_width - 75, frame_height - 15), 
                          fontFace  = cv2.FONT_HERSHEY_SIMPLEX,
                          fontScale = 0.5,
                          thickness = 1,
                          color     = (255, 0, 0))
        cv2.imshow("YOLOv9 inference result: press 'q' to quit", annotated_frame)

        if cv2.waitKey(1) == ord('q'):
            break

    # Close camera and openCV window
    cam.release()
    print("Camera off")
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()