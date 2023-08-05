import unittest
import time
from thirdparty import Sagemaker
from ibm_ai_openscale import APIClient
from ibm_ai_openscale.engines import *
from preparation_and_cleaning import *
from ibm_ai_openscale.supporting_classes import PayloadRecord


class TestAIOpenScaleClient(unittest.TestCase):
    deployment_uid = None
    model_uid = None
    subscription_uid = None
    binding_uid = None
    scoring_url = None
    labels = None
    ai_client = None
    wml_client = None
    subscription = None
    test_uid = str(uuid.uuid4())
    source_uid = None
    transaction_id = None

    engine = Sagemaker()

    @classmethod
    def setUpClass(self):
        clean_env()

        self.aios_credentials = get_aios_credentials()
        self.sagemaker_credentials = get_aws_credentials()
        self.postgres_credentials = get_postgres_credentials()

    def test_01_create_client(self):
        TestAIOpenScaleClient.ai_client = APIClient(self.aios_credentials)

    def test_02_setup_data_mart(self):
        TestAIOpenScaleClient.ai_client.data_mart.setup(db_credentials=self.postgres_credentials, schema=get_schema_name())

    def test_03_bind_sagemaker(self):
        TestAIOpenScaleClient.binding_uid = TestAIOpenScaleClient.ai_client.data_mart.bindings.add("SageMaker ml engine", SageMakerMachineLearningInstance(self.sagemaker_credentials))
        print("Binding uid: {}".format(TestAIOpenScaleClient.binding_uid))

    def test_04_get_binding_details(self):
        binding_details = TestAIOpenScaleClient.ai_client.data_mart.bindings.get_details(TestAIOpenScaleClient.binding_uid)
        print("Binding details: {}".format(binding_details))
        TestAIOpenScaleClient.ai_client.data_mart.bindings.list()

    def test_05_get_assets(self):
        assets_uids = TestAIOpenScaleClient.ai_client.data_mart.bindings.get_asset_uids()
        self.assertGreater(len(assets_uids), 1)
        print("Assets uids: {}".format(assets_uids))

        TestAIOpenScaleClient.ai_client.data_mart.bindings.list_assets()
        asset_details = TestAIOpenScaleClient.ai_client.data_mart.bindings.get_asset_details()
        print("Assets details: {}".format(asset_details))

        asset_name = ""
        for detail in asset_details:
            if 'DEMO-classification-2' in detail['name']:
                asset_name = detail['name']
                TestAIOpenScaleClient.source_uid = detail['source_uid']

        print("asset name: {}".format(asset_name))
        print("asset uid: {}".format(TestAIOpenScaleClient.source_uid))
        self.assertIsNotNone(TestAIOpenScaleClient.source_uid)

    def test_06_subscribe_sagemaker_asset(self):
        from ibm_ai_openscale.supporting_classes.enums import ProblemType, InputDataType

        subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.add(
            SageMakerMachineLearningAsset(
                source_uid=TestAIOpenScaleClient.source_uid,
                binding_uid=TestAIOpenScaleClient.binding_uid,
                input_data_type=InputDataType.STRUCTURED,
                problem_type=ProblemType.BINARY_CLASSIFICATION,
                prediction_column='predicted_label',
                label_column='diagnosis'))

        TestAIOpenScaleClient.subscription_uid = subscription.uid
        print("Subscription uid: ".format(TestAIOpenScaleClient.subscription_uid))

    def test_07_get_subscription_details(self):
        TestAIOpenScaleClient.subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.get(TestAIOpenScaleClient.subscription_uid)
        details = TestAIOpenScaleClient.subscription.get_details()
        print('Subscription details: ' + str(details))

        self.assertTrue('s3' in str(details))

    def test_07b_list_deployments(self):
        TestAIOpenScaleClient.subscription.list_deployments()
        deployment_uids = TestAIOpenScaleClient.subscription.get_deployment_uids()
        self.assertGreater(len(deployment_uids), 0)

    def test_08_setup_payload_logging(self):
        TestAIOpenScaleClient.subscription.payload_logging.enable()

    def test_09_get_payload_logging_details(self):
        payload_logging_details = TestAIOpenScaleClient.subscription.payload_logging.get_details()
        print('Payload logging details: ' + str(payload_logging_details))

    def test_10_score_model_and_log_payload(self):
        binding_details = TestAIOpenScaleClient.ai_client.data_mart.bindings.get_details(TestAIOpenScaleClient.binding_uid)
        subscription_details = TestAIOpenScaleClient.subscription.get_details()

        request, response, response_time = self.engine.score(binding_details=binding_details, subscription_details=subscription_details)

        records_list = [PayloadRecord(request=request, response=response, response_time=int(response_time)),
                        PayloadRecord(request=request, response=response, response_time=int(response_time))]

        TestAIOpenScaleClient.subscription.payload_logging.store(records=records_list)

        time.sleep(30)

        payload_table_content = TestAIOpenScaleClient.subscription.payload_logging.get_table_content(format='python')
        self.assertTrue('perimeter_mean' in str(payload_table_content))

    def test_11_stats_on_payload_logging_table(self):
        TestAIOpenScaleClient.subscription.payload_logging.print_table_schema()
        TestAIOpenScaleClient.subscription.payload_logging.show_table()
        TestAIOpenScaleClient.subscription.payload_logging.describe_table()
        pandas_df = TestAIOpenScaleClient.subscription.payload_logging.get_table_content()
        print(str(pandas_df))
        self.assertTrue(pandas_df.size > 1)

    def test_12_setup_quality_monitoring(self):
        from ibm_ai_openscale.supporting_classes.enums import ProblemType

        TestAIOpenScaleClient.subscription.quality_monitoring.enable(problem_type=ProblemType.BINARY_CLASSIFICATION, threshold=0.8, min_records=5)

    def test_13_get_quality_monitoring_details(self):
        print(str(TestAIOpenScaleClient.subscription.quality_monitoring.get_details()))
        TestAIOpenScaleClient.subscription.quality_monitoring.get_details()

    def test_14_send_feedback_data(self):

        feedback_records = []

        for i in range(1, 10):
            feedback_records.append(
                [17.02,23.98,112.8,899.3,0.1197,0.1496,0.2417,0.1203,0.2248,0.06382,0.6009,1.398,3.999,67.78,0.008268,0.03082,0.05042,0.01112,0.02102,0.003854,20.88,32.09,136.1,1344,0.1634,0.3559,0.5588,0.1847,0.353,0.08482, 1])

        TestAIOpenScaleClient.subscription.feedback_logging.store(feedback_data=feedback_records)

    def test_15_run_quality_monitor(self):
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

    def test_16_stats_on_quality_monitoring_table(self):
        TestAIOpenScaleClient.subscription.quality_monitoring.print_table_schema()
        TestAIOpenScaleClient.subscription.quality_monitoring.show_table()
        TestAIOpenScaleClient.subscription.quality_monitoring.show_table(limit=None)
        TestAIOpenScaleClient.subscription.quality_monitoring.describe_table()
        TestAIOpenScaleClient.subscription.quality_monitoring.get_table_content()
        quality_metrics = TestAIOpenScaleClient.subscription.quality_monitoring.get_table_content(format='python')
        self.assertTrue(len(quality_metrics['values']) > 0)

    def test_17_stats_on_feedback_logging_table(self):
        TestAIOpenScaleClient.subscription.feedback_logging.print_table_schema()
        TestAIOpenScaleClient.subscription.feedback_logging.show_table()
        TestAIOpenScaleClient.subscription.feedback_logging.describe_table()
        TestAIOpenScaleClient.subscription.feedback_logging.get_table_content()
        feedback_logging = TestAIOpenScaleClient.subscription.feedback_logging.get_table_content(format='python')
        self.assertTrue(len(feedback_logging['values']) > 0)

    def test_18_get_details(self):
        details = TestAIOpenScaleClient.subscription.explainability.get_details()
        print("Explainability details: {}".format(details))

    def test_19_disable_quality_monitoring(self):
        TestAIOpenScaleClient.subscription.quality_monitoring.disable()

    def test_20_disable_payload_logging(self):
        TestAIOpenScaleClient.subscription.payload_logging.disable()

    def test_21_get_metrics(self):
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics())
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(deployment_uid=TestAIOpenScaleClient.deployment_uid))
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(subscription_uid=TestAIOpenScaleClient.subscription.uid))
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(asset_uid=TestAIOpenScaleClient.subscription.source_uid))
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(metric_type='quality'))

    def test_22_unsubscribe(self):
        TestAIOpenScaleClient.ai_client.data_mart.subscriptions.delete(TestAIOpenScaleClient.subscription.uid)

    def test_23_unbind(self):
        TestAIOpenScaleClient.ai_client.data_mart.bindings.delete(TestAIOpenScaleClient.binding_uid)

    def test_24_delete_data_mart(self):
        TestAIOpenScaleClient.ai_client.data_mart.delete()
        delete_schema(get_postgres_credentials(), get_schema_name())


if __name__ == '__main__':
    unittest.main()
