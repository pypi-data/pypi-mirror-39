# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-J33
# Copyright IBM Corp. 2018
# The source code for this program is not published or other-wise divested of its trade 
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------


import unittest

from ibm_ai_openscale import APIClient, APIClient4ICP
from ibm_ai_openscale.engines import *
from preparation_and_cleaning import *
from models.spark import GoSales


class TestAIOpenScaleClient(unittest.TestCase):
    binding_uid = None
    deployment_uid = None
    model_uid = None
    aios_model_uid = None
    scoring_url = None
    labels = None
    ai_client = None
    wml_client = None
    subscription = None
    subscription_uid = None
    test_uid = str(uuid.uuid4())

    model = GoSales()

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
        details = self.ai_client.data_mart.get_details()
        print("Datamart details: {}".format(details))
        self.assertTrue(len(json.dumps(details)) > 10)

    def test_04_bind_wml_instance(self):
        if "ICP" in get_env():
            TestAIOpenScaleClient.binding_uid = self.ai_client.data_mart.bindings.add("WML instance on ICP", WatsonMachineLearningInstance4ICP())
        else:
            TestAIOpenScaleClient.binding_uid = self.ai_client.data_mart.bindings.add("WML instance on Cloud", WatsonMachineLearningInstance(self.wml_credentials))
        self.assertIsNotNone(self.binding_uid)

    def test_05_get_wml_client(self):
        binding_uid = TestAIOpenScaleClient.ai_client.data_mart.bindings.get_uids()[0]
        print("Binding id: {}".format(binding_uid))
        self.assertEqual(binding_uid, TestAIOpenScaleClient.binding_uid)

        TestAIOpenScaleClient.wml_client = TestAIOpenScaleClient.ai_client.data_mart.bindings.get_native_engine_client(
            binding_uid)
        self.assertIsNotNone(TestAIOpenScaleClient.wml_client)

    def test_06_list_instances(self):
        self.ai_client.data_mart.bindings.list()

    def test_07_get_binding_uid(self):
        print("Bindings list:\n")
        self.ai_client.data_mart.bindings.list()
        binding_uid = self.ai_client.data_mart.bindings.get_uids()[0]
        print("Datamart details binding guid: {}".format(binding_uid))
        self.assertIsNotNone(binding_uid)
        self.assertEqual(binding_uid, self.binding_uid)

    def test_08_get_binding_details(self):
        binding_details = self.ai_client.data_mart.bindings.get_details()
        print("Binding details: {}".format(binding_details))
        self.assertIsNotNone(binding_details)

    def test_09_prepare_model(self):
        wml_models = self.wml_client.repository.get_details()

        for model in wml_models['models']['resources']:
            if self.model.model_name == model['entity']['name']:
                TestAIOpenScaleClient.model_uid = model['metadata']['guid']
                break

        if self.model_uid is None:
            print("Storing model ...")

            published_model_details = self.model.publish_to_wml(self.wml_client)
            TestAIOpenScaleClient.model_uid = self.wml_client.repository.get_model_uid(published_model_details)

        print("Model id: {}".format(self.model_uid))

    def test_10_list_subscriptions(self):
        self.ai_client.data_mart.subscriptions.list()

    def test_11_subscribe(self):
        TestAIOpenScaleClient.subscription = self.ai_client.data_mart.subscriptions.add(
            WatsonMachineLearningAsset(self.model_uid))
        print("Subscription: {}".format(self.subscription))
        self.assertIsNotNone(self.subscription)
        TestAIOpenScaleClient.subscription_uid = self.subscription.uid

    def test_12_list_deployments(self):
        print("Listing deployments:\n")
        self.subscription.list_deployments()

    def test_13_get_deployments(self):
        deployments_list = self.subscription.get_deployment_uids()
        print("Deployments uids: {}".format(deployments_list))
        self.assertTrue(len(deployments_list) == 1)

    def test_14_list_and_get_uids_after_subscribe(self):
        TestAIOpenScaleClient.ai_client.data_mart.subscriptions.list()
        TestAIOpenScaleClient.ai_client.data_mart.subscriptions.list(name=self.model.model_name)
        subscription_uids = self.ai_client.data_mart.subscriptions.get_uids()
        self.assertTrue(len(subscription_uids) > 0)

    def test_15_prepare_deployment(self):
        deployment = self.wml_client.deployments.create(artifact_uid=self.model_uid, name=self.model.deployment_name, asynchronous=False)
        TestAIOpenScaleClient.deployment_uid = self.wml_client.deployments.get_uid(deployment)
        print("New deployment uid: {}".format(self.deployment_uid))

    def test_16_update_deployments(self):
        TestAIOpenScaleClient.subscription.update()

    def test_17_check_if_deployments_were_added(self):
        deployments_list = self.subscription.get_deployment_uids()
        print("Deployments uids: {}".format(deployments_list))
        self.assertTrue(len(deployments_list) == 2)
        self.assertIn(self.deployment_uid, deployments_list)

        self.assertTrue(len(self.ai_client.data_mart.subscriptions.get_details()['subscriptions'][0]['entity']['deployments']) > 0)

    def test_18_list_models_and_functions(self):
        TestAIOpenScaleClient.ai_client.data_mart.bindings.list_assets()

    def test_19_get_asset_uids(self):
        asset_uids = self.ai_client.data_mart.bindings.get_asset_uids()
        print("Asset uids: {}".format(asset_uids))
        self.assertTrue(len(asset_uids) > 0)
        self.assertIn(self.model_uid, asset_uids)

    def test_20_select_asset_and_get_details(self):
        TestAIOpenScaleClient.subscription = self.ai_client.data_mart.subscriptions.get(self.subscription_uid)
        self.assertIsNotNone(self.subscription)

    def test_21_delete_deployment(self):
        self.wml_client.deployments.delete(deployment_uid=self.deployment_uid)

    def test_22_unsubscribe(self):
        self.ai_client.data_mart.subscriptions.delete(self.subscription.uid)

    def test_23_unbind(self):
        self.ai_client.data_mart.bindings.delete(self.binding_uid)

    @classmethod
    def tearDownClass(cls):
        print("Deleting DataMart.")
        cls.ai_client.data_mart.delete()


if __name__ == '__main__':
    unittest.main()
