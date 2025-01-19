import ultralytics

"""
pip install ultralytics torch torchvision
pip install tensorflow onnx onnx-tf
pip install tf_keras sng4onnx onnx_graphsurgeon onnx2tf onnxslim tflite_support onnxruntime

Visual Studio C++ >= 14
Make sure to check the boxes for build tools and windows 11 SDK

Coral should run TFLite and EdgeTPU but the latter performs better on their hardware
Export EdgeTPU only works on x86-linux, so probably need some Google Colab environment

Documentation -> https://docs.ultralytics.com/guides/coral-edge-tpu-on-raspberry-pi
"""

MODEL_PATH = "model/yolov9t.pt"

# Export NCNN
# model = ultralytics.YOLO(MODEL_PATH)
# model.export(format="ncnn")

# Export TensorFlow-Lite
# model = ultralytics.YOLO(MODEL_PATH)
# model.export(format="tflite")

# Export EdgeTPU
# model = ultralytics.YOLO(MODEL_PATH)
# model.export(format="edgetpu")