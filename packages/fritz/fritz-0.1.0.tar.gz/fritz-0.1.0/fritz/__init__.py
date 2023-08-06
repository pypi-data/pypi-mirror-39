"""
Fritz ML Library
~~~~~~~~~~~~~~~~
Fritz is a library to simplify your mobile machine learning workflow.

usage:
   >>> import fritz
   >>> client = fritz.client.FritzClient('<your api key>')
   >>> model_details = client.upload_new_model_version(
           '<model_uid>', '/path/to/your_great_model.mlmodel'
       )
   >>> print(model_details)
   {
       'model': {'uid': '<model_uid>', ...}
       'version': {'uid': '<version_uid>', ...}
   }

:copyright: © 2018 by Fritz Labs Incorporated
:license: MIT, see LICENSE for more details.
"""

from fritz import client
