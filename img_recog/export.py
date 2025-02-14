'''
    A x86 (non-ARM) platform running Linux is required for exporting.
    The simpliest way is to use a Google Colab virtual runtime.
'''

# Run these to setup environment for exporting
# pip uninstall tensorflow tensorflow-aarch64
# pip install -U tflite-runtime
# pip install ultralytics

# Do these if ultralytics doesn't auto install all needed stuff
# !pip install ultralytics torch torchvision
# !pip install tflite-runtime onnx onnx-tf
# !pip install tf_keras sng4onnx onnx_graphsurgeon onnx2tf
# !pip install onnxslim tflite_support onnxruntime

import ultralytics

# Export EdgeTPU
model = ultralytics.YOLO("path_to_pt_file")
model.export(format="edgetpu")