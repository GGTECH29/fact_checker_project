import torch

print(f"PyTorch Version: {torch.__version__}")
print(f"CUDA verfügbar: {torch.cuda.is_available()}")
print(f"CUDA-Gerät: {torch.cuda.get_device_name(0)}")
