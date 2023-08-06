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
import boto3
from preparation_and_cleaning import *
from ibm_ai_openscale import APIClient
from ibm_ai_openscale.engines import *
from ibm_ai_openscale.supporting_classes import PayloadRecord


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

    # AWS configuration
    credentials = {
        "access_key_id": "AKIAI3LQITG4RLLSUIHA",
        "secret_access_key": "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",
        "region": "us-east-1"
    }

    def score(self, binding_details, subscription_details):
        access_id = binding_details['entity']['credentials']['access_key_id']
        access_key = binding_details['entity']['credentials']['secret_access_key']
        region = binding_details['entity']['credentials']['region']
        endpoint_name = subscription_details['entity']['deployments'][0]['name']

        runtime = boto3.client('sagemaker-runtime',
                               region_name=region,
                               aws_access_key_id=access_id,
                               aws_secret_access_key=access_key)

        fields = ['radius_mean', 'texture_mean', 'perimeter_mean', 'area_mean', 'smoothness_mean', 'compactness_mean',
                  'concavity_mean', 'concave points_mean', 'symmetry_mean', 'fractal_dimension_mean', 'radius_se',
                  'texture_se', 'perimeter_se', 'area_se', 'smoothness_se', 'compactness_se', 'concavity_se',
                  'concave points_se', 'symmetry_se', 'fractal_dimension_se', 'radius_worst', 'texture_worst',
                  'perimeter_worst', 'area_worst', 'smoothness_worst', 'compactness_worst', 'concavity_worst',
                  'concave points_worst', 'symmetry_worst', 'fractal_dimension_worst']
        payload = "17.02,23.98,112.8,899.3,0.1197,0.1496,0.2417,0.1203,0.2248,0.06382,0.6009,1.398,3.999,67.78,0.008268,0.03082,0.05042,0.01112,0.02102,0.003854,20.88,32.09,136.1,1344,0.1634,0.3559,0.5588,0.1847,0.353,0.08482\n17.02,23.98,112.8,899.3,0.1197,0.1496,0.2417,0.1203,0.2248,0.06382,0.6009,1.398,3.999,67.78,0.008268,0.03082,0.05042,0.01112,0.02102,0.003854,20.88,32.09,136.1,1344,0.1634,0.3559,0.5588,0.1847,0.353,0.08482"

        start_time = time.time()
        response = runtime.invoke_endpoint(EndpointName=endpoint_name,
                                           ContentType='text/csv',
                                           Body=payload)
        response_time = time.time() - start_time
        result = json.loads(response['Body'].read().decode())

        values = []
        for v in payload.split('\n'):
            values.append([float(s) for s in v.split(',')])

        request = {'fields': fields, 'values': values}
        response = {
            'fields': list(result['predictions'][0]),
            'values': [list(x.values()) for x in result['predictions']]
        }

        return request, response, response_time

    @classmethod
    def setUpClass(cls):
        clean_env(database="postgres")

        cls.aios_credentials = get_aios_credentials()
        cls.wml_credentials = get_wml_credentials()
        cls.database_credentials = get_postgres_credentials()
        cls.schema_name = get_schema_name()

        cls.ai_client = APIClient(cls.aios_credentials)

    def test_01_setup_data_mart(self):
        self.ai_client.data_mart.setup(db_credentials=self.database_credentials, schema=self.schema_name)

    def test_02_bind_sagemaker(self):
        TestAIOpenScaleClient.binding_uid = self.ai_client.data_mart.bindings.add("SageMaker ml engine", SageMakerMachineLearningInstance(self.credentials))
        print("Binding uid: {}".format(self.binding_uid))

    def test_03_get_binding_details(self):
        binding_details = self.ai_client.data_mart.bindings.get_details(self.binding_uid)
        print("Binding details: {}".format(binding_details))
        self.ai_client.data_mart.bindings.list()

    def test_04_get_assets(self):
        assets_uids = self.ai_client.data_mart.bindings.get_asset_uids()
        self.assertGreater(len(assets_uids), 1)
        print("Assets uids: {}".format(assets_uids))

        self.ai_client.data_mart.bindings.list_assets()
        asset_details = self.ai_client.data_mart.bindings.get_asset_details()
        print("Assets details: {}".format(asset_details))

        asset_name = ""
        for detail in asset_details:
            if 'DEMO-classification-2' in detail['name']:
                asset_name = detail['name']
                TestAIOpenScaleClient.source_uid = detail['source_uid']

        print("asset name: {}".format(asset_name))
        print("asset uid: {}".format(self.source_uid))
        self.assertIsNotNone(TestAIOpenScaleClient.source_uid)

    def test_05_subscribe_sagemaker_asset(self):
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

    def test_06_get_subscription_details(self):
        TestAIOpenScaleClient.subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.get(TestAIOpenScaleClient.subscription_uid)
        details = TestAIOpenScaleClient.subscription.get_details()
        print('Subscription details: ' + str(details))

        self.assertTrue('s3' in str(details))

    def test_07_list_deployments(self):
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

        request, response, response_time = self.score(binding_details=binding_details, subscription_details=subscription_details)

        records_list = []
        for i in range(0, 15):
            records_list.append(PayloadRecord(request=request, response=response, response_time=int(response_time)))

        TestAIOpenScaleClient.subscription.payload_logging.store(records=records_list)

        time.sleep(30)

    def test_11_stats_on_payload_logging_table(self):
        payload_table_content = TestAIOpenScaleClient.subscription.payload_logging.get_table_content(format='python')
        self.assertTrue('perimeter_mean' in str(payload_table_content))

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

    def test_14_unsubscribe(self):
        self.ai_client.data_mart.subscriptions.delete(self.subscription.uid)

    def test_15_unbind(self):
        self.ai_client.data_mart.bindings.delete(self.binding_uid)

    @classmethod
    def tearDownClass(cls):
        print("Deleting DataMart.")
        cls.ai_client.data_mart.delete()


if __name__ == '__main__':
    unittest.main()
