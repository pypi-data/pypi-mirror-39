from ibm_ai_openscale.base_classes.instances import AIInstance
from ibm_ai_openscale.utils import *
from .consts import AzureConsts
import uuid


class AzureMachineLearningInstance(AIInstance):
    """
    Describes Microsoft Azure Machine Learning instance.

    :param service_credentials: credentials of azure machine learning studio instance
    :type service_credentials: dict

    A way you might use me is:

    >>> credentials = {
    >>>                 "tenant": "username",
    >>>                 "client_secret": "password",
    >>>                 "subscription_id": "id",
    >>>                 "client_id": "id"
    >>> }
    >>>
    >>> client.bindings.add("Azure instance A", AzureMachineLearningInstance(credentials))
    """

    def __init__(self, service_credentials):
        validate_type(service_credentials, 'service_credentials', dict, True)
        validate_type(service_credentials['tenant'], 'service_credentials.tenant', str, False)
        validate_type(service_credentials['client_secret'], 'service_credentials.client_secret', str, False)
        validate_type(service_credentials['subscription_id'], 'service_credentials.subscription_id', str, False)
        validate_type(service_credentials['client_id'], 'service_credentials.client_id', str, False)

        #TODO do we need to validate what is inside credentials ???
        AIInstance.__init__(self, str(uuid.uuid4()), service_credentials, AzureConsts.SERVICE_TYPE)
