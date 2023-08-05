import numpy as np
import torch
import torch.nn as nn
from torch.autograd import Variable
from pytorch2keras.converter import pytorch_to_keras


class TestLSTM(nn.Module):
    """Module for TestLSTM conversion testing
    """

    def __init__(self, inp=10, out=16, kernel_size=3, bias=True):
        super(TestLSTM, self).__init__()
        self.rnn = nn.LSTM(10, 10, 3)

    def forward(self, x):
        x, (hn, cn) = self.rnn(x)
        x, (hn, cn) = self.rnn(x)
        x, (hn, cn) = self.rnn(x)
        return x


if __name__ == '__main__':
    max_error = 0
    for i in range(100):
        inp = np.random.randint(10, 100)
        out = np.random.randint(10, 100)

        model = TestLSTM()
        print(model)

        input_np = np.random.uniform(0, 1, (5, 3, 10))
        input_var = Variable(torch.FloatTensor(input_np))
        output = model(input_var)

        k_model = pytorch_to_keras(model, input_var, (5, 3, 10,), verbose=True)

        pytorch_output = output.data.numpy()
        keras_output = k_model.predict(input_np)

        error = np.max(pytorch_output - keras_output)
        print(error)
        if max_error < error:
            max_error = error

    print('Max error: {0}'.format(max_error))
