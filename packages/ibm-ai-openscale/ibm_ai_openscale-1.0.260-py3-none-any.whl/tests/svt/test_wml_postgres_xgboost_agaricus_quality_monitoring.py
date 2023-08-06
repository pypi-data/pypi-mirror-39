import unittest
import time

from models.xgboost import XGBoost
from preparation_and_cleaning import *
from ibm_ai_openscale import APIClient
from ibm_ai_openscale.engines import *


@unittest.skip("Rework needed")
class TestAIOpenScaleClient(unittest.TestCase):

    ai_client = None
    deployment_uid = None
    model_uid = None
    subscription_uid = None
    scoring_url = None
    labels = None
    wml_client = None
    subscription = None
    binding_uid = None
    aios_model_uid = None
    scoring_result = None
    payload_scoring = None
    published_model_details = None
    source_uid = None

    test_uid = str(uuid.uuid4())

    @classmethod
    def setUpClass(cls):
        clean_env(database="postgres")

        cls.aios_credentials = get_aios_credentials()
        cls.wml_credentials = get_wml_credentials()
        cls.database_credentials = get_postgres_credentials()
        cls.schema_name = get_schema_name()
        cls.model = XGBoost()

        cls.ai_client = APIClient(cls.aios_credentials)

    @classmethod
    def tearDownClass(cls):
        print("Deleting DataMart.")
        cls.ai_client.data_mart.delete()

    def test_01_setup_data_mart(self):
        self.ai_client.data_mart.setup(db_credentials=self.database_credentials, schema=self.schema_name)

    def test_02_bind_wml(self):
        TestAIOpenScaleClient.binding_uid = self.ai_client.data_mart.bindings.add(
            "My WML instance",
            WatsonMachineLearningInstance(self.wml_credentials))

        print("Binding uid: {}".format(self.binding_uid))
        self.assertIsNotNone(self.binding_uid)

    def test_03_get_binding_id(self):
        print("Bindings list:\n")
        self.ai_client.data_mart.bindings.list()
        binding_uid = self.ai_client.data_mart.bindings.get_uids()[0]
        print("Datamart details binding guid: {}".format(binding_uid))
        self.assertIsNotNone(binding_uid)
        self.assertEqual(binding_uid, self.binding_uid)

    def test_04_get_wml_client(self):
        TestAIOpenScaleClient.wml_client = self.ai_client.data_mart.bindings.get_native_engine_client(self.binding_uid)
        self.assertIsNotNone(self.wml_client)

    def test_05_prepare_deployment(self):
        TestAIOpenScaleClient.published_model_details = self.model.publish_to_wml(self.wml_client)
        print("Published model details: {}".format(self.published_model_details))
        TestAIOpenScaleClient.model_uid = self.wml_client.repository.get_model_uid(self.published_model_details)
        print("Model uid: {}".format(self.model_uid))

        deployment = self.wml_client.deployments.create(
            artifact_uid=self.model_uid,
            name="Test deployment",
            asynchronous=False)
        print("Deployment details: {}".format(deployment))

        TestAIOpenScaleClient.deployment_uid = self.wml_client.deployments.get_uid(deployment)
        print("Deployment uid: {}".format(self.deployment_uid))

    def test_06_subscribe(self):
        TestAIOpenScaleClient.subscription = self.ai_client.data_mart.subscriptions.add(
            WatsonMachineLearningAsset(self.model_uid))
        self.assertIsNotNone(self.subscription)
        TestAIOpenScaleClient.subscription_uid = self.subscription.uid

    def test_07_get_subscription(self):
        TestAIOpenScaleClient.subscription = self.ai_client.data_mart.subscriptions.get(self.subscription_uid)
        self.assertIsNotNone(self.subscription)

        subscription_details = self.subscription.get_details()
        print("Subscription details:\n{}".format(subscription_details))

    def test_08_setup_payload_logging(self):
        self.subscription.payload_logging.enable(dynamic_schema_update=True)

        subscription_details = TestAIOpenScaleClient.subscription.get_details()
        print("Subscription details after payload logging ON:\n{}".format(subscription_details))

        for configuration in subscription_details['entity']['configurations']:
            if configuration['type'] == 'payload_logging':
                self.assertEqual(configuration['enabled'], True)
            else:
                self.assertEqual(configuration['enabled'], False)

    def test_09_get_payload_logging_details(self):
        payload_logging_details = self.subscription.payload_logging.get_details()
        print("Payload logging details:\n{}".format(payload_logging_details))
        self.assertIsNotNone(payload_logging_details)

    def test_10_score(self):
        deployment_details = self.wml_client.deployments.get_details(self.deployment_uid)
        scoring_endpoint = self.wml_client.deployments.get_scoring_url(deployment_details)

        for i in range(0, 10):
            payload_scoring = self.model.get_scoring_payload()
            print("Payload scoring:\n{}".format(payload_scoring))
            TestAIOpenScaleClient.scoring_result = self.wml_client.deployments.score(scoring_endpoint, payload_scoring)
            print("Scoring result: {}".format(self.scoring_result))
            self.assertIsNotNone(self.scoring_result)

        print("Waiting 60 seconds for propagation.")
        time.sleep(60)

    def test_11_stats_on_payload_logging_table(self):
        print("Print table schema:")
        self.subscription.payload_logging.print_table_schema()
        print("Show table:")
        self.subscription.payload_logging.show_table()

        print("Describe table description:")
        table_description = self.subscription.payload_logging.describe_table()
        print("Table description:\n{}".format(table_description))

        table_content = self.subscription.payload_logging.get_table_content()
        print("Table content:\n{}".format(table_content))
        print(type(table_content))

        python_table_content = self.subscription.payload_logging.get_table_content(format='python')
        print("Python Table content:\n{}".format(python_table_content))

        self.assertIsNotNone(python_table_content)

        if self.scoring_result is not None and 'fields' in self.scoring_result.keys():
            if 'prediction' in self.scoring_result['fields']:
                self.assertIn('prediction', python_table_content['fields'])

            if 'probability' in self.scoring_result['fields']:
                self.assertIn('probability', python_table_content['fields'])

        self.assertGreater(table_content.size, 1)

    def test_12_enable_quality_monitoring(self):
        from ibm_ai_openscale.supporting_classes.enums import ProblemType
        self.subscription.quality_monitoring.enable(threshold=0.7, min_records=10, problem_type=ProblemType.BINARY_CLASSIFICATION)
        details = TestAIOpenScaleClient.subscription.quality_monitoring.get_details()
        self.assertIn('True', str(details))

    def test_13_feedback_logging(self):

        records = []

        for i in range(1, 20):
            records.append(self.model.get_feedback_payload()['values'])

        TestAIOpenScaleClient.subscription.feedback_logging.store(feedback_data=records)
        time.sleep(30)

        feedback_pd = TestAIOpenScaleClient.subscription.feedback_logging.get_table_content(format='pandas')
        print(feedback_pd)
        self.assertGreater(len(feedback_pd), 1)

    def test_14_stats_on_feedback_logging(self):
        TestAIOpenScaleClient.subscription.feedback_logging.show_table()
        TestAIOpenScaleClient.subscription.feedback_logging.print_table_schema()
        TestAIOpenScaleClient.subscription.feedback_logging.describe_table()

    def test_15_run_quality_monitoring(self):
        run_details = TestAIOpenScaleClient.subscription.quality_monitoring.run()
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

    def test_16_stats_on_quality_monitoring_table(self):
        TestAIOpenScaleClient.subscription.quality_monitoring.print_table_schema()
        TestAIOpenScaleClient.subscription.quality_monitoring.show_table()
        TestAIOpenScaleClient.subscription.quality_monitoring.show_table(limit=None)
        TestAIOpenScaleClient.subscription.quality_monitoring.describe_table()
        TestAIOpenScaleClient.subscription.quality_monitoring.get_table_content()
        quality_metrics = TestAIOpenScaleClient.subscription.quality_monitoring.get_table_content(format='python')
        self.assertTrue(len(quality_metrics['values']) > 0)

    def test_17_disable_quality_monitoring(self):
        TestAIOpenScaleClient.subscription.payload_logging.disable()

    def test_18_disable_payload_logging(self):
        self.subscription.payload_logging.disable()

    def test_19_unsubscribe(self):
        self.ai_client.data_mart.subscriptions.delete(self.subscription.uid)

    def test_20_unbind(self):
        self.ai_client.data_mart.bindings.delete(self.binding_uid)


if __name__ == '__main__':
    unittest.main()
