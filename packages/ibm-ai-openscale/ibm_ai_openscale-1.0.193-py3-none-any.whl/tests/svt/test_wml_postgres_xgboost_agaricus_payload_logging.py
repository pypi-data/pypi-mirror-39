import unittest

from models.xgboost import XGBoost
from test_base import TestBasePostgres


class TestAIOpenScaleClient(TestBasePostgres):

    model = XGBoost()

    def test_01_create_client(self):
        self.create_client()

    def test_02_setup_data_mart(self):
        self.setup_data_mart()

    def test_03_bind_wml(self):
        self.bind_wml_instance()

    def test_04_get_binding_id(self):
        self.get_binding_id()

    def test_05_get_wml_client(self):
        self.get_wml_client()

    def test_06_prepare_deployment(self):
        self.prepare_deployment(self.model)

    def test_07_subscribe(self):
        self.subscribe()

    def test_08_get_subscription(self):
        self.get_subscription()

    def test_09_setup_payload_logging(self):
        TestAIOpenScaleClient.subscription.payload_logging.enable()

        subscription_details = TestAIOpenScaleClient.subscription.get_details()
        print("Subscription details after payload logging ON:\n{}".format(subscription_details))

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

    def test_14_unsubscribe(self):
        self.unsubscribe()

    def test_15_unbind(self):
        self.unbind()

    def test_16_delete_data_mart(self):
        self.delete_data_mart()


if __name__ == '__main__':
    unittest.main()
