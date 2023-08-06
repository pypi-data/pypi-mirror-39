# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-J33
# Copyright IBM Corp. 2018
# The source code for this program is not published or other-wise divested of its trade 
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

import unittest

from models.tensorflow import Unknown
from test_base import TestBasePostgres


class TestAIOpenScaleClient(TestBasePostgres):

    model = Unknown()

    def test_01_create_client(self):
        self.create_client()

    def test_02_setup_data_mart(self):
        self.setup_data_mart()

    def test_03_bind_wml_instance(self):
        self.bind_wml_instance()

    def test_04_get_wml_client(self):
        self.get_wml_client()

    def test_05_store_model(self):
        self.prepare_deployment(self.model)

    def test_06_subscribe(self):
        self.subscribe()

    def test_07_select_asset_and_get_details(self):
        self.select_asset_and_get_details()

    def test_08_list_deployments(self):
        self.list_deployments()

    def test_09_setup_payload_logging(self):
        TestAIOpenScaleClient.subscription.payload_logging.enable()
        subscription_details = TestAIOpenScaleClient.subscription.get_details()
        print("Subscription details after performance monitor ON:\n{}".format(subscription_details))

        for configuration in subscription_details['entity']['configurations']:
            if configuration['type'] == 'payload_logging':
                self.assertEqual(configuration['enabled'], True)
            else:
                self.assertEqual(configuration['enabled'], False)

    def test_10_get_payload_logging_details(self):
        self.get_payload_logging_details()

    def test_11_score(self):
        self.score(self.model, 5)

    def test_12_stats_on_payload_logging_table(self):
        self.stats_on_payload_logging_table()

    def test_13_disable_payload_logging(self):
        TestAIOpenScaleClient.subscription.payload_logging.disable()

        subscription_details = TestAIOpenScaleClient.subscription.get_details()
        print("Subscription details after disabling performance monitoring:\n{}".format(subscription_details))

        for configuration in subscription_details['entity']['configurations']:
            self.assertEqual(configuration['enabled'], False)

    def test_14_unsubscribe(self):
        self.unsubscribe()

    def test_15_unbind(self):
        self.unbind()

    def test_16_delete_data_mart(self):
        self.delete_data_mart()


if __name__ == '__main__':
    unittest.main()
