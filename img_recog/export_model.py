import ultralytics

MODEL_PATH = ""

# pip install ultralytics torch torchvision
# pip install tensorflow onnx onnx-tf

# Export PyTorch to NCNN
model = ultralytics.YOLO(MODEL_PATH)
model.export(format="ncnn")

# Export PyTorch to TensorFlow-Lite
model = ultralytics.YOLO(MODEL_PATH)
model.export(format="tflite")
