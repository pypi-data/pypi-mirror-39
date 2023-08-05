import unittest
from ibm_ai_openscale.supporting_classes.enums import ProblemType
from models.spark import BestHeartDrugFeedback
from test_base import TestBaseDB2


class TestAIOpenScaleClient(TestBaseDB2):

    model = BestHeartDrugFeedback()

    def test_01_create_client(self):
        self.create_client()

    def test_02_setup_data_mart(self):
        self.setup_data_mart()

    def test_03_bind_wml_instance(self):
        self.bind_wml_instance()

    def test_04_get_wml_client(self):
        self.get_wml_client()

    def test_05_prepare_model(self):
        self.prepare_deployment(self.model)

    def test_06_subscribe(self):
        self.subscribe()

    def test_07_select_asset_and_get_details(self):
        self.select_asset_and_get_details()

    def test_08_list_deployments(self):
        self.list_deployments()

    def test_09_setup_quality_monitoring(self):
        TestAIOpenScaleClient.subscription.quality_monitoring.enable(problem_type=ProblemType.MULTICLASS_CLASSIFICATION, threshold=0.8, min_records=5)

    def test_10_get_quality_monitoring_details(self):
        self.get_quality_monitoring_details()

    def test_11_send_feedback_data(self):
        self.send_feedback_data(self.model)

    def test_12_run_quality_monitor(self):
        self.run_quality_monitor()

    def test_13a_stats_on_feedback_table_from_db2(self):
        self.stats_on_feedback_table_from_db2(self.model)

    def test_13b_stats_on_quality_monitoring_table(self):
        self.stats_on_quality_monitoring_table()

    def test_13c_stats_on_feedback_logging_table(self):
        self.stats_on_feedback_logging_table()

    def test_14_disable_quality_monitoring(self):
        TestAIOpenScaleClient.subscription.quality_monitoring.disable()

    def test_15_get_metrics(self):
        self.get_metrics()

    def test_16_unsubscribe(self):
        self.unsubscribe()

    def test_17_unbind(self):
        self.unbind()

    def test_18_delete_data_mart(self):
        self.delete_data_mart()


if __name__ == '__main__':
    unittest.main()
