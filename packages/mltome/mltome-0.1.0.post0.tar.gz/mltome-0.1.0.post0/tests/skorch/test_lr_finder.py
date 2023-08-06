import pytest
import numpy as np
import torch.nn as nn
from skorch import NeuralNetRegressor

from mltome.skorch.lr_finder import lr_find


class MyModule(nn.Module):
    def __init__(self):
        super().__init__()
        self.layer1 = nn.Linear(1, 2)
        self.layer2 = nn.Linear(2, 1)

    def forward(self, x):
        return self.layer2(self.layer1(x))


@pytest.fixture
def data():
    X = np.ones((1000, 1), dtype='float32')
    y = np.ones((1000, 1), dtype='float32')
    return X, y


def test_lr_find(data):
    X, y = data
    net, lr_finder = lr_find(NeuralNetRegressor, MyModule, nn.MSELoss, 100, X,
                             1000, y)

    assert net.max_epochs == 1
