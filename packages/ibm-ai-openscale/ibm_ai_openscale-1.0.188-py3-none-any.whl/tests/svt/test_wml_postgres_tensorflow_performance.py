import unittest

from models.tensorflow import Unknown
from test_base import TestBasePostgres


class TestAIOpenScaleClient(TestBasePostgres):

    model = Unknown()

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

    def test_08_select_asset_and_get_details(self):
        self.select_asset_and_get_details()

    def test_10_list_deployments(self):
        self.list_deployments()

    def test_11_setup_performance_monitoring(self):
        TestAIOpenScaleClient.subscription.performance_monitoring.enable()

        subscription_details = TestAIOpenScaleClient.subscription.get_details()
        print("Subscription details after performance monitor ON:\n{}".format(subscription_details))

        for configuration in subscription_details['entity']['configurations']:
            if configuration['type'] == 'performance_monitoring':
                self.assertEqual(configuration['enabled'], True)

    def test_12_get_performance_monitoring_details(self):
        self.get_performance_monitoring_details()

    def test_13_score(self):
        self.score(self.model, 5)

    def test_14_stats_on_performance_monitoring_table(self):
        self.stats_on_performance_monitoring_table()

    def test_15_disable_performance_monitoring(self):
        TestAIOpenScaleClient.subscription.performance_monitoring.disable()

        subscription_details = TestAIOpenScaleClient.subscription.get_details()
        print("Subscription details after disabling performance monitoring:\n{}".format(subscription_details))

        for configuration in subscription_details['entity']['configurations']:
            self.assertEqual(configuration['enabled'], False)

    def test_16_get_metrics(self):
        self.get_metrics()

    def test_17_unsubscribe(self):
        self.unsubscribe()

    def test_18_unbind(self):
        self.unbind()

    def test_19_delete_data_mart(self):
        self.delete_data_mart()


if __name__ == '__main__':
    unittest.main()
