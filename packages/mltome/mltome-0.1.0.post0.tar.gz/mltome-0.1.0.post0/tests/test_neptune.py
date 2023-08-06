from unittest.mock import NonCallableMagicMock, call

from mltome.neptune import NeptuneSkorchCallback


def test_neptunecallback():
    ctx_mock = NonCallableMagicMock()
    no = NeptuneSkorchCallback(
        ctx_mock, batch_targets=['train_loss'], epoch_targets=['valid_loss'])

    no.update_batch_values({'train_loss': 1}, 0)
    ctx_mock.channel_send.assert_has_calls([call('train_loss', 0, 1)])

    no.update_epoch_values({'valid_loss': 1}, 0)
    ctx_mock.channel_send.assert_has_calls([call('valid_loss', 0, 1)])
