from ibm_ai_openscale.base_classes.instances import AIInstance
from ibm_ai_openscale.utils import *
from .consts import CustomConsts
import uuid


class CustomMachineLearningInstance(AIInstance):
    """
    Describes Custom Machine Learning instance.

    :param service_credentials: credentials of custom instance containing: "url" to list deployments endpoint and optionally "username", "password"
    :type service_credentials: dict

    A way you might use me is:

    >>> credentials = {
    >>>                 "url": "list deployments endpoint url",
    >>>                 "username": "username",
    >>>                 "password": "password"
    >>> }
    >>>
    >>> client.bindings.add("Custom instance A", CustomMachineLearningInstance(credentials))
    """

    def __init__(self, service_credentials):
        validate_type(service_credentials, 'service_credentials', dict, True)
        validate_type(service_credentials['url'], 'service_credentials.url', str, True)
        validate_type(service_credentials['username'], 'service_credentials.username', str, False)
        validate_type(service_credentials['password'], 'service_credentials.password', str, False)

        #TODO do we need to validate what is inside credentials ???
        AIInstance.__init__(self, str(uuid.uuid4()), service_credentials, CustomConsts.SERVICE_TYPE)
