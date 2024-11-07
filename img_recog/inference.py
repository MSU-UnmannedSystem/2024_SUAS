import ultralytics
import cv2

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

def main():
    img = cv2.imread("capy.jpg")
    img = resize(img, width = 640)

    # model = ultralytics.YOLO("datasets/demo/runs/detect/train/weights/best.pt")
    model = ultralytics.YOLO("model/yolov9t.pt")
    
    results = model(img, verbose = False)
    annotated_img = results[0].plot()

    cv2.imshow("Custom model inference result: press 'q' to quit", annotated_img)

    while True:
        if cv2.waitKey(1) == ord('q'):
            break
    
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()