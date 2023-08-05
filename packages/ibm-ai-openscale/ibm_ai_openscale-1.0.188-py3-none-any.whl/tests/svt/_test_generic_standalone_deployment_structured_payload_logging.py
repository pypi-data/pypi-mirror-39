import logging
import unittest
import requests
from ibm_ai_openscale import APIClient
from ibm_ai_openscale.engines import *
from preparation_and_cleaning import *


@unittest.skip("Rework on generic needed")
class TestAIOpenScaleClient(unittest.TestCase):
    deployment_uid = None
    model_uid = None
    subscription_uid = None
    binding_uid = None
    scoring_url = None
    labels = None
    logger = logging.getLogger(__name__)
    ai_client = None
    wml_client = None
    subscription = None
    test_uid = str(uuid.uuid4())

    @classmethod
    def setUpClass(self):
        TestAIOpenScaleClient.logger.info("Service Instance: setting up credentials")

        clean_env()

        self.aios_credentials = get_aios_credentials()
        self.postgres_credentials = get_postgres_credentials()

    def test_01_create_client(self):
        TestAIOpenScaleClient.ai_client = APIClient(self.aios_credentials)

    def test_02_setup_data_mart(self):
        TestAIOpenScaleClient.ai_client.data_mart.setup(db_credentials=self.postgres_credentials, schema=get_schema_name())

    def test_03_bind_custom(self):
        TestAIOpenScaleClient.binding_uid = TestAIOpenScaleClient.ai_client.data_mart.bindings.add("Black box engine", GenericMachineLearningInstance())

    def test_04_get_binding_details(self):
        print('Binding details: :' + str(TestAIOpenScaleClient.ai_client.data_mart.bindings.get_details(TestAIOpenScaleClient.binding_uid)))
        TestAIOpenScaleClient.ai_client.data_mart.bindings.list()

    def test_06_subscribe_custom_deployment(self):
        scoring_url = 'http://169.60.4.178:31520/v1/deployments/action/online'
        scoring_header = {'Authorization': 'Bearer xxx', 'Content-type': 'application/json'}
        name = 'action model deployment'

        subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.add(GenericAsset(name=name,
                                                                                                scoring_url=scoring_url,
                                                                                                scoring_headers=scoring_header,
                                                                                                binding_uid=TestAIOpenScaleClient.binding_uid))
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

    def test_10_score_model_and_log_payload(self):
        payload = {'fields': ['ID',
                              'Gender',
                              'Status',
                              'Children',
                              'Age',
                              'Customer_Status',
                              'Car_Owner',
                              'Customer_Service',
                              'Business_Area',
                              'Satisfaction'],
                             'values': [[3785,
                               'Male',
                               'S',
                               1,
                               17,
                               'Inactive',
                               'Yes',
                               'The car should have been brought to us instead of us trying to find it in the lot.',
                               'Product: Information',
                               0]]}


        subscription_details = TestAIOpenScaleClient.subscription.get_details()
        scoring_url = subscription_details['entity']['deployments'][0]['scoring_endpoint']['url']
        scoring_headers = subscription_details['entity']['deployments'][0]['scoring_endpoint']['request_headers']

        r = requests.post(scoring_url, json=payload, headers=scoring_headers)

        print('Response: ' + str(r.json()))
        TestAIOpenScaleClient.subscription.payload_logging.store(request=payload, response=r.json(), response_time=12)

    def test_11_stats_on_payload_logging_table(self):
        TestAIOpenScaleClient.subscription.payload_logging.print_table_schema()
        TestAIOpenScaleClient.subscription.payload_logging.show_table()
        TestAIOpenScaleClient.subscription.payload_logging.describe_table()
        pandas_df = TestAIOpenScaleClient.subscription.payload_logging.get_table_content()
        print(str(pandas_df))
        self.assertTrue(pandas_df.size > 1)

    def test_12_disable_payload_logging(self):
        TestAIOpenScaleClient.subscription.payload_logging.disable()

    def test_13_get_metrics(self):
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics())
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(deployment_uid=TestAIOpenScaleClient.deployment_uid))
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(subscription_uid=TestAIOpenScaleClient.subscription.uid))
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(asset_uid=TestAIOpenScaleClient.subscription.source_uid))
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(metric_type='quality'))

    def test_15_unsubscribe(self):
        TestAIOpenScaleClient.ai_client.data_mart.subscriptions.delete(TestAIOpenScaleClient.subscription.uid)
        wait_until_deleted(TestAIOpenScaleClient.ai_client, subscription_uid=TestAIOpenScaleClient.subscription.uid)

    def test_16_unbind(self):
        TestAIOpenScaleClient.ai_client.data_mart.bindings.delete(TestAIOpenScaleClient.subscription.binding_uid)
        wait_until_deleted(TestAIOpenScaleClient.ai_client, binding_uid=TestAIOpenScaleClient.subscription.binding_uid)

    def test_17_delete_data_mart(self):
        TestAIOpenScaleClient.ai_client.data_mart.delete()
        wait_until_deleted(TestAIOpenScaleClient.ai_client, data_mart=True)
        delete_schema(get_postgres_credentials(), get_schema_name())


if __name__ == '__main__':
    unittest.main()
