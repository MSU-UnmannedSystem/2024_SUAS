import cv2
import json
import depthai
import numpy as np

# ------------------------------------- Constants -------------------------------------
RESULT_PATH = "model/"
BLOB_NAME = "yolov9t.blob"
JSON_NAME = "yolov9t.json"

field_of_view_width_m = 200 # not used
field_of_view_height_m = 150 # not used
# ------------------------------------- Constants -------------------------------------

def get_model_param():
    blob_path = RESULT_PATH + BLOB_NAME   
    json_path = RESULT_PATH + JSON_NAME

    file = open(json_path)
    nn_config = json.load(file).get("nn_config")
    num_classes = nn_config["NN_specific_metadata"]["classes"]
    coordinates = nn_config["NN_specific_metadata"]["coordinates"]
    anchors = nn_config["NN_specific_metadata"]["anchors"]
    anchor_masks = nn_config["NN_specific_metadata"]["anchor_masks"]
    iou_threshold = nn_config["NN_specific_metadata"]["iou_threshold"]
    confidence_threshold = nn_config["NN_specific_metadata"]["confidence_threshold"]
    width, height = nn_config["input_size"].split("x")
    width, height = int(width), int(height)
    file.close()

    file = open(json_path)
    class_map = json.load(file).get("mappings")
    class_map = class_map["labels"]
    file.close()

    return blob_path, iou_threshold, confidence_threshold, class_map,\
           num_classes, coordinates, anchors, anchor_masks, width, height

def start_camera(pipeline, class_map):
    with depthai.Device(pipeline) as device:
        q_rgb = device.getOutputQueue("camera")
        q_nn = device.getOutputQueue("nn")
        frame = None
        detections = []
        
        print("Activated detection loop.")
        print("Press 'q' to quit.")

        def get_frame_Norm(frame, bbox):
            normVals = np.full(len(bbox), frame.shape[0])
            normVals[::2] = frame.shape[1]

            return (np.clip(np.array(bbox), 0, 1) * normVals).astype(int)
        
        while True:
            in_rgb = q_rgb.tryGet()
            in_nn = q_nn.tryGet()

            if in_rgb is not None:
                frame = in_rgb.getCvFrame()

            if in_nn is not None:
                detections = in_nn.detections

            if frame is not None:

                for detection in detections:
                    bbox = get_frame_Norm(frame, (detection.xmin, detection.ymin,
                                                  detection.xmax, detection.ymax))
                    
                    cv2.rectangle(img       = frame,
                                  pt1       = (bbox[0], bbox[1]),
                                  pt2       = (bbox[2], bbox[3]),
                                  color     = (255, 0, 0),
                                  thickness = 2)
                    
                    class_name = class_map[detection.label]
                    confidence = int(detection.confidence * 100)
                    text = f"{class_name} {confidence}%"
                    org_x = int(bbox[0] * 1.1)
                    org_y = int(bbox[1] * 0.9)

                    cv2.putText(img       = frame, 
                                text      = text, 
                                org       = (org_x, org_y), 
                                fontFace  = cv2.FONT_HERSHEY_SIMPLEX,
                                fontScale = 1,
                                thickness = 2,
                                color     = (255, 0, 0))
                    
                cv2.imshow("preview", frame)

            if cv2.waitKey(1) == ord('q'):
                break

def main():
    blob_path,\
    iou_threshold,\
    confidence_threshold,\
    class_map,\
    num_classes,\
    coordinates,\
    anchors,\
    anchor_masks,\
    width,\
    height = get_model_param()
    
    pipeline = depthai.Pipeline()

    detection_nn = pipeline.createYoloDetectionNetwork()
    detection_nn.setBlobPath(blob_path)
    detection_nn.setIouThreshold(iou_threshold)
    detection_nn.setConfidenceThreshold(confidence_threshold)
    detection_nn.setNumClasses(num_classes)
    detection_nn.setCoordinateSize(coordinates)
    detection_nn.setAnchors(anchors)
    detection_nn.setAnchorMasks(anchor_masks)

    xout_rgb = pipeline.createXLinkOut()
    xout_rgb.setStreamName("camera")

    cam_rgb = pipeline.createColorCamera()
    cam_rgb.setPreviewSize(width, height)
    cam_rgb.setInterleaved(False)
    cam_rgb.preview.link(detection_nn.input)
    cam_rgb.preview.link(xout_rgb.input)

    xout_nn = pipeline.createXLinkOut()
    xout_nn.setStreamName("nn")

    detection_nn.out.link(xout_nn.input)

    try:
        depthai.Device(pipeline)
    except:
        print("No OAK-D devices deteced.")
        exit()
    else:
        print("Starting camera...")
        start_camera(pipeline = pipeline, class_map = class_map)

if __name__ == "__main__":
    main()