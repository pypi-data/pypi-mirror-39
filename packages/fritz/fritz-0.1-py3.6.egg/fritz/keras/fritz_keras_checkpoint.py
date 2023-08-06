import os
import keras  # pylint: disable=import-error
from fritz.client import FritzClient


class FritzModelCheckpoint(keras.callbacks.Callback):
    """A callback to save local model checkpoints to Fritz."""

    def __init__(self,
                 fritz_api_key,
                 model_uid,
                 keras_filename,
                 convert_function,
                 epoch_frequency=1,
                 deploy=True):
        """Save a checkpoint to Fritz."""
        self._client = FritzClient(fritz_api_key)
        self._model_uid = model_uid
        self._keras_filename = keras_filename
        self._epoch_frequency = epoch_frequency
        self._deploy = deploy
        self._convert_func = convert_function

    def on_epoch_end(self, epoch, logs=None):
        """Save model to Fritz on epoch end.

        Args:
            epoch (int): the epoch number
            logs (dict, optional): logs dict
        """
        if epoch % self._epoch_frequency != 0:
            return

        converted_model = self._convert_func(self.model)
        metadata = {
            'epoch': epoch,
            'keras_model_path': self._keras_filename,
        }

        mlmodel_filename = os.path.splitext(
            os.path.basename(self._keras_filename)
        )[0] + '.mlmodel'
        self._client.upload_new_version(self._model_uid,
                                        mlmodel_filename,
                                        mlmodel=converted_model,
                                        set_active=self._deploy,
                                        metadata=metadata)
