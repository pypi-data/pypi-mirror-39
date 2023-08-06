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

from ibm_ai_openscale import APIClient, APIClient4ICP
from ibm_ai_openscale.engines import *
from preparation_and_cleaning import *


class TestAIOpenScaleClient(unittest.TestCase):
    deployment_uid = None
    function_uid = None
    subscription_uid = None
    scoring_url = None
    labels = None
    ai_client = None
    wml_client = None
    binding_uid = None
    subscription = None
    test_uid = str(uuid.uuid4())

    @classmethod
    def setUpClass(cls):
        cls.schema = get_schema_name()
        cls.aios_credentials = get_aios_credentials()
        cls.database_credentials = get_database_credentials()

        if "ICP" in get_env():
            cls.ai_client = APIClient4ICP(cls.aios_credentials)
        else:
            cls.ai_client = APIClient(cls.aios_credentials)
            cls.wml_credentials = get_wml_credentials()

        prepare_env(cls.ai_client)

    def test_01_setup_data_mart(self):
        TestAIOpenScaleClient.ai_client.data_mart.setup(db_credentials=self.database_credentials, schema=self.schema)

    def test_02_data_mart_get_details(self):
        details = TestAIOpenScaleClient.ai_client.data_mart.get_details()
        print(details)
        self.assertTrue(len(json.dumps(details)) > 10)

    def test_03_bind_wml_instance(self):
        if "ICP" in get_env():
            TestAIOpenScaleClient.binding_uid = self.ai_client.data_mart.bindings.add("WML instance on ICP", WatsonMachineLearningInstance4ICP())
        else:
            TestAIOpenScaleClient.binding_uid = self.ai_client.data_mart.bindings.add("WML instance on Cloud", WatsonMachineLearningInstance(self.wml_credentials))

    def test_04_get_wml_client(self):
        binding_uid = TestAIOpenScaleClient.ai_client.data_mart.bindings.get_uids()[0]
        TestAIOpenScaleClient.wml_client = TestAIOpenScaleClient.ai_client.data_mart.bindings.get_native_engine_client(binding_uid)

    def test_05_list_instances(self):
        TestAIOpenScaleClient.ai_client.data_mart.bindings.list()

    def test_06_get_uids(self):
        TestAIOpenScaleClient.ai_client.data_mart.bindings.get_uids()

    def test_07_get_details(self):
        print("Data mart details: {}".format(TestAIOpenScaleClient.ai_client.data_mart.bindings.get_details()))

    def test_08_prepare_deployment(self):

        function_name = "AIOS score function"
        function_deployment_name = "AIOS score function deployment"

        wml_models = self.wml_client.repository.get_details()

        for function in wml_models['functions']['resources']:
            if function_name == function['entity']['name']:
                TestAIOpenScaleClient.function_uid = function['metadata']['guid']
                break

        if self.function_uid is None:
            print("Storing function ...")

            def score(payload):
                values = [[row[0]*row[1]] for row in payload['values']]
                return {'fields': ['multiplication'], 'values': values}

            ai_function_details = self.wml_client.repository.store_function(score, function_name)
            TestAIOpenScaleClient.function_uid = self.wml_client.repository.get_function_uid(ai_function_details)

        wml_deployments = self.wml_client.deployments.get_details()

        for deployment in wml_deployments['resources']:
            if function_deployment_name == deployment['entity']['name']:
                TestAIOpenScaleClient.deployment_uid = deployment['metadata']['guid']
                break

        if self.deployment_uid is None:
            print("Deploying funtion...")

            deployment = self.wml_client.deployments.create(artifact_uid=TestAIOpenScaleClient.function_uid, name=function_deployment_name, asynchronous=False)
            TestAIOpenScaleClient.deployment_uid = self.wml_client.deployments.get_uid(deployment)

        print("Function id: {}".format(self.function_uid))
        print("Deployment id: {}".format(self.deployment_uid))

    def test_09_list_subscriptions(self):
        TestAIOpenScaleClient.ai_client.data_mart.subscriptions.list()

    def test_10_subscribe(self):
        subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.add(WatsonMachineLearningAsset(TestAIOpenScaleClient.function_uid))
        TestAIOpenScaleClient.subscription_uid = subscription.uid

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
        TestAIOpenScaleClient.subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.get(name='AIOS score function', choose='random')
        TestAIOpenScaleClient.subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.get(name='AIOS score function', choose='first')
        TestAIOpenScaleClient.subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.get(name='AIOS score function', choose='last')
        TestAIOpenScaleClient.subscription.get_details()

    def test_16_list_deployments(self):
        TestAIOpenScaleClient.subscription.list_deployments()

    def test_17_get_metrics(self):
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics())
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(deployment_uid=TestAIOpenScaleClient.deployment_uid))
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(subscription_uid=TestAIOpenScaleClient.subscription.uid))
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(asset_uid=TestAIOpenScaleClient.subscription.source_uid))
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(metric_type='quality'))

    def test_18_unsubscribe(self):
        self.ai_client.data_mart.subscriptions.delete(self.subscription_uid)

    def test_19_unbind(self):
        self.ai_client.data_mart.bindings.delete(self.binding_uid)

    @classmethod
    def tearDownClass(cls):
        print("Deleting DataMart.")
        cls.ai_client.data_mart.delete()


if __name__ == '__main__':
    unittest.main()
