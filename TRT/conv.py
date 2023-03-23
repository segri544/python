import torch
import tensorrt as trt
import pycuda.driver as cuda
import pycuda.autoinit

# Define the input shape of the model
input_shape = (3, 224, 224)

# Load the PyTorch model
model = torch.load('model.pt', map_location=torch.device('cpu'))

# Create a TensorRT engine builder
builder = trt.Builder(trt.Logger(trt.Logger.WARNING))

# Set the maximum batch size and workspace size for the engine
max_batch_size = 1
max_workspace_size = 1 << 30
builder.max_batch_size = max_batch_size
builder.max_workspace_size = max_workspace_size

# Create a TensorRT network from the PyTorch model
network = builder.create_network()
input_tensor = network.add_input('input', trt.DataType.FLOAT, input_shape)
output_tensor = network.add_output('output', trt.DataType.FLOAT, (1000,))
output_tensor.set_softmax(True)
pt_engine = trt.tensorrt.PyTorchImporter(network, None)
pt_engine.import_weights(model)

# Build the TensorRT engine
engine = builder.build_cuda_engine(network)

# Save the TensorRT engine to a file
with open('model.engine', 'wb') as f:
    f.write(engine.serialize())
