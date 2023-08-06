# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-J33
# Copyright IBM Corp. 2018
# The source code for this program is not published or other-wise divested of its trade 
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

import unittest
import time
from models.scikit import Digit
from test_base import TestBasePostgres
from ibm_ai_openscale.engines import *


class TestAIOpenScaleClient(TestBasePostgres):

    model = Digit()

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
        TestAIOpenScaleClient.subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.add(WatsonMachineLearningAsset(TestAIOpenScaleClient.model_uid, label_column='prediction'))
        print("Subscription: {}".format(TestAIOpenScaleClient.subscription))
        self.assertIsNotNone(TestAIOpenScaleClient.subscription)
        TestAIOpenScaleClient.subscription_uid = TestAIOpenScaleClient.subscription.uid

    def test_07_select_asset_and_get_details(self):
        self.select_asset_and_get_details()

    def test_08_list_deployments(self):
        self.list_deployments()

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
        self.score(self.model, 10)

    def test_12_stats_on_payload_logging_table(self):
        self.stats_on_payload_logging_table()

    def test_13_enable_quality_monitoring(self):
        from ibm_ai_openscale.supporting_classes.enums import ProblemType
        TestAIOpenScaleClient.subscription.quality_monitoring.enable(threshold=0.7, min_records=5, problem_type=ProblemType.MULTICLASS_CLASSIFICATION)
        details = TestAIOpenScaleClient.subscription.quality_monitoring.get_details()
        self.assertTrue('True' in str(details))

    def test_14_feedback_logging(self):
        records = []

        for i in range(1, 10):
            records.append([
                 0.0,
                 0.0,
                 5.0,
                 16.0,
                 16.0,
                 3.0,
                 0.0,
                 0.0,
                 0.0,
                 0.0,
                 9.0,
                 16.0,
                 7.0,
                 0.0,
                 0.0,
                 0.0,
                 0.0,
                 0.0,
                 12.0,
                 15.0,
                 2.0,
                 0.0,
                 0.0,
                 0.0,
                 0.0,
                 1.0,
                 15.0,
                 16.0,
                 15.0,
                 4.0,
                 0.0,
                 0.0,
                 0.0,
                 0.0,
                 9.0,
                 13.0,
                 16.0,
                 9.0,
                 0.0,
                 0.0,
                 0.0,
                 0.0,
                 0.0,
                 0.0,
                 14.0,
                 12.0,
                 0.0,
                 0.0,
                 0.0,
                 0.0,
                 5.0,
                 12.0,
                 16.0,
                 8.0,
                 0.0,
                 0.0,
                 0.0,
                 0.0,
                 3.0,
                 15.0,
                 15.0,
                 1.0,
                 0.0,
                 0.0,
                 2
              ])

        TestAIOpenScaleClient.subscription.feedback_logging.store(feedback_data=records)
        time.sleep(15)

        feedback_pd = TestAIOpenScaleClient.subscription.feedback_logging.get_table_content(format='pandas')
        self.assertGreater(len(feedback_pd), 1)

    def test_15_stats_on_feedback_logging(self):
        TestAIOpenScaleClient.subscription.feedback_logging.show_table()
        TestAIOpenScaleClient.subscription.feedback_logging.print_table_schema()
        TestAIOpenScaleClient.subscription.feedback_logging.describe_table()

    def test_16_run_quality_monitoring(self):
        run_details = TestAIOpenScaleClient.subscription.quality_monitoring.run()
        import time
        self.assertTrue('Prerequisite check' in str(run_details))

        status = run_details['status']
        id = run_details['id']
        start_time = time.time()
        elapsed_time = 0

        while status is not 'completed' and elapsed_time < 60:
            time.sleep(10)
            run_details = TestAIOpenScaleClient.subscription.quality_monitoring.get_run_details(run_uid=id)
            status = run_details['status']
            elapsed_time = time.time() - start_time

        self.assertTrue('completed' in status)

    def test_17_stats_on_quality_monitoring_table(self):
        TestAIOpenScaleClient.subscription.quality_monitoring.print_table_schema()
        TestAIOpenScaleClient.subscription.quality_monitoring.show_table()
        TestAIOpenScaleClient.subscription.quality_monitoring.show_table(limit=None)
        TestAIOpenScaleClient.subscription.quality_monitoring.describe_table()
        TestAIOpenScaleClient.subscription.quality_monitoring.get_table_content()
        quality_metrics = TestAIOpenScaleClient.subscription.quality_monitoring.get_table_content(format='python')
        self.assertTrue(len(quality_metrics['values']) > 0)

    def test_18_disable_quality_monitoring(self):
        TestAIOpenScaleClient.subscription.payload_logging.disable()

    def test_19_disable_payload_logging(self):
        TestAIOpenScaleClient.subscription.payload_logging.disable()

        subscription_details = TestAIOpenScaleClient.subscription.get_details()
        print("Subscription details after disabling performance monitoring:\n{}".format(subscription_details))

        for configuration in subscription_details['entity']['configurations']:
            self.assertEqual(configuration['enabled'], False)

    def test_20_get_metrics(self):
        self.get_performance_metrics()

    def test_21_unsubscribe(self):
        self.unsubscribe()

    def test_22_unbind(self):
        self.unbind()

    def test_23_delete_data_mart(self):
        self.delete_data_mart()


if __name__ == '__main__':
    unittest.main()
