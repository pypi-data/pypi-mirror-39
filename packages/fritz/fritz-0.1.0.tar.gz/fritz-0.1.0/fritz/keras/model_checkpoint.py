"""
fritz.keras.model_checkpoint
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This module contains a Keras Callback to upload new versions of a
model to Fritz.
"""


import os
import keras
from fritz.client import FritzClient


class FritzMLModelCheckpoint(keras.callbacks.Callback):
    """Saves current keras model version as a new mlmodel in Fritz."""

    def __init__(self,
                 fritz_api_key,
                 model_uid,
                 keras_filename,
                 convert_function,
                 period=1,
                 deploy=False):
        """Save a checkpoint to Fritz.

        Args:
            fritz_api_key (str): Fritz client API key.
            model_uid (str): Fritz Model UID to add new versions to.
            keras_filename (str): Name of keras model output filename.
            convert_function (func): Function used to convert keras model to
                MLModel.
            period (int): Interval (number of epochs) between checkpoints.
            deploy (bool): If True will set active version of model to latest
                uploaded model. Default False.
        """
        super(FritzMLModelCheckpoint, self).__init__()
        self._client = FritzClient(fritz_api_key)
        self._model_uid = model_uid
        self._keras_filename = keras_filename
        self._period = period
        self._deploy = deploy
        self._convert_func = convert_function

    def add_model_metadata(self, logs):  # noqa pylint: disable=unused-argument,no-self-use
        """Adds additional metadata about the model to be stored in Fritz.

        Optionally override this method returning custom information.

        Args:
            logs (dict): Includes values such as `acc` and `loss`.

        Returns: Dict of model metadata.
        """
        return {}

    def on_epoch_end(self, epoch, logs=None):
        """Saves model to Fritz on epoch end.

        Args:
            epoch (int): the epoch number
            logs (dict, optional): logs dict
        """
        if epoch % self._period != 0:
            return

        converted_model = self._convert_func(self.model)

        metadata = {
            'epoch': epoch,
            'keras_model_path': self._keras_filename,
        }
        metadata.update(self.add_model_metadata(logs))

        mlmodel_filename = os.path.splitext(
            os.path.basename(self._keras_filename)
        )[0] + '.mlmodel'
        self._client.upload_new_version(self._model_uid,
                                        mlmodel_filename,
                                        mlmodel=converted_model,
                                        set_active=self._deploy,
                                        metadata=metadata)

    def on_training_end(self, logs=None):
        """Saves model to Fritz at end of training run.

        Args:
            epoch (int): the epoch number
            logs (dict, optional): logs dict
        """
        converted_model = self._convert_func(self.model)

        metadata = {
            'keras_model_path': self._keras_filename,
        }
        metadata.update(self.add_model_metadata(logs))

        mlmodel_filename = os.path.splitext(
            os.path.basename(self._keras_filename)
        )[0] + '.mlmodel'
        self._client.upload_new_version(self._model_uid,
                                        mlmodel_filename,
                                        mlmodel=converted_model,
                                        set_active=self._deploy,
                                        metadata=metadata)
