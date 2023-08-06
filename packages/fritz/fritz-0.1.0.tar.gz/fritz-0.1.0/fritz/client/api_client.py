"""
fritz.client.api_client
~~~~~~~~~~~~~~~~~~~~~~~
This module contains the FritzClient for interacting with the Fritz API.
"""

import json
import io
import os

import requests


class FritzClientBase(object):
    """Fritz Client to interact with Fritz API."""

    def __init__(self, api_key, base_url):
        """
        Args:
            api_key (str): Account API Key for Fritz API.
            base_url (str): URL base of Fritz API.
        """
        self._api_key = api_key
        self._base_url = base_url

    @staticmethod
    def _create_streamable_mlmodel(model):
        """Convert mlmodel model into BytesIO object ready for streaming.

        Args:
            model (coremltools.models.MLModel): Model to upload
        """
        serialized_spec = model.get_spec().SerializeToString()
        return io.BytesIO(serialized_spec)

    def upload_new_version(self,
                           model_uid,
                           model_path,
                           mlmodel=None,
                           set_active=False,
                           metadata=None):
        """Upload new version of a model.

        Args:
            model_uid (str): Model Identifier to update.
            model_path (str): Path to saved model. If mlmodel is not provided,
                model will be loaded from this path.
            mlmodel (coremltools.models.MLModel): Optional MLModel file to
                upload.  If this is not provided, MLModel file will be uploaded
                from model_path.
            set_active (bool): If True, will set active version of model to
                newly uploaded model.
            metadata (Dict): Dictionary of JSON serializable metadata about
                model.

        Returns: Model and ModelVersion of uploaded model.
        """
        path = os.path.join(
            self._base_url,
            'client/v1/model/{model_uid}/version'.format(model_uid=model_uid)
        )
        if mlmodel:
            data = self._create_streamable_mlmodel(mlmodel)
        else:
            data = open(model_path, 'rb')

        response = requests.post(
            path,
            headers={
                'Authorization': self._api_key,
            },
            data={
                'metadata_json': json.dumps(metadata or {}),
                'set_active': set_active,
            },
            files={'file': (os.path.basename(model_path), data)}
        )

        data.close()
        return response.json()


class FritzClient(FritzClientBase):
    """Client used to interact with the Production Fritz API."""
    API_PATH = 'https://api.fritz.ai'

    def __init__(self, api_key):
        super(FritzClient, self).__init__(api_key, self.API_PATH)
