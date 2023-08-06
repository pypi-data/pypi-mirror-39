# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-J33
# Copyright IBM Corp. 2018
# The source code for this program is not published or other-wise divested of its trade 
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

import unittest
import io
from unittest import mock
from models.AbstractModel import AbstractFeedbackModel, AbstractModel
from preparation_and_cleaning import *

from ibm_ai_openscale import APIClient
from ibm_ai_openscale.engines import *


class TestBase(unittest.TestCase):
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

    database_credentials = None
    schema_name = None

    test_uid = str(uuid.uuid4())

    @classmethod
    def setUpClass(cls):
        cls.aios_credentials = get_aios_credentials()
        cls.wml_credentials = get_wml_credentials()

    @classmethod
    def tearDownClass(cls):
        if cls.wml_client is not None:
            print("Cleaning wml:")
            if cls.deployment_uid is not None:
                cls.wml_client.deployments.delete(cls.deployment_uid)
                print("  Deployment {} removed.".format(cls.deployment_uid))
            if cls.model_uid is not None:
                cls.wml_client.repository.delete(cls.model_uid)
                print("  Model {} removed.".format(cls.model_uid))

    # STEPS

    def create_client(self):
        TestBase.ai_client = APIClient(self.aios_credentials)
        self.assertIsNotNone(TestBase.ai_client)

    def setup_data_mart(self):
        TestBase.ai_client.data_mart.setup(db_credentials=self.database_credentials, schema=self.schema_name)

    def get_data_mart_details(self):
        details = TestBase.ai_client.data_mart.get_details()
        print("Datamart details: {}".format(details))
        self.assertTrue(len(json.dumps(details)) > 10)

    def bind_wml_instance(self):
        TestBase.binding_uid = TestBase.ai_client.data_mart.bindings.add("My WML instance", WatsonMachineLearningInstance(self.wml_credentials))
        self.assertIsNotNone(TestBase.binding_uid)

    def get_binding_id(self):
        print("Bindings list:\n")
        TestBase.ai_client.data_mart.bindings.list()
        binding_uid = TestBase.ai_client.data_mart.bindings.get_uids()[0]
        print("Datamart details binding guid: {}".format(binding_uid))
        self.assertIsNotNone(binding_uid)
        self.assertEqual(binding_uid, TestBase.binding_uid)

    def get_binding_details(self):
        binding_details = TestBase.ai_client.data_mart.bindings.get_details()
        print("Binding details: {}".format(binding_details))
        self.assertIsNotNone(binding_details)

    def get_wml_client(self):
        TestBase.binding_uid = TestBase.ai_client.data_mart.bindings.get_uids()[0]
        print("Binding id: {}".format(TestBase.binding_uid))
        TestBase.wml_client = TestBase.ai_client.data_mart.bindings.get_native_engine_client(TestBase.binding_uid)
        self.assertIsNotNone(TestBase.wml_client)

    def list_instances(self):
        TestBase.ai_client.data_mart.bindings.list()

    def publish_model(self, model):
        if isinstance(model, AbstractFeedbackModel):
            published_model_details = model.publish_to_wml(self.wml_client, db2_credentials=self.database_credentials)
        elif isinstance(model, AbstractModel):
            published_model_details = model.publish_to_wml(self.wml_client)
        else:
            print("Model type: {}".format(type(model)))
            self.fail("Model has invalid type.")
        print("Published model details: {}".format(published_model_details))
        self.published_model_details = published_model_details
        TestBase.model_uid = TestBase.wml_client.repository.get_model_uid(published_model_details)

    def deploy_model(self, model_uid=None):
        if model_uid is None:
            model_uid = TestBase.model_uid

        deployment = self.wml_client.deployments.create(artifact_uid=model_uid, name="Test deployment",
                                                        asynchronous=False)
        print("Deployment details: {}".format(deployment))

        TestBase.deployment_uid = self.wml_client.deployments.get_uid(deployment)
        print("Deployment uid: {}".format(TestBase.deployment_uid))

    def prepare_deployment(self, model):
        self.publish_model(model=model)
        self.deploy_model(model_uid=TestBase.model_uid)

    def subscribe(self):
        TestBase.subscription = TestBase.ai_client.data_mart.subscriptions.add(WatsonMachineLearningAsset(TestBase.model_uid))
        print("Subscription: {}".format(TestBase.subscription))
        self.assertIsNotNone(TestBase.subscription)
        TestBase.subscription_uid = TestBase.subscription.uid

    def list_subscription(self):
        TestBase.ai_client.data_mart.subscriptions.list()

    def get_subscription(self):
        TestBase.subscription = TestBase.ai_client.data_mart.subscriptions.get(TestBase.subscription_uid)
        self.assertIsNotNone(TestBase.subscription)

        subscription_details = TestBase.subscription.get_details()
        print("Subscription details:\n{}".format(subscription_details))

    def select_asset_and_get_details(self):
        TestBase.subscription = TestBase.ai_client.data_mart.subscriptions.get(TestBase.subscription_uid)
        self.assertIsNotNone(TestBase.subscription)

    def list_deployments(self):
        print("Listing deployments:\n")
        self.subscription.list_deployments()

    def get_payload_logging_details(self):
        payload_logging_details = self.subscription.payload_logging.get_details()
        print("Payload logging details:\n{}".format(payload_logging_details))
        self.assertIsNotNone(payload_logging_details)

    def score(self, model, scoring_number=5):
        deployment_details = self.wml_client.deployments.get_details(TestBase.deployment_uid)
        scoring_endpoint = self.wml_client.deployments.get_scoring_url(deployment_details)

        payload_scoring = model.get_scoring_payload()
        print("Payload scoring:\n{}".format(payload_scoring))

        scoring_result = None
        for i in range(0, scoring_number):
            scoring_result = self.wml_client.deployments.score(scoring_endpoint, payload_scoring)
            print("Scoring result: {}".format(scoring_result))
            self.assertIsNotNone(scoring_result)

        TestBase.scoring_result = scoring_result
        TestBase.payload_scoring = payload_scoring

        print('Scoring result: ' + str(scoring_result))
        print('Scoring payload: ' + str(payload_scoring))

        import time
        print("Waiting 20 seconds for propagation.")
        time.sleep(20)

    def get_quality_monitoring_details(self):
        quality_monitoring_details = TestBase.subscription.quality_monitoring.get_details()
        self.assertIsNotNone(quality_monitoring_details)
        print("Quality monitoring details:\n{}".format(quality_monitoring_details))

    def get_performance_monitoring_details(self):
        performance_monitoring_details = self.subscription.performance_monitoring.get_details()
        print("Performance monitoring details:\n{}".format(performance_monitoring_details))

        self.assertIsNotNone(performance_monitoring_details)
        self.assertEqual(performance_monitoring_details['enabled'], True)

    def send_feedback_data(self, model):
        feedback_data, fields = model.get_feedback_data()
        TestBase.subscription.feedback_logging.store(feedback_data, fields=fields)

    def run_quality_monitor(self):
        run_details = TestBase.subscription.quality_monitoring.run()
        print("Quality monitoring run details:\n{}".format(run_details))
        import time
        self.assertTrue('Prerequisite check' in str(run_details))

        status = run_details['status']
        id = run_details['id']
        start_time = time.time()
        elapsed_time = 0

        while status is not 'completed' and elapsed_time < 60:
            time.sleep(10)
            run_details = TestBase.subscription.quality_monitoring.get_run_details(run_uid=id)
            status = run_details['status']
            elapsed_time = time.time() - start_time

        print("Latest run details:\n{}".format(run_details))
        self.assertTrue('completed' in status)

        time.sleep(30)

    def stats_on_payload_logging_table(self):
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

        self.assertTrue(table_content.size > 1)
        self.assertIsNotNone(python_table_content)

        if self.scoring_result is not None and 'fields' in self.scoring_result.keys():
            if 'prediction' in self.scoring_result['fields']:
                self.assertIn('prediction', python_table_content['fields'])

            if 'probability' in self.scoring_result['fields']:
                self.assertIn('probability', python_table_content['fields'])

    def stats_on_quality_monitoring_table(self):
        TestBase.subscription.quality_monitoring.print_table_schema()
        TestBase.subscription.quality_monitoring.show_table()
        TestBase.subscription.quality_monitoring.show_table(limit=None)
        TestBase.subscription.quality_monitoring.describe_table()
        TestBase.subscription.quality_monitoring.get_table_content()
        quality_metrics = TestBase.subscription.quality_monitoring.get_table_content(format='python')
        self.assertTrue(len(quality_metrics['values']) > 0)

    def stats_on_performance_monitoring_table(self):
        print("Printing performance table: ")
        self.subscription.performance_monitoring.print_table_schema()
        self.subscription.performance_monitoring.show_table()
        self.subscription.performance_monitoring.describe_table()
        self.subscription.performance_monitoring.get_table_content()
        performance_metrics = self.subscription.performance_monitoring.get_table_content(format='python')
        print("Performance metrics:\n{}".format(performance_metrics))
        self.assertTrue(len(performance_metrics['values']) > 0)

    def stats_on_feedback_logging_table(self):
        TestBase.subscription.feedback_logging.print_table_schema()
        TestBase.subscription.feedback_logging.show_table()
        TestBase.subscription.feedback_logging.describe_table()
        TestBase.subscription.feedback_logging.get_table_content()
        feedback_logging = TestBase.subscription.feedback_logging.get_table_content(format='python')
        self.assertTrue(len(feedback_logging['values']) > 0)
        
    def get_metrics(self):
        deployment_metrics = self.ai_client.data_mart.get_deployment_metrics()
        deployment_metrics_deployment_uid = self.ai_client.data_mart.get_deployment_metrics(
            deployment_uid=self.deployment_uid)
        deployment_metrics_subscription_uid = self.ai_client.data_mart.get_deployment_metrics(
            subscription_uid=self.subscription.uid)
        deployment_metrics_asset_uid = self.ai_client.data_mart.get_deployment_metrics(
            asset_uid=self.subscription.source_uid)

        print(deployment_metrics)
        print(deployment_metrics_deployment_uid)
        print(deployment_metrics_subscription_uid)
        print(deployment_metrics_asset_uid)

        self.assertGreater(len(deployment_metrics['deployment_metrics']), 0)
        self.assertGreater(len(deployment_metrics_deployment_uid['deployment_metrics']), 0)
        self.assertGreater(len(deployment_metrics_subscription_uid['deployment_metrics']), 0)
        self.assertGreater(len(deployment_metrics_asset_uid['deployment_metrics']), 0)

    def get_quality_metrics(self):
        self.get_metrics()
        quality_metrics_asset_uid = TestBase.ai_client.data_mart.get_deployment_metrics(asset_uid=TestBase.subscription.source_uid, metric_type='quality')
        quality_metrics_deployment_uid = TestBase.subscription.quality_monitoring.get_metrics(deployment_uid=TestBase.deployment_uid)

        print(quality_metrics_asset_uid)
        print(quality_metrics_deployment_uid)

        self.assertGreater(len(quality_metrics_asset_uid['deployment_metrics'][0]['metrics']), 0)
        self.assertGreater(len(quality_metrics_deployment_uid['metrics']), 0)

    def get_performance_metrics(self):
        deployment_metrics = self.ai_client.data_mart.get_deployment_metrics()
        deployment_metrics_deployment_uid = self.ai_client.data_mart.get_deployment_metrics(
            deployment_uid=self.deployment_uid)
        deployment_metrics_subscription_uid = self.ai_client.data_mart.get_deployment_metrics(
            subscription_uid=self.subscription.uid)
        deployment_metrics_asset_uid = self.ai_client.data_mart.get_deployment_metrics(
            asset_uid=self.subscription.source_uid)

        print(deployment_metrics)
        print(deployment_metrics_deployment_uid)
        print(deployment_metrics_subscription_uid)
        print(deployment_metrics_asset_uid)

        self.assertGreater(len(deployment_metrics['deployment_metrics']), 0)
        self.assertGreater(len(deployment_metrics_deployment_uid['deployment_metrics']), 0)
        self.assertGreater(len(deployment_metrics_subscription_uid['deployment_metrics']), 0)
        self.assertGreater(len(deployment_metrics_asset_uid['deployment_metrics']), 0)

        performance_metrics_asset_uid = self.ai_client.data_mart.get_deployment_metrics(
            asset_uid=self.subscription.source_uid, metric_type='performance')
        performance_metrics_deployment_uid = self.subscription.performance_monitoring.get_metrics(
            deployment_uid=self.deployment_uid)

        print(performance_metrics_asset_uid)
        print(performance_metrics_deployment_uid)

        self.assertGreater(len(performance_metrics_asset_uid['deployment_metrics'][0]['metrics']), 0)
        self.assertGreater(len(performance_metrics_deployment_uid['metrics']), 0)

    def unsubscribe(self):
        TestBase.ai_client.data_mart.subscriptions.delete(self.subscription.uid)

    def unbind(self):
        TestBase.ai_client.data_mart.bindings.delete(self.binding_uid)

    def delete_data_mart(self):
        TestBase.ai_client.data_mart.delete()

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def assert_stdout(self, method, expected_output, mock_stdout):
        try:
            method()
        except:
            pass
        self.assertRegex(mock_stdout.getvalue(), expected_output)

    def get_std_output(self, function):
        old_output = sys.stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output
        function()
        sys.stdout = old_output
        return captured_output.getvalue().strip()


class TestBasePostgres(TestBase):

    @classmethod
    def setUpClass(cls):
        TestBase.setUpClass()
        clean_env(database="postgres")

        cls.database_credentials = get_postgres_credentials()
        cls.schema_name = get_schema_name()


class TestBaseDB2(TestBase):

    @classmethod
    def setUpClass(cls):
        TestBase.setUpClass()
        clean_env(database="db2")

        cls.database_credentials = get_db2_datamart_credentials()
        cls.schema_name = get_db2_schema_name()


