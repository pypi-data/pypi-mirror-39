from contextlib import suppress

import numpy as np
from skorch.callbacks.base import Callback

from .callbacks import LRRecorder


class LRFinder(Callback):
    def __init__(self, start_lr, end_lr, warm_start=10, scale_linear=False):

        self.start_lrs = start_lr
        self.end_lrs = end_lr
        self.scale_linear = scale_linear

        self.lr_multiplier = None
        self.warm_start = warm_start
        self.final_valid_batch_idx = None

    def initialize(self):
        self.batch_idx_ = 0

    def on_train_begin(self, net, X, **kwargs):
        self.best_loss = 1e9
        self.total_samples = net.max_epochs * len(X)
        self.best_batch_idx = 0

        optimizer = net.optimizer_
        self.start_lrs = self._format_lrs("start_lr", optimizer,
                                          self.start_lrs)
        self.end_lrs = self._format_lrs("end_lr", optimizer, self.end_lrs)
        self.optimizer = optimizer

    def on_batch_begin(self, net, X, **kwargs):
        if self.lr_multiplier is None:
            ratio = self.end_lrs / self.start_lrs
            num_of_batches = self.total_samples // len(X)

            self.lr_multiplier = ratio / num_of_batches
            if not self.scale_linear:
                self.lr_multiplier = ratio**(1 / num_of_batches)

        self.batch_step(self.batch_idx_)

    def on_batch_end(self, net, **kwargs):
        loss = net.history[-1, 'batches', -1, 'train_loss']
        if not np.isfinite(loss) or loss > 4 * self.best_loss:
            raise ValueError("loss is too big")
        if loss < self.best_loss and self.batch_idx_ > self.warm_start:
            self.best_loss = loss
            self.best_lr = self.get_lr(self.batch_idx_)
        self.batch_idx_ += 1

    def _format_lrs(self, name, optimizer, lr):
        if isinstance(lr, (list, tuple)):
            if len(lr) != len(optimizer.param_groups):
                raise ValueError(
                    f"expected {len(optimizer.param_groups)} values for "
                    f"{name}, got {len(lr)}")
            return np.array(lr)
        else:
            return lr * np.ones(len(optimizer.param_groups))

    def batch_step(self, batch_idx):
        lrs = self.get_lr(batch_idx)
        pgroups_lr = zip(self.optimizer.param_groups, lrs)
        for param_group, lr in pgroups_lr:
            param_group['lr'] = lr

    def get_lr(self, batch_idx):
        mult = self.lr_multiplier * (batch_idx + 1)
        if not self.scale_linear:
            mult = self.lr_multiplier**(batch_idx + 1)
        return self.start_lrs * mult


def lr_find(net_cls,
            module,
            criterion,
            batch_size,
            X,
            iterations,
            y=None,
            start_lr=1e-5,
            end_lr=10,
            scale_linear=False,
            **kwargs):
    lr_finder = ('lr_finder',
                 LRFinder(
                     start_lr=start_lr,
                     end_lr=end_lr,
                     scale_linear=scale_linear))
    lr_recorder = ('lr_recorder', LRRecorder(per_epoch=False))
    callbacks = [lr_finder, lr_recorder]

    epochs = iterations // len(X)

    net = net_cls(
        module,
        criterion=criterion,
        max_epochs=epochs,
        batch_size=batch_size,
        callbacks=callbacks,
        train_split=None,
        **kwargs)

    with suppress(ValueError):
        net.fit(X, y)

    return net, lr_finder[1]


def plot_lr(history, lr_finder, ax):
    if not lr_finder.scale_linear:
        ax.set_xscale('log')

    losses = history[:, 'batches', 'train_loss'][0]
    lrs = history[:, 'batches', 'default_lr'][0]
    ax.vlines(lr_finder.best_lr, min(losses), max(losses), color='r')
    ax.set_ylim(min(losses), max(losses))
    ax.set_xlabel("Learning rate (log-scaled)")
    ax.set_ylabel("Loss")
    ax.plot(lrs, losses)
