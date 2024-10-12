import torch

cuda_is_availible = torch.cuda.is_available()
print()
print("Cuda device found:\n\t", cuda_is_availible)

if cuda_is_availible:
    print("Device name:\n\t", torch.cuda.get_device_name())
    print("Cuda version:\n\t", torch.version.cuda)