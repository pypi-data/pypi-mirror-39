import unittest

from ibm_ai_openscale import APIClient
from ibm_ai_openscale.engines import *
from preparation_and_cleaning import *
from thirdparty import Sagemaker
from ibm_ai_openscale.supporting_classes import PayloadRecord


class TestAIOpenScaleClient(unittest.TestCase):
    deployment_uid = None
    model_uid = None
    aios_model_uid = None
    scoring_url = None
    labels = None
    ai_client = None
    wml_client = None
    subscription = None
    source_uid = None
    binding_uid = None
    subscription_uid = None
    test_uid = str(uuid.uuid4())
    sagemaker = Sagemaker()

    @classmethod
    def setUpClass(self):

        clean_env()

        self.aios_credentials = get_aios_credentials()
        self.db2_credentials = get_db2_datamart_credentials()
        self.schema_name = get_db2_schema_name()
        self.sagemaker_credentials = get_aws_credentials()

        clean_db2_schema(self.db2_credentials, self.schema_name)

    def test_01_create_client(self):
        TestAIOpenScaleClient.ai_client = APIClient(self.aios_credentials)

    def test_02_setup_data_mart(self):
        TestAIOpenScaleClient.ai_client.data_mart.setup(db_credentials=self.db2_credentials, schema=self.schema_name)

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
        subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.add(SageMakerMachineLearningAsset(source_uid=TestAIOpenScaleClient.source_uid, binding_uid=TestAIOpenScaleClient.binding_uid))
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

        request, response, response_time = self.sagemaker.score(binding_details=binding_details, subscription_details=subscription_details)

        records_list = [PayloadRecord(request=request, response=response, response_time=int(response_time)),
                        PayloadRecord(request=request, response=response, response_time=int(response_time))]

        TestAIOpenScaleClient.subscription.payload_logging.store(records=records_list)

    def test_11a_stats_on_payload_table_from_db2(self):
        tables = list_db2_tables(self.db2_credentials, self.schema_name)
        payload_table = None
        for table in tables:
            if "Payload" in table:
                payload_table = table

        self.assertIsNotNone(payload_table)
        print("Payload table: {}".format(payload_table))
        table_content = execute_sql_query(""" SELECT * FROM "{}" """.format(payload_table), db2_credentials=self.db2_credentials)
        print(table_content)

        self.assertEqual(4, len(table_content))

    def test_11b_stats_on_payload_logging_table(self):
        TestAIOpenScaleClient.subscription.payload_logging.print_table_schema()
        TestAIOpenScaleClient.subscription.payload_logging.show_table()
        TestAIOpenScaleClient.subscription.payload_logging.describe_table()
        TestAIOpenScaleClient.subscription.payload_logging.get_table_content()
        performance_metrics = TestAIOpenScaleClient.subscription.payload_logging.get_table_content(format='python')
        self.assertTrue(len(performance_metrics['values']) > 0)

    def test_12_disable_payload_logging(self):
        TestAIOpenScaleClient.subscription.payload_logging.disable()

    def test_13_unsubscribe(self):
        TestAIOpenScaleClient.ai_client.data_mart.subscriptions.delete(TestAIOpenScaleClient.subscription.uid)

    def test_14_unbind(self):
        TestAIOpenScaleClient.ai_client.data_mart.bindings.delete(TestAIOpenScaleClient.subscription.binding_uid)

    def test_15_delete_data_mart(self):
        TestAIOpenScaleClient.ai_client.data_mart.delete()


if __name__ == '__main__':
    unittest.main()
