from .skorch.callbacks import MetricsLogger


class NeptuneSkorchCallback(MetricsLogger):
    def __init__(self, ctx, batch_targets=None, epoch_targets=None):
        super().__init__(
            batch_targets=batch_targets, epoch_targets=epoch_targets)
        self.ctx = ctx

    def update_batch_values(self, values, idx):
        for name, value in values.items():
            self.ctx.channel_send(name, idx, value)

    def update_epoch_values(self, values, idx):
        for name, value in values.items():
            self.ctx.channel_send(name, idx, value)
