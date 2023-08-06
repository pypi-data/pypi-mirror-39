# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-J33
# Copyright IBM Corp. 2018
# The source code for this program is not published or other-wise divested of its trade 
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

import unittest

from models.spark import GoSales
from test_base import TestBasePostgres


class TestAIOpenScaleClient(TestBasePostgres):

    model = GoSales()

    def test_01_create_client(self):
        self.create_client()

    def test_02_setup_data_mart(self):
        self.setup_data_mart()

    def test_03_data_mart_get_details(self):
        self.get_data_mart_details()

    def test_04_bind_wml_instance(self):
        self.bind_wml_instance()

    def test_05_get_wml_client(self):
        self.get_wml_client()

    def test_06_list_instances(self):
        self.list_instances()

    def test_07_get_binding_uid(self):
        self.get_binding_id()

    def test_08_get_binding_details(self):
        self.get_binding_details()

    def test_08_prepare_model(self):
        self.publish_model(self.model)

    def test_09_list_subscriptions(self):
        self.list_subscription()

    def test_10_subscribe(self):
        self.subscribe()

    def test_11_list_deployments(self):
        self.list_deployments()

    def test_12_get_deployments(self):
        deployments_list = TestBasePostgres.subscription.get_deployment_uids()
        print("Deployments uids: {}".format(deployments_list))
        self.assertTrue(len(deployments_list) == 0)

    def test_13_list_and_get_uids_after_subscribe(self):
        TestBasePostgres.ai_client.data_mart.subscriptions.list()
        TestBasePostgres.ai_client.data_mart.subscriptions.list(name='Test_' + self.test_uid)
        subscription_uids = TestBasePostgres.ai_client.data_mart.subscriptions.get_uids()
        self.assertTrue(len(subscription_uids) > 0)

    def test_14_prepare_deployment(self):
        self.deploy_model()

    def test_15_update_deployments(self):
        TestBasePostgres.subscription.update()

    def test_16_check_if_deployments_were_added(self):
        deployments_list =  TestBasePostgres.subscription.get_deployment_uids()
        print("Deployments uids: {}".format(deployments_list))
        self.assertTrue(len(deployments_list) > 0)
        self.assertIn(TestBasePostgres.deployment_uid, deployments_list)

        self.assertTrue(len( TestBasePostgres.ai_client.data_mart.subscriptions.get_details()['subscriptions'][0]['entity']['deployments']) > 0)

    def test_17_list_models_and_functions(self):
        TestAIOpenScaleClient.ai_client.data_mart.bindings.list_assets()

    def test_18_get_asset_uids(self):
        asset_uids = TestBasePostgres.ai_client.data_mart.bindings.get_asset_uids()
        print("Asset uids: {}".format(asset_uids))
        self.assertTrue(len(asset_uids) > 0)
        self.assertIn(TestBasePostgres.model_uid, asset_uids)

    def test_19_select_asset_and_get_details(self):
        self.select_asset_and_get_details()

    def test_20_unsubscribe(self):
        self.unsubscribe()

    def test_21_unbind(self):
        self.unbind()

    def test_22_delete_data_mart(self):
        self.delete_data_mart()


if __name__ == '__main__':
    unittest.main()
