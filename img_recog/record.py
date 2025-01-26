import cv2
import datetime

# Constant
cam_number = 0 # Change this if necessary
frame_width, frame_height = 960, 540

def main():
    cam = cv2.VideoCapture(cam_number, cv2.CAP_DSHOW)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 3840)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('webcam_output.mp4', fourcc, 20.0, (frame_width, frame_height))
    SEC = 15
    start = datetime.datetime.now()
    i=0
    ind = True
    while True:
        fps = cam.get(cv2.CAP_PROP_FPS)
        ret, frame = cam.read()
        print(int((datetime.datetime.now()-start).total_seconds()))
        if(int((datetime.datetime.now()-start).total_seconds())==15):
            i=i+1
            print("yes")
            print("\\saved\\"+str(i)+'.jpg')
            if ind:
                cv2.imwrite(".\\saved\\"+str(i)+'.jpg',frame)
            ind =False
        else:
            ind=True

        out.write(frame)

        cv2.imshow("Webcam capture: press 'q' to quit", frame)

        if cv2.waitKey(1) == ord('q'):
            break
    out.release()
    cam.release()
    cv2.destroyAllWindows()
        

if __name__ == "__main__":
    main()
