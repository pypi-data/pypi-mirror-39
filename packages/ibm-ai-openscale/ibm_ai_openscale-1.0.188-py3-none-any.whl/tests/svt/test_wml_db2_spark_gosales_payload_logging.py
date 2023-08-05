import unittest

from test_base import TestBaseDB2
from models.spark import GoSales


class TestAIOpenScaleClient(TestBaseDB2):

    model = GoSales()

    def test_01_create_client(self):
        self.create_client()

    def test_02_setup_data_mart(self):
        self.setup_data_mart()

    def test_03_bind_wml_instance(self):
        self.bind_wml_instance()

    def test_04_get_wml_client(self):
        self.get_wml_client()

    def test_05_prepare_deployment(self):
        self.prepare_deployment(self.model)

    def test_06_subscribe(self):
        self.subscribe()

    def test_07_select_asset_and_get_details(self):
        self.select_asset_and_get_details()

    def test_07b_list_deployments(self):
        self.list_deployments()

    def test_08_setup_payload_logging(self):
        TestAIOpenScaleClient.subscription.payload_logging.enable()

    def test_09_get_payload_logging_details(self):
        self.get_payload_logging_details()

    def test_10_score(self):
        self.score(self.model, 5)

    def test_11a_stats_on_payload_table_from_db2(self):
        self.stats_on_payload_table_from_db2(self.model, 5)

    def test_11_stats_on_payload_logging_table(self):
        self.stats_on_payload_logging_table()

    def test_12_disable_payload_logging(self):
        TestAIOpenScaleClient.subscription.payload_logging.disable()

    def test_13_get_metrics(self):
        self.get_metrics()

    def test_14_unsubscribe(self):
        self.unsubscribe()

    def test_15_unbind(self):
        self.unbind()

    def test_16_delete_data_mart(self):
        self.delete_data_mart()


if __name__ == '__main__':
    unittest.main()
