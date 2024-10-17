import cv2

# Constant
cam_number = 1 # Change this if necessary
frame_width, frame_height = 960, 540

def main():
    cam = cv2.VideoCapture(cam_number, cv2.CAP_DSHOW)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 3840)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('webcam_output.mp4', fourcc, 20.0, (frame_width, frame_height))

    while True:
        ret, frame = cam.read()

        out.write(frame)

        cv2.imshow("Webcam capture: press 'q' to quit", frame)

        if cv2.waitKey(1) == ord('q'):
            break

    out.release()
    cam.release()
    cv2.destroyAllWindows()
        

if __name__ == "__main__":
    main()
