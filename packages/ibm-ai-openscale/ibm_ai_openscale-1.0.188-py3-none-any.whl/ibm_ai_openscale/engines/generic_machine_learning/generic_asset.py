import uuid
from ibm_ai_openscale.base_classes.assets import Asset
from ibm_ai_openscale.utils import validate_type


class GenericAsset(Asset):
    """
    Describes asset for generic engine.

    :param name: name of asset
    :type name: str
    :param binding_uid: binding_uid of asset (not necessary if only one generic binding exists)
    :type binding_uid: str
    :param source_uid: source uid of asset (optional)
    :type source_uid: str
    :param source_url: source url of asset (optional)
    :type source_url: str
    :param asset_type: type of asset - may be one of ['model', 'function'] (default: model)
    :type asset_type: str
    :param frameworks: frameworks used with asset (optional, only for display purposes, will not be saved in AIOS)
    :type frameworks: list of Framework
    :param source_entry: source entry describing asset (optional, will not be saved in AIOS)
    :type source_entry: dict
    :param scoring_url: scoring endpoint url (optional)
    :type scoring_url: str
    :param scoring_headers: request headers (optional)
    :type scoring_headers: dict
    :param scoring_authorization: dict describing authorization method and credentials {'method': , 'credentials': {}} (optional)
    :type scoring_authorization: dict
    """
    def __init__(self, name, binding_uid=None, source_uid=None, source_url=None,
                 asset_type='model', frameworks=[], source_entry=None, scoring_url=None,
                 scoring_authorization=None, scoring_headers=None):

        validate_type(name, "name", str, True)
        validate_type(binding_uid, "binding_uid", str, False)
        validate_type(source_uid, "source_uid", str, False)
        validate_type(source_url, "source_url", str, False)
        validate_type(asset_type, "asset_type", str, False)
        validate_type(frameworks, "frameworks", list, False)
        validate_type(source_entry, "source_entry", dict, False)
        validate_type(scoring_url, "scoring_url", str, False)
        validate_type(scoring_authorization, "scoring_authorization", dict, False)
        validate_type(scoring_headers, "scoring_headers", dict, False)

        Asset.__init__(self, binding_uid)

        self.name = name
        self.source_uid = source_uid if source_uid is not None else 'generic_uid_' + str(uuid.uuid4())
        self.source_url = source_url
        self.asset_type = asset_type
        self.frameworks = frameworks
        self.source_entry = source_entry
        self.scoring_url = scoring_url
        self.scoring_headers = scoring_headers
        self.scoring_authorization = scoring_authorization
