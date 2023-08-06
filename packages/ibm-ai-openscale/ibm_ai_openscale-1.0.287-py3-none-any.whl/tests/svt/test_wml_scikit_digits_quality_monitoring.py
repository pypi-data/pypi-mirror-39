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
from preparation_and_cleaning import *
from ibm_ai_openscale import APIClient, APIClient4ICP
from ibm_ai_openscale.engines import *


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

    model = Digit()

    @classmethod
    def setUpClass(cls):
        cls.schema = get_schema_name()
        cls.aios_credentials = get_aios_credentials()
        cls.database_credentials = get_database_credentials()

        if "ICP" in get_env():
            cls.ai_client = APIClient4ICP(cls.aios_credentials)
        else:
            cls.ai_client = APIClient(cls.aios_credentials)
            cls.wml_credentials = get_wml_credentials()

        prepare_env(cls.ai_client)

    def test_01_setup_data_mart(self):
        TestAIOpenScaleClient.ai_client.data_mart.setup(db_credentials=self.database_credentials, schema=self.schema)

    def test_02_data_mart_get_details(self):
        details = TestAIOpenScaleClient.ai_client.data_mart.get_details()
        print(details)
        self.assertTrue(len(json.dumps(details)) > 10)

    def test_03_bind_wml_instance(self):
        if "ICP" in get_env():
            TestAIOpenScaleClient.binding_uid = self.ai_client.data_mart.bindings.add("WML instance on ICP", WatsonMachineLearningInstance4ICP())
        else:
            TestAIOpenScaleClient.binding_uid = self.ai_client.data_mart.bindings.add("WML instance on Cloud", WatsonMachineLearningInstance(self.wml_credentials))

    def test_04_get_wml_client(self):
        binding_uid = TestAIOpenScaleClient.ai_client.data_mart.bindings.get_uids()[0]
        TestAIOpenScaleClient.wml_client = TestAIOpenScaleClient.ai_client.data_mart.bindings.get_native_engine_client(binding_uid)

    def test_05_prepare_deployment(self):
        model_name = "AIOS Spark Digits model"
        deployment_name = "AIOS Spark Digits deployment"

        wml_models = self.wml_client.repository.get_details()

        for model in wml_models['models']['resources']:
            if model_name == model['entity']['name']:
                TestAIOpenScaleClient.model_uid = model['metadata']['guid']
                break

        if self.model_uid is None:
            print("Storing model ...")

            published_model_details = self.model.publish_to_wml(self.wml_client)
            TestAIOpenScaleClient.model_uid = self.wml_client.repository.get_model_uid(published_model_details)

        wml_deployments = self.wml_client.deployments.get_details()

        for deployment in wml_deployments['resources']:
            if deployment_name == deployment['entity']['name']:
                TestAIOpenScaleClient.deployment_uid = deployment['metadata']['guid']
                break

        if self.deployment_uid is None:
            print("Deploying model...")

            deployment = self.wml_client.deployments.create(artifact_uid=self.model_uid, name=deployment_name,
                                                            asynchronous=False)
            TestAIOpenScaleClient.deployment_uid = self.wml_client.deployments.get_uid(deployment)

        print("Model id: {}".format(self.model_uid))
        print("Deployment id: {}".format(self.deployment_uid))

    def test_06_subscribe(self):
        TestAIOpenScaleClient.subscription = self.ai_client.data_mart.subscriptions.add(
            WatsonMachineLearningAsset(self.model_uid, prediction_column='prediction'))
        self.assertIsNotNone(self.subscription)
        TestAIOpenScaleClient.subscription_uid = self.subscription.uid

    def test_07_select_asset_and_get_details(self):
        TestAIOpenScaleClient.subscription = self.ai_client.data_mart.subscriptions.get(self.subscription_uid)
        self.assertIsNotNone(self.subscription)

    def test_08_list_deployments(self):
        print("Listing deployments:\n")
        self.subscription.list_deployments()

    def test_09_setup_payload_logging(self):
        self.subscription.payload_logging.enable(dynamic_schema_update=True)
        subscription_details = TestAIOpenScaleClient.subscription.get_details()
        print("Subscription details after payload logging ON:\n{}".format(subscription_details))

        for configuration in subscription_details['entity']['configurations']:
            if configuration['type'] == 'payload_logging':
                self.assertEqual(configuration['enabled'], True)

    def test_10_get_payload_logging_details(self):
        payload_logging_details = self.subscription.payload_logging.get_details()
        print("Payload logging details:\n{}".format(payload_logging_details))
        self.assertIsNotNone(payload_logging_details)

    def test_11_score(self):
        deployment_details = self.wml_client.deployments.get_details(self.deployment_uid)
        scoring_endpoint = self.wml_client.deployments.get_scoring_url(deployment_details)

        payload_scoring = self.model.get_scoring_payload()
        print("Payload scoring:\n{}".format(payload_scoring))

        for i in range(0, 15):
            TestAIOpenScaleClient.scoring_result = self.wml_client.deployments.score(scoring_endpoint, payload_scoring)
            print("Scoring result: {}".format(self.scoring_result))
            self.assertIsNotNone(self.scoring_result)

        print("Waiting 30 seconds for propagation.")
        time.sleep(30)

    def test_12_stats_on_payload_logging_table(self):
        print("Print table schema:")
        self.subscription.payload_logging.print_table_schema()
        print("Show table:")
        self.subscription.payload_logging.show_table()

        print("Describe table description:")
        table_description = self.subscription.payload_logging.describe_table()
        print("Table description:\n{}".format(table_description))

        table_content = self.subscription.payload_logging.get_table_content()
        print("Table content:\n{}".format(table_content))

        python_table_content = self.subscription.payload_logging.get_table_content(format='python')
        print("Python Table content:\n{}".format(python_table_content))

        self.assertGreater(table_content.size, 1)
        self.assertIsNotNone(python_table_content)

        if self.scoring_result is not None and 'fields' in self.scoring_result.keys():
            if 'prediction' in self.scoring_result['fields']:
                self.assertIn('prediction', python_table_content['fields'])

            if 'probability' in self.scoring_result['fields']:
                self.assertIn('probability', python_table_content['fields'])

    def test_13_enable_quality_monitoring(self):
        from ibm_ai_openscale.supporting_classes.enums import ProblemType
        TestAIOpenScaleClient.subscription.quality_monitoring.enable(threshold=0.7, min_records=5, problem_type=ProblemType.MULTICLASS_CLASSIFICATION)
        details = TestAIOpenScaleClient.subscription.quality_monitoring.get_details()
        self.assertTrue('True' in str(details))

    def test_14_feedback_logging(self):
        records = []

        for i in range(0, 10):
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
        time.sleep(30)

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

        while status != 'completed' and elapsed_time < 60:
            time.sleep(10)
            run_details = TestAIOpenScaleClient.subscription.quality_monitoring.get_run_details(run_uid=id)
            status = run_details['status']
            elapsed_time = time.time() - start_time
            print("Run details: {}".format(run_details))
            self.assertNotIn('failed', status)

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

    def test_20_unsubscribe(self):
        self.ai_client.data_mart.subscriptions.delete(self.subscription.uid)

    def test_21_unbind(self):
        self.ai_client.data_mart.bindings.delete(self.binding_uid)

    @classmethod
    def tearDownClass(cls):
        print("Deleting DataMart.")
        cls.ai_client.data_mart.delete()


if __name__ == '__main__':
    unittest.main()
