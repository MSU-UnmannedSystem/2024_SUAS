import ultralytics

MODEL_PATH = ""

# Export PyTorch to NCNN
model = ultralytics.YOLO(MODEL_PATH)
model.export(format="ncnn")

# Export PyTorch to TensorFlow-Lite
model = ultralytics.YOLO(MODEL_PATH)
model.export(format="tflite")