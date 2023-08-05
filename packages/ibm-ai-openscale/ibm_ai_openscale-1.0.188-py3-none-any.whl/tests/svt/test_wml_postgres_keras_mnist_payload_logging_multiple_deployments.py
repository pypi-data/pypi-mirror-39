import logging
import unittest

from ibm_ai_openscale import APIClient
from ibm_ai_openscale.engines import *
from preparation_and_cleaning import *
from models.Keras import Mnist


class TestAIOpenScaleClient(unittest.TestCase):
    model_uid = None
    deployment_1_uid = None
    deployment_2_uid = None
    deployment_3_uid = None
    scoring_1_url = None
    scoring_2_url = None
    scoring_3_url = None
    subscription_uid = None
    labels = None
    logger = logging.getLogger(__name__)
    ai_client = None
    wml_client = None
    subscription = None
    binding_uid = None
    test_uid = str(uuid.uuid4())

    model = Mnist()

    @classmethod
    def setUpClass(self):
        clean_env()

        self.aios_credentials = get_aios_credentials()
        self.wml_credentials = get_wml_credentials()
        self.postgres_credentials = get_postgres_credentials()

    def test_01_create_client(self):
        TestAIOpenScaleClient.ai_client = APIClient(self.aios_credentials)
        self.assertIsNotNone(TestAIOpenScaleClient.ai_client)

    def test_02_setup_data_mart(self):
        TestAIOpenScaleClient.ai_client.data_mart.setup(db_credentials=self.postgres_credentials, schema=get_schema_name())

    def test_03_bind_wml_instance_and_get_wml_client(self):
        TestAIOpenScaleClient.binding_uid = TestAIOpenScaleClient.ai_client.data_mart.bindings.add("My WML instance", WatsonMachineLearningInstance(self.wml_credentials))
        self.assertIsNotNone(TestAIOpenScaleClient.binding_uid)

    def test_04_get_wml_client(self):
        binding_uid = TestAIOpenScaleClient.ai_client.data_mart.bindings.get_uids()[0]
        TestAIOpenScaleClient.wml_client = TestAIOpenScaleClient.ai_client.data_mart.bindings.get_native_engine_client(binding_uid)

    def test_05_publish_model(self):
        published_model = self.model.publish_to_wml(self.wml_client)
        print("Published model: {}".format(published_model))
        self.assertIsNotNone(published_model)

        TestAIOpenScaleClient.model_uid = self.wml_client.repository.get_model_uid(published_model)
        print("Published model uid: {}".format(TestAIOpenScaleClient.model_uid))

    def test_06a_create_1_deployment(self):
        deployment = self.wml_client.deployments.create(artifact_uid=TestAIOpenScaleClient.model_uid, name="Keras 1 deployment", asynchronous=False)
        print("Deployment: {}".format(deployment))
        self.assertIsNotNone(deployment)

        TestAIOpenScaleClient.deployment_1_uid = self.wml_client.deployments.get_uid(deployment)
        TestAIOpenScaleClient.scoring_1_url = self.wml_client.deployments.get_scoring_url(deployment)
        print("Scoring url: {}".format(TestAIOpenScaleClient.scoring_1_url))
        self.assertTrue('online' in str(TestAIOpenScaleClient.scoring_1_url))

    def test_06b_create_2_deployment(self):
        deployment = self.wml_client.deployments.create(artifact_uid=TestAIOpenScaleClient.model_uid, name="Keras 2 deployment", asynchronous=False)
        print("Deployment: {}".format(deployment))
        self.assertIsNotNone(deployment)

        TestAIOpenScaleClient.deployment_2_uid = self.wml_client.deployments.get_uid(deployment)
        TestAIOpenScaleClient.scoring_2_url = self.wml_client.deployments.get_scoring_url(deployment)
        print("Scoring url: {}".format(TestAIOpenScaleClient.scoring_2_url))
        self.assertTrue('online' in str(TestAIOpenScaleClient.scoring_2_url))

    def test_06c_create_3_deployment(self):
        deployment = self.wml_client.deployments.create(artifact_uid=TestAIOpenScaleClient.model_uid, name="Keras 3 deployment", asynchronous=False)
        print("Deployment: {}".format(deployment))
        self.assertIsNotNone(deployment)

        TestAIOpenScaleClient.deployment_3_uid = self.wml_client.deployments.get_uid(deployment)
        TestAIOpenScaleClient.scoring_3_url = self.wml_client.deployments.get_scoring_url(deployment)
        print("Scoring url: {}".format(TestAIOpenScaleClient.scoring_3_url))
        self.assertTrue('online' in str(TestAIOpenScaleClient.scoring_3_url))

    def test_07_subscribe(self):
        subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.add(
            WatsonMachineLearningAsset(TestAIOpenScaleClient.model_uid))
        TestAIOpenScaleClient.subscription_uid = subscription.uid

    def test_08_select_asset_and_get_details(self):
        TestAIOpenScaleClient.subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.get(
            TestAIOpenScaleClient.subscription_uid)
        print(str(TestAIOpenScaleClient.subscription.get_details()))

    def test_09_list_deployments(self):
        TestAIOpenScaleClient.subscription.list_deployments()

    def test_10_setup_payload_logging(self):
        TestAIOpenScaleClient.subscription.payload_logging.enable()
        print('Subscription details after payload logging ON: ' + str(
            TestAIOpenScaleClient.subscription.get_details()))

    def test_11_get_payload_logging_details(self):
        TestAIOpenScaleClient.subscription.payload_logging.get_details()

    def test_12_score(self):

        for i in range(0, 10):
            scoring_payload = self.model.get_scoring_payload()
            scores = self.wml_client.deployments.score(scoring_url=TestAIOpenScaleClient.scoring_1_url, payload=scoring_payload)
            self.assertIsNotNone(scores)

        for i in range(0, 10):
            scoring_payload = self.model.get_scoring_payload()
            scores = self.wml_client.deployments.score(scoring_url=TestAIOpenScaleClient.scoring_2_url, payload=scoring_payload)
            self.assertIsNotNone(scores)

        for i in range(0, 10):
            scoring_payload = self.model.get_scoring_payload()
            scores = self.wml_client.deployments.score(scoring_url=TestAIOpenScaleClient.scoring_3_url, payload=scoring_payload)
            self.assertIsNotNone(scores)

        import time
        time.sleep(10)

    def test_13_stats_on_payload_logging_table(self):
        TestAIOpenScaleClient.subscription.payload_logging.print_table_schema()
        TestAIOpenScaleClient.subscription.payload_logging.show_table()
        TestAIOpenScaleClient.subscription.payload_logging.describe_table()
        TestAIOpenScaleClient.subscription.payload_logging.get_table_content()
        performance_metrics = TestAIOpenScaleClient.subscription.payload_logging.get_table_content(format='python')
        self.assertTrue(len(performance_metrics['values']) > 0)

    def test_14_setup_performance_monitoring(self):
        TestAIOpenScaleClient.subscription.performance_monitoring.enable()
        print('Subscription details after performance monitor ON: ' + str(
            TestAIOpenScaleClient.subscription.get_details()))

    def test_15_get_performance_monitor_details(self):
        TestAIOpenScaleClient.subscription.performance_monitoring.get_details()

    def test_16_score(self):

        for i in range(0, 10):
            scoring_payload = self.model.get_scoring_payload()
            scores = self.wml_client.deployments.score(scoring_url=TestAIOpenScaleClient.scoring_1_url, payload=scoring_payload)
            self.assertIsNotNone(scores)

        import time
        time.sleep(10)

    def test_17_stats_on_performance_monitoring_table(self):
        TestAIOpenScaleClient.subscription.performance_monitoring.print_table_schema()
        TestAIOpenScaleClient.subscription.performance_monitoring.show_table()
        TestAIOpenScaleClient.subscription.performance_monitoring.describe_table()
        TestAIOpenScaleClient.subscription.performance_monitoring.get_table_content()
        performance_metrics = TestAIOpenScaleClient.subscription.performance_monitoring.get_table_content(format='python')
        self.assertTrue(len(performance_metrics['values']) > 0)

    def test_18_disable_performance_monitoring(self):
        TestAIOpenScaleClient.subscription.performance_monitoring.disable()

    def test_19_get_metrics(self):
        print(TestAIOpenScaleClient.subscription.performance_monitoring.get_metrics(deployment_uid=TestAIOpenScaleClient.deployment_1_uid))

        self.assertTrue(len(TestAIOpenScaleClient.subscription.performance_monitoring.get_metrics(deployment_uid=TestAIOpenScaleClient.deployment_1_uid)['metrics']) > 0)

    def test_20_disable_payload_logging(self):
        TestAIOpenScaleClient.subscription.payload_logging.disable()

    def test_21_unsubscribe(self):
        TestAIOpenScaleClient.ai_client.data_mart.subscriptions.delete(TestAIOpenScaleClient.subscription.uid)
        wait_until_deleted(TestAIOpenScaleClient.ai_client, subscription_uid=TestAIOpenScaleClient.subscription.uid)

    def test_22_clean(self):
        self.wml_client.deployments.delete(TestAIOpenScaleClient.deployment_1_uid)
        self.wml_client.deployments.delete(TestAIOpenScaleClient.deployment_2_uid)
        self.wml_client.deployments.delete(TestAIOpenScaleClient.deployment_3_uid)
        self.wml_client.repository.delete(TestAIOpenScaleClient.model_uid)

    def test_23_unbind(self):
        TestAIOpenScaleClient.ai_client.data_mart.bindings.delete(TestAIOpenScaleClient.subscription.binding_uid)
        wait_until_deleted(TestAIOpenScaleClient.ai_client, binding_uid=TestAIOpenScaleClient.subscription.binding_uid)

    def test_24_delete_data_mart(self):
        TestAIOpenScaleClient.ai_client.data_mart.delete()
        wait_until_deleted(TestAIOpenScaleClient.ai_client, data_mart=True)
        delete_schema(get_postgres_credentials(), get_schema_name())
        delete_schema(get_postgres_credentials(), get_schema_name2())


if __name__ == '__main__':
    unittest.main()