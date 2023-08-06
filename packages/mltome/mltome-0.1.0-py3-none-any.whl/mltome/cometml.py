from .skorch.callbacks import MetricsLogger


class CometSkorchCallback(MetricsLogger):
    def __init__(self, exp, batch_targets=None, epoch_targets=None):
        super().__init__(
            batch_targets=batch_targets, epoch_targets=epoch_targets)
        self.exp = exp

    def update_batch_values(self, values, idx):
        self.exp.log_metrics(values, step=idx)

    def update_epoch_values(self, values, idx):
        self.exp.log_metrics(values, step=idx)
