# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-J33
# Copyright IBM Corp. 2018
# The source code for this program is not published or other-wise divested of its trade 
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

from ibm_ai_openscale.base_classes.clients import Client
from ibm_ai_openscale.base_classes import Artifact, SourceDeployment
from ibm_ai_openscale.base_classes.assets import KnownServiceAsset
from .consts import CustomConsts
from ibm_ai_openscale.utils import *
import requests


class CustomClient(Client):
    service_type = CustomConsts.SERVICE_TYPE

    def __init__(self, binding_uid, service_credentials, project_id=None):
        Client.__init__(self, binding_uid)
        self.url = service_credentials['url']
        self.deployment_endpoint = self.url + '/v1/deployments'
        self.header = {}
        self.username = None
        self.password = None

        if 'username' in service_credentials.keys():
            self.username = service_credentials['username']

        if 'password' in service_credentials.keys():
            self.password = service_credentials['password']

        if 'header' in service_credentials.keys():
            self.header = service_credentials['header']

    def _make_artifact_from_details(self, details):

        return Artifact(
            details['entity']['asset']['guid'],
            details['entity']['scoring_url'],
            self.binding_uid,
            details['entity']['asset']['name'],
            'model',
            details['metadata']['created_at'],
            [],
            details,
            details['entity']['asset_properties']
        )

    def get_artifact(self, source_uid):
        details = self._get_deployments_details()
        asset_details = {}

        for detail in details:
            if detail['metadata']['guid'] == source_uid:
                asset_details = detail

        return self._make_artifact_from_details(asset_details)

    def prepare_artifact(self, asset):
        validate_type(asset, 'KnownServiceAsset', KnownServiceAsset, True)
        artifact = self.get_artifact(source_uid=asset.source_uid)

        if asset.input_data_type is not None:
            artifact.properties['input_data_type'] = asset.input_data_type
        if asset.problem_type is not None:
            artifact.properties['problem_type'] = asset.problem_type
        if asset.label_column is not None:
            artifact.properties['label_column'] = asset.label_column
        if asset.prediction_column is not None:
            artifact.properties['predicted_target_field'] = asset.prediction_column
        if asset.probability_column is not None:
            artifact.properties['prediction_probability_field'] = asset.probability_column

        return artifact

    def get_artifacts(self):
        models = self._get_deployments_details()
        unique_models = []
        unique_source_uids = set()

        for model in models:
            model_uid = model['entity']['asset']['guid']
            if model_uid not in unique_source_uids:
                unique_models.append(model)
            unique_source_uids.add(model_uid)

        return [self._make_artifact_from_details(asset) for asset in unique_models]

    def _get_deployments_details(self):
        if self.username is not None and self.password is not None:
            response = requests_session.get(self.deployment_endpoint, auth=(self.username, self.password), headers=self.header)
        else:
            response = requests_session.get(self.deployment_endpoint, headers=self.header)

        if response.status_code == 200:
            deployments = response.json()['resources']

        return deployments

    def get_deployments(self, asset=None, deployment_uids=None):
        deployments = self._get_deployments_details()

        if asset is None and deployment_uids is None:
            return [
                SourceDeployment(
                    deployment['metadata']['guid'],
                    '',
                    deployment['entity']['name'],
                    'online',
                    deployment['metadata']['created_at'],
                    scoring_endpoint={'url': deployment['entity']['scoring_url']},
                ) for deployment in deployments
            ]
        elif asset is not None and deployment_uids is None:
            return [
                SourceDeployment(
                    deployment['metadata']['guid'],
                    '',
                    deployment['entity']['name'],
                    'online',
                    deployment['metadata']['created_at'],
                    scoring_endpoint={'url': deployment['entity']['scoring_url']},
                ) for deployment in deployments if deployment['entity']['asset']['guid'] == asset.source_uid
            ]
        elif asset is None and deployment_uids is not None:
            return [
                SourceDeployment(
                    deployment['metadata']['guid'],
                    '',
                    deployment['entity']['name'],
                    'online',
                    deployment['metadata']['created_at'],
                    scoring_endpoint={'url': deployment['entity']['scoring_url']},
                ) for deployment in deployments if deployment['metadata']['guid'] in deployment_uids
            ]
        else:
            return [
                SourceDeployment(
                    deployment['metadata']['guid'],
                    '',
                    deployment['entity']['name'],
                    'online',
                    deployment['metadata']['created_at'],
                    scoring_endpoint={'url': deployment['entity']['scoring_url']},
                ) for deployment in deployments if (deployment['metadata']['guid'] in deployment_uids and deployment['entity']['asset']['guid'] == asset.source_uid)
            ]