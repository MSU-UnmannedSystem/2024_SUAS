import time
import cv2

def main():
    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)

    loop_counter, start_time, current_time, fps = 0, 0, 0, 0
    
    while True:
        current_time = time.time()
        if (current_time - start_time) >= 1:
            fps = loop_counter
            start_time = current_time
            loop_counter = 0
        loop_counter += 1

        ret, frame = cam.read()

        cv2.putText(img         = frame, 
                    text        = "FPS: " + str(fps), 
                    org         = (0, 0),
                    fontFace    = cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale   = 0.5,
                    thickness   = 1,
                    color       = (255, 0, 0))

        cv2.imshow("Camera capture: press 'q' to quit", frame)

        if cv2.waitKey(1) == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()