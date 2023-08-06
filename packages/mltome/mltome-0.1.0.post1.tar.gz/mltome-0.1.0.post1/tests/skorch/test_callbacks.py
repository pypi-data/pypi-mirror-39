from unittest.mock import ANY, call, Mock

import pytest
import numpy as np
import torch
import torch.nn as nn

from skorch.net import NeuralNet
from mltome.skorch.callbacks import LRRecorder
from mltome.skorch.callbacks import TensorboardXLogger


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


# LRRecorder
def test_lr_recorder_default_lr_per_epoch(data):
    module = MyModule()
    X, y = data

    recorder = LRRecorder(per_epoch=True)
    net = NeuralNet(
        module,
        torch.nn.MSELoss,
        callbacks=[recorder],
        max_epochs=5,
        optimizer__lr=0.1,
        batch_size=100)
    net.fit(X, y)

    lrs = net.history[:, 'default_lr']
    assert lrs == [0.1] * 5


def test_lr_recorder_default_lr_per_batch(data):
    module = MyModule()
    X, y = data

    recorder = LRRecorder(per_epoch=False)
    net = NeuralNet(
        module,
        torch.nn.MSELoss,
        callbacks=[recorder],
        max_epochs=5,
        optimizer__lr=0.1,
        batch_size=100)
    net.fit(X, y)

    lrs_per_epoch = net.history[:, 'batches', :, 'default_lr']
    for lr in lrs_per_epoch:
        assert lr == [0.1] * 10


def test_lr_recorder_custom_lr_per_epoch(data):
    module = MyModule()
    X, y = data

    param_group = [('layer1.*', {'lr': 0.01})]
    params_names = [name for name, _ in param_group]
    recorder = LRRecorder(group_names=params_names, per_epoch=True)

    net = NeuralNet(
        module,
        torch.nn.MSELoss,
        callbacks=[recorder],
        max_epochs=5,
        optimizer__lr=0.1,
        batch_size=100,
        optimizer__param_groups=param_group)
    net.fit(X, y)

    lrs = net.history[:, 'layer1.*']
    assert lrs == [0.01] * 5

    lrs = net.history[:, 'default_lr']
    assert lrs == [0.10] * 5


def test_lr_recorder_custom_lr_per_batch(data):
    module = MyModule()
    X, y = data

    param_group = [('layer1.*', {'lr': 0.01})]
    params_names = [name for name, _ in param_group]
    recorder = LRRecorder(group_names=params_names, per_epoch=False)

    net = NeuralNet(
        module,
        torch.nn.MSELoss,
        callbacks=[recorder],
        max_epochs=5,
        optimizer__lr=0.1,
        batch_size=100,
        optimizer__param_groups=param_group)
    net.fit(X, y)

    lrs_per_epoch_layer1 = net.history[:, 'batches', :, 'layer1.*']
    for lr in lrs_per_epoch_layer1:
        assert lr == [0.01] * 10

    lrs_per_epoch_default = net.history[:, 'batches', :, 'default_lr']
    for lr in lrs_per_epoch_default:
        assert lr == [0.1] * 10


def test_tensorboard_logger(monkeypatch, data, tmpdir):
    add_scalar_mock = Mock()
    add_scalars_mock = Mock()

    monkeypatch.setattr('tensorboardX.SummaryWriter.add_scalar',
                        add_scalar_mock)
    monkeypatch.setattr('tensorboardX.SummaryWriter.add_scalars',
                        add_scalars_mock)

    log_dir = str(tmpdir.mkdir('tensorboardx_log'))

    module = MyModule()

    tensor_logger = TensorboardXLogger(
        log_dir,
        batch_targets=['train_loss'],
        epoch_targets=['valid_loss'],
        batch_groups=['train_loss'],
        epoch_groups=['valid_loss'])
    net = NeuralNet(
        module,
        torch.nn.MSELoss,
        callbacks=[tensor_logger],
        max_epochs=2,
        batch_size=100)

    X, y = data

    net.fit(X, y)

    batch_calls = [call('batch/train_loss', ANY, i) for i in range(8)]
    batch_calls += [call('batch/train_loss', ANY, i) for i in range(10, 18)]
    epoch_calls = [call('epoch/valid_loss', ANY, i) for i in range(1, 3)]
    add_scalar_mock.assert_has_calls(batch_calls + epoch_calls, any_order=True)

    batch_group_calls = [call('batch_train_loss', ANY, i) for i in range(8)]
    batch_group_calls += [
        call('batch_train_loss', ANY, i) for i in range(10, 18)
    ]
    epoch_group_calls = [call('epoch_valid_loss', ANY, i) for i in range(1, 3)]
    add_scalars_mock.assert_has_calls(
        batch_group_calls + epoch_group_calls, any_order=True)
