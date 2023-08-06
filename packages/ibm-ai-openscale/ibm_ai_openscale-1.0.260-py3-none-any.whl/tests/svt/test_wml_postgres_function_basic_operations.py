# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-J33
# Copyright IBM Corp. 2018
# The source code for this program is not published or other-wise divested of its trade 
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

import logging
import unittest

from ibm_ai_openscale import APIClient
from ibm_ai_openscale.engines import *
from models_preparation import *
from preparation_and_cleaning import *


class TestAIOpenScaleClient(unittest.TestCase):
    deployment_uid = None
    function_uid = None
    subscription_uid = None
    scoring_url = None
    labels = None
    logger = logging.getLogger(__name__)
    ai_client = None
    wml_client = None
    subscription = None
    test_uid = str(uuid.uuid4())

    @classmethod
    def setUpClass(self):
        TestAIOpenScaleClient.logger.info("Service Instance: setting up credentials")

        clean_env()

        self.aios_credentials = get_aios_credentials()
        self.wml_credentials = get_wml_credentials()
        self.postgres_credentials = get_postgres_credentials()

    def test_01_create_client(self):
        TestAIOpenScaleClient.ai_client = APIClient(self.aios_credentials)

    def test_02_setup_data_mart(self):
        TestAIOpenScaleClient.ai_client.data_mart.setup(db_credentials=self.postgres_credentials, schema=get_schema_name())

    def test_03_data_mart_get_details(self):
        details = TestAIOpenScaleClient.ai_client.data_mart.get_details()
        print(details)
        self.assertTrue(len(json.dumps(details)) > 10)

    def test_04_bind_wml_instance_and_get_wml_client(self):
        TestAIOpenScaleClient.ai_client.data_mart.bindings.add("My WML instance", WatsonMachineLearningInstance(self.wml_credentials))

    def test_05_get_wml_client(self):
        binding_uid = TestAIOpenScaleClient.ai_client.data_mart.bindings.get_uids()[0]
        TestAIOpenScaleClient.wml_client = TestAIOpenScaleClient.ai_client.data_mart.bindings.get_native_engine_client(binding_uid)

    def test_06_list_instances(self):
        TestAIOpenScaleClient.ai_client.data_mart.bindings.list()

    def test_07_get_uids(self):
        TestAIOpenScaleClient.ai_client.data_mart.bindings.get_uids()

    def test_07b_get_details(self):
        print('DETAILS', TestAIOpenScaleClient.ai_client.data_mart.bindings.get_details())

    def test_08_prepare_deployment(self):
        def score(payload):
            values = [[row[0]*row[1]] for row in payload['values']]
            return {'fields': ['multiplication'], 'values': values}

        ai_function_details = self.wml_client.repository.store_function(score, "My func")

        TestAIOpenScaleClient.function_uid = self.wml_client.repository.get_function_uid(ai_function_details)

        deployment = self.wml_client.deployments.create(artifact_uid=TestAIOpenScaleClient.function_uid, name="Test deployment",
                                                        asynchronous=False)
        TestAIOpenScaleClient.deployment_uid = self.wml_client.deployments.get_uid(deployment)

    def test_09_list_subscriptions(self):
        TestAIOpenScaleClient.ai_client.data_mart.subscriptions.list()

    def test_10_subscribe(self):
        subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.add(WatsonMachineLearningAsset(TestAIOpenScaleClient.function_uid))
        TestAIOpenScaleClient.subscription_uid = subscription.uid
        # TODO check the deployments

    def test_11_list_and_get_uids_after_subscribe(self):
        TestAIOpenScaleClient.ai_client.data_mart.subscriptions.list()
        TestAIOpenScaleClient.ai_client.data_mart.subscriptions.list(name='test_' + self.test_uid)
        TestAIOpenScaleClient.ai_client.data_mart.subscriptions.get_uids()

    def test_12_check_if_deployments_were_added(self):
        self.assertTrue(len(TestAIOpenScaleClient.ai_client.data_mart.subscriptions.get_details()['subscriptions'][0]['entity']['deployments']) > 0)

    def test_13_list_models_and_functions(self):
        TestAIOpenScaleClient.ai_client.data_mart.bindings.list_assets()

    def test_14_get_asset_uids(self):
        TestAIOpenScaleClient.ai_client.data_mart.bindings.get_asset_uids()

    def test_15_select_asset_and_get_details(self):
        TestAIOpenScaleClient.subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.get(TestAIOpenScaleClient.subscription_uid)
        TestAIOpenScaleClient.subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.get(source_uid=TestAIOpenScaleClient.function_uid)
        TestAIOpenScaleClient.subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.get(name='My func', choose='random')
        TestAIOpenScaleClient.subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.get(name='My func', choose='first')
        TestAIOpenScaleClient.subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.get(name='My func', choose='last')
        TestAIOpenScaleClient.subscription.get_details()

    def test_15b_list_deployments(self):
        TestAIOpenScaleClient.subscription.list_deployments()

    def test_16_get_metrics(self):
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics())
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(deployment_uid=TestAIOpenScaleClient.deployment_uid))
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(subscription_uid=TestAIOpenScaleClient.subscription.uid))
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(asset_uid=TestAIOpenScaleClient.subscription.source_uid))
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(metric_type='quality'))

    def test_18_unsubscribe(self):
        TestAIOpenScaleClient.ai_client.data_mart.subscriptions.delete(TestAIOpenScaleClient.subscription.uid)
        wait_until_deleted(TestAIOpenScaleClient.ai_client, subscription_uid=TestAIOpenScaleClient.subscription.uid)

    def test_19_clean(self):
        self.wml_client.deployments.delete(TestAIOpenScaleClient.deployment_uid)
        self.wml_client.repository.delete(TestAIOpenScaleClient.function_uid)

    def test_20_unbind(self):
        TestAIOpenScaleClient.ai_client.data_mart.bindings.delete(TestAIOpenScaleClient.subscription.binding_uid)
        wait_until_deleted(TestAIOpenScaleClient.ai_client, binding_uid=TestAIOpenScaleClient.subscription.binding_uid)

    def test_21_delete_data_mart(self):
        TestAIOpenScaleClient.ai_client.data_mart.delete()
        wait_until_deleted(TestAIOpenScaleClient.ai_client, data_mart=True)
        delete_schema(get_postgres_credentials(), get_schema_name())


if __name__ == '__main__':
    unittest.main()
