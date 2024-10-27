import ultralytics
import cv2
import utils

def main():
    # Replace the image path with any custom image
    img = cv2.imread("capy.jpg")
    img = utils.img_resize(img, width = 640)

    # Replace the path with any custom model
    model = ultralytics.YOLO("datasets/demo/runs/detect/train/weights/best.pt")
    
    results = model(img, verbose = False)
    annotated_img = results[0].plot()

    cv2.imshow("Custom model inference result: press 'q' to quit", annotated_img)

    while True:
        if cv2.waitKey(1) == ord('q'):
            break
    
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    main()