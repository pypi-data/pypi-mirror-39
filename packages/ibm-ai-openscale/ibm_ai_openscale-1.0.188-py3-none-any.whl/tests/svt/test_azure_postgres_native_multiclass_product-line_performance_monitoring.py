import unittest
import time
from ibm_ai_openscale.supporting_classes import PayloadRecord
from thirdparty import Azure
from ibm_ai_openscale import APIClient
from ibm_ai_openscale.engines import *
from preparation_and_cleaning import *
from ibm_ai_openscale.supporting_classes.enums import InputDataType, ProblemType


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

    engine = Azure()

    @classmethod
    def setUpClass(self):
        clean_env()

        self.aios_credentials = get_aios_credentials()
        self.azure_credentials = get_azure_credentials()

        self.postgres_credentials = get_postgres_credentials()

    def test_01_create_client(self):
        TestAIOpenScaleClient.ai_client = APIClient(self.aios_credentials)

    def test_02_setup_data_mart(self):
        TestAIOpenScaleClient.ai_client.data_mart.setup(db_credentials=self.postgres_credentials, schema=get_schema_name())

    def test_03_bind_azure(self):
        TestAIOpenScaleClient.binding_uid = TestAIOpenScaleClient.ai_client.data_mart.bindings.add("Azure ml engine", AzureMachineLearningInstance(self.azure_credentials))

    def test_04_get_binding_details(self):
        print('Binding details: :' + str(TestAIOpenScaleClient.ai_client.data_mart.bindings.get_details(TestAIOpenScaleClient.binding_uid)))
        TestAIOpenScaleClient.ai_client.data_mart.bindings.list()

    def test_05_get_assets(self):
        assets_uids = TestAIOpenScaleClient.ai_client.data_mart.bindings.get_asset_uids()
        self.assertGreater(len(assets_uids), 1)
        print('Assets uids: ' + str(assets_uids))

        TestAIOpenScaleClient.ai_client.data_mart.bindings.list_assets()
        asset_details = TestAIOpenScaleClient.ai_client.data_mart.bindings.get_asset_details()
        print('Assets details: ' + str(asset_details))

        for detail in asset_details:
            if 'ProductLineClass.2018.11.2.11.40.22.845' in detail['name']:
                TestAIOpenScaleClient.source_uid = detail['source_uid']

        self.assertIsNotNone(TestAIOpenScaleClient.source_uid)

    def test_06_subscribe_azure_asset(self):
        subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.add(
            AzureMachineLearningAsset(source_uid=TestAIOpenScaleClient.source_uid,
                                      binding_uid=TestAIOpenScaleClient.binding_uid,
                                      input_data_type=InputDataType.STRUCTURED,
                                      problem_type=ProblemType.MULTICLASS_CLASSIFICATION,
                                      label_column='PRODUCT_LINE',
                                      prediction_column='Scored Labels'))

        TestAIOpenScaleClient.subscription_uid = subscription.uid
        print('Subscription details: ' + str(subscription.get_details()))

    def test_07_select_asset_and_get_details(self):
        TestAIOpenScaleClient.subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.get(TestAIOpenScaleClient.subscription_uid)
        print('Subscription details: ' + str(TestAIOpenScaleClient.subscription.get_details()))

    def test_07b_list_deployments(self):
        TestAIOpenScaleClient.subscription.list_deployments()

    def test_08_setup_payload_logging(self):
        TestAIOpenScaleClient.subscription.payload_logging.enable()

    def test_09_get_payload_logging_details(self):
        payload_logging_details = TestAIOpenScaleClient.subscription.payload_logging.get_details()
        print('Payload logging details: ' + str(payload_logging_details))

    def test_10_setup_performance_monitoring(self):
        TestAIOpenScaleClient.subscription.performance_monitoring.enable()
        subscription_details = TestAIOpenScaleClient.subscription.get_details()
        print("Subscription details after performance monitor ON:\n{}".format(subscription_details))

        for configuration in subscription_details['entity']['configurations']:
            if configuration['type'] == 'performance_monitoring':
                self.assertEqual(configuration['enabled'], True)

    def test_11_get_performance_monitoring_details(self):
        performance_monitoring_details = TestAIOpenScaleClient.subscription.performance_monitoring.get_details()
        print("Details: {}".format(performance_monitoring_details))

    def test_12_score_model_and_log_payload(self):
        subscription_details = TestAIOpenScaleClient.subscription.get_details()

        request, response, response_time = self.engine.score_product_line(None, subscription_details)

        records_list = [PayloadRecord(request=request, response=response, response_time=int(17)),
                        PayloadRecord(request=request, response=response, response_time=int(21)),
                        PayloadRecord(request=request, response=response, response_time=int(33)),
                        PayloadRecord(request=request, response=response, response_time=int(11)),
                        PayloadRecord(request=request, response=response, response_time=int(15))]

        TestAIOpenScaleClient.subscription.payload_logging.store(records=records_list)

        time.sleep(60)

        payload_table_content = TestAIOpenScaleClient.subscription.payload_logging.get_table_content(format='python')

        print('XXX' + str(payload_table_content))
        self.assertTrue('Scored Probabilities' in str(payload_table_content))

    def test_13_stats_on_payload_logging_table(self):
        TestAIOpenScaleClient.subscription.payload_logging.print_table_schema()
        TestAIOpenScaleClient.subscription.payload_logging.show_table()
        TestAIOpenScaleClient.subscription.payload_logging.describe_table()
        pandas_df = TestAIOpenScaleClient.subscription.payload_logging.get_table_content()
        print(str(pandas_df))
        self.assertTrue(pandas_df.size > 1)

    def test_14_stats_on_performance_monitoring_table(self):
        TestAIOpenScaleClient.subscription.performance_monitoring.print_table_schema()
        TestAIOpenScaleClient.subscription.performance_monitoring.show_table()
        TestAIOpenScaleClient.subscription.performance_monitoring.describe_table()
        TestAIOpenScaleClient.subscription.performance_monitoring.get_table_content()
        performance_metrics = TestAIOpenScaleClient.subscription.performance_monitoring.get_table_content(
            format='python')
        self.assertTrue(len(performance_metrics['values']) > 0)

    def test_15_disable_performance_monitoring(self):
        TestAIOpenScaleClient.subscription.performance_monitoring.disable()
        subscription_details = TestAIOpenScaleClient.subscription.get_details()
        print("Subscription details after disabling performance monitoring:\n{}".format(subscription_details))

    def test_16_disable_payload_logging(self):
        TestAIOpenScaleClient.subscription.payload_logging.disable()

    def test_17_get_metrics(self):
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics())
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(deployment_uid=TestAIOpenScaleClient.deployment_uid))
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(subscription_uid=TestAIOpenScaleClient.subscription.uid))
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(asset_uid=TestAIOpenScaleClient.subscription.source_uid))
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(metric_type='quality'))

    def test_18_unsubscribe(self):
        TestAIOpenScaleClient.ai_client.data_mart.subscriptions.delete(TestAIOpenScaleClient.subscription.uid)

    def test_19_unbind(self):
        TestAIOpenScaleClient.ai_client.data_mart.bindings.delete(TestAIOpenScaleClient.binding_uid)

    def test_20_delete_data_mart(self):
        TestAIOpenScaleClient.ai_client.data_mart.delete()
        delete_schema(get_postgres_credentials(), get_schema_name())


if __name__ == '__main__':
    unittest.main()
