# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-J33
# Copyright IBM Corp. 2018
# The source code for this program is not published or other-wise divested of its trade 
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

import unittest

from ibm_ai_openscale import APIClient
from ibm_ai_openscale.engines import *
from ibm_ai_openscale.supporting_classes import *
from models_preparation import *
from preparation_and_cleaning import *
from datasets_classes import GoSalesDataset


class TestAIOpenScaleClient(unittest.TestCase):
    deployment_uid = None
    model_uid = None
    aios_model_uid = None
    scoring_url = None
    labels = None
    logger = logging.getLogger(__name__)
    ai_client = None
    wml_client = None
    subscription = None
    test_uid = str(uuid.uuid4())
    transaction_id = None

    @classmethod
    def setUpClass(self):

        clean_env()

        self.cos_resource = get_cos_resource()
        self.bucket_names = prepare_cos(self.cos_resource)
        GoSalesDataset.upload_to_cos(self.cos_resource, self.bucket_names['data'])

        self.aios_credentials = get_aios_credentials()
        self.wml_credentials = get_wml_credentials()
        self.postgres_credentials = get_postgres_credentials()

    def test_01_create_client(self):
        TestAIOpenScaleClient.ai_client = APIClient(self.aios_credentials)

    def test_02_setup_data_mart(self):
        TestAIOpenScaleClient.ai_client.data_mart.setup(db_credentials=self.postgres_credentials, schema=get_schema_name())

    def test_03_bind_wml_instance_and_get_wml_client(self):
        TestAIOpenScaleClient.ai_client.data_mart.bindings.add("My WML instance", WatsonMachineLearningInstance(self.wml_credentials))

    def test_04_get_wml_client(self):
        binding_uid = TestAIOpenScaleClient.ai_client.data_mart.bindings.get_uids()[0]
        TestAIOpenScaleClient.wml_client = TestAIOpenScaleClient.ai_client.data_mart.bindings.get_native_engine_client(binding_uid)

    def test_05_prepare_deployment(self):
        model_data = create_spark_mllib_model_data()

        model_props = {self.wml_client.repository.ModelMetaNames.AUTHOR_NAME: "IBM",
                       self.wml_client.repository.ModelMetaNames.NAME: "test_" + self.test_uid
                       }

        published_model = self.wml_client.repository.store_model(model=model_data['model'], meta_props=model_props,
                                                                 training_data=model_data['training_data'],
                                                                 pipeline=model_data['pipeline'])
        TestAIOpenScaleClient.model_uid = self.wml_client.repository.get_model_uid(published_model)

        print('Stored model: ', TestAIOpenScaleClient.model_uid)

        deployment = self.wml_client.deployments.create(artifact_uid=self.model_uid, name="Test deployment",
                                                        asynchronous=False)
        TestAIOpenScaleClient.deployment_uid = self.wml_client.deployments.get_uid(deployment)

    def test_06_subscribe(self):
        subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.add(WatsonMachineLearningAsset(TestAIOpenScaleClient.model_uid))
        TestAIOpenScaleClient.aios_model_uid = subscription.uid

    def test_07_select_asset_and_get_details(self):
        TestAIOpenScaleClient.subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.get(TestAIOpenScaleClient.aios_model_uid)

    def test_08_list_deployments(self):
        TestAIOpenScaleClient.subscription.list_deployments()

    def test_09_setup(self):
        TestAIOpenScaleClient.subscription.explainability.enable(
            problem_type=ProblemType.MULTICLASS_CLASSIFICATION,
            input_data_type=InputDataType.STRUCTURED,
            feature_columns=["GENDER", "AGE", "MARITAL_STATUS", "PROFESSION"],
            label_column='label',
            training_data_reference=BluemixCloudObjectStorageReference(
                get_cos_credentials(),
                self.bucket_names['data'] + '/GoSales_Tx_NaiveBayes.csv',
                first_line_header=True
            ),
            categorical_columns=["GENDER", "MARITAL_STATUS", "PROFESSION"]
        )

    def test_10_get_details(self):
        details = TestAIOpenScaleClient.subscription.explainability.get_details()
        print("Explainability details: {}".format(details))

    def test_11_score(self):
        TestAIOpenScaleClient.transaction_id = str(uuid.uuid4()).replace("-", "")
        print("Transaction id: {}".format(TestAIOpenScaleClient.transaction_id))

        deployment_details = self.wml_client.deployments.get_details(TestAIOpenScaleClient.deployment_uid)
        scoring_endpoint = self.wml_client.deployments.get_scoring_url(deployment_details)

        payload_scoring = {"fields": ["GENDER", "AGE", "MARITAL_STATUS", "PROFESSION"],
                           "values": [["M", 23, "Single", "Student"]]}

        self.wml_client.deployments.score(scoring_endpoint, payload_scoring, transaction_id=TestAIOpenScaleClient.transaction_id)
        
        import time
        time.sleep(30)

    def test_12_run(self):
        TestAIOpenScaleClient.status = TestAIOpenScaleClient.subscription.explainability.run(transaction_id="{}-1".format(TestAIOpenScaleClient.transaction_id))
        print("Status: {}".format(TestAIOpenScaleClient.status))
        self.assertTrue(TestAIOpenScaleClient.status == "finished")

    def test_13_print_table_schema(self):
        TestAIOpenScaleClient.subscription.explainability.print_table_schema()

    def test_14_stats_on_explainability_table(self):
        TestAIOpenScaleClient.subscription.explainability.show_table()
        TestAIOpenScaleClient.subscription.explainability.describe_table()
        pandas_df = TestAIOpenScaleClient.subscription.explainability.get_table_content()
        print(str(pandas_df))
        self.assertTrue(pandas_df.size > 1)

    def test_15_disable(self):
        TestAIOpenScaleClient.subscription.explainability.disable()

    def test_16_get_metrics(self):
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics())
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(deployment_uid=TestAIOpenScaleClient.deployment_uid))
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(subscription_uid=TestAIOpenScaleClient.subscription.uid))
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(asset_uid=TestAIOpenScaleClient.subscription.source_uid))
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(metric_type='quality'))

    def test_17_unsubscribe(self):
        TestAIOpenScaleClient.ai_client.data_mart.subscriptions.delete(TestAIOpenScaleClient.subscription.uid)

    def test_18_clean(self):
        self.wml_client.deployments.delete(TestAIOpenScaleClient.deployment_uid)
        self.wml_client.repository.delete(TestAIOpenScaleClient.model_uid)

    def test_19_unbind(self):
        TestAIOpenScaleClient.ai_client.data_mart.bindings.delete(TestAIOpenScaleClient.subscription.binding_uid)

    def test_20_delete_data_mart(self):
        TestAIOpenScaleClient.ai_client.data_mart.delete()
        delete_schema(get_postgres_credentials(), get_schema_name())


if __name__ == '__main__':
    unittest.main()
