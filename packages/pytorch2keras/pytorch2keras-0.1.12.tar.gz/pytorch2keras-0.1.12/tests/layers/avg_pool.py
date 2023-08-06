import numpy as np
import torch
import torch.nn as nn
from torch.autograd import Variable
from pytorch2keras.converter import pytorch_to_keras


class AvgPool(nn.Module):
    """Module for AveragePool conversion testing
    """

    def __init__(self, inp=10, out=16, kernel_size=3, bias=True):
        super(AvgPool, self).__init__()
        # self.conv2d = nn.Conv2d(inp, out, kernel_size=kernel_size, padding=1, bias=bias)
        # self.pool = nn.((1,1))

    def forward(self, x):
        # x = self.conv2d(x)
        import torch.nn.functional as F
        x = F.adaptive_avg_pool2d(x, (1, 1))
        return x


if __name__ == '__main__':
    max_error = 0
    for i in range(100):
        kernel_size = np.random.randint(4, 7)
        inp = np.random.randint(kernel_size + 1, 100)
        out = np.random.randint(1, 100)

        model = AvgPool(inp, out, kernel_size, inp % 2)

        input_np = np.random.uniform(0, 1, (1, inp, inp, inp))
        input_var = Variable(torch.FloatTensor(input_np))
        output = model(input_var)
        print('out', output.shape)
        k_model = pytorch_to_keras(model, input_var, (inp, inp, inp,), verbose=True, names='keep')
        print(k_model.summary())
        pytorch_output = output.data.numpy()
        keras_output = k_model.predict(input_np)
        print('out_k', keras_output.shape)

        error = np.max(pytorch_output - keras_output)
        print(error)
        if max_error < error:
            max_error = error

    print('Max error: {0}'.format(max_error))
