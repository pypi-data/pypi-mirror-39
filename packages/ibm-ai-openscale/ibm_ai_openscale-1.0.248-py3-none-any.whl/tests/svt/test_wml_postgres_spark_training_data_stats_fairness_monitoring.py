# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-J33
# Copyright IBM Corp. 2018
# The source code for this program is not published or other-wise divested of its trade 
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

import logging
import unittest

from ibm_ai_openscale import APIClient
from ibm_ai_openscale.engines import *
from ibm_ai_openscale.supporting_classes import *
from models_preparation import *
from preparation_and_cleaning import *


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

    @classmethod
    def setUpClass(self):
        TestAIOpenScaleClient.logger.info("Service Instance: setting up credentials")

        clean_env()

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

    def test_07b_list_deployments(self):
        TestAIOpenScaleClient.subscription.list_deployments()

    def test_08_setup_fairness_monitoring_with_training_data_json(self):
        import json

        with open('assets/training_distribution.json') as json_data:
            d = json.load(json_data)
            print(d)

        TestAIOpenScaleClient.subscription.fairness_monitoring.enable(
            features=[
                Feature("AGE", [[20,50],[60,70]], [[51,59]], 0.8)#,
                #Feature("PROFESSION", ['Student'], ['Executive'], 0.8)
            ],
            prediction_column='prediction',
            favourable_classes=[3], # TODO try also with something outside these classes
            unfavourable_classes=[1],
            min_records=4,
            training_data_stats=d
        )

    def test_09_get_fairness_configuration(self):
        fairness_details = TestAIOpenScaleClient.subscription.fairness_monitoring.get_details()
        subscription_details = TestAIOpenScaleClient.subscription.get_details()

        print('Subscription details: ' + str(subscription_details))
        print('Fairness details: ' + str(fairness_details))

    """
    def test_08c_score(self):
        deployment_details = self.wml_client.deployments.get_details(TestAIOpenScaleClient.deployment_uid)
        scoring_endpoint = self.wml_client.deployments.get_scoring_url(deployment_details)

        payload_scoring = {"fields": ["GENDER", "AGE", "MARITAL_STATUS", "PROFESSION"],
                           "values": [
                               ["M", 23, "Single", "Student"],
                               ["M", 50, "Single", "Executive"],
                               ["M", 70, "Single", "Student"],
                               ["M", 20, "Single", "Executive"],
                               ["M", 23, "Single", "Student"],
                               ["M", 55, "Single", "Executive"],
                               ["M", 70, "Single", "Student"],
                               ["M", 60, "Single", "Executive"]
                           ]
                           }

        self.wml_client.deployments.score(scoring_endpoint, payload_scoring)
        print('SCORING_RESULT', self.wml_client.deployments.score(scoring_endpoint, payload_scoring))

    def test_09_get_fairness_monitoring_details(self):
        print(TestAIOpenScaleClient.subscription.fairness_monitoring.get_details())

    def test_10b_run(self):
        TestAIOpenScaleClient.subscription.fairness_monitoring.run()
        import time
        time.sleep(2 * 60)

    def test_11_stats_on_fairness_monitoring_table(self):
        TestAIOpenScaleClient.subscription.payload_logging.show_table()
        TestAIOpenScaleClient.subscription.fairness_monitoring.print_table_schema()
        TestAIOpenScaleClient.subscription.fairness_monitoring.show_table()
        TestAIOpenScaleClient.subscription.fairness_monitoring.describe_table()
        pandas_df = TestAIOpenScaleClient.subscription.fairness_monitoring.get_table_content()
        print(str(pandas_df))
        self.assertTrue(pandas_df.size > 1)
        print(TestAIOpenScaleClient.subscription.payload_logging.get_table_content(format='python'))
        print(TestAIOpenScaleClient.subscription.fairness_monitoring.get_table_content(format='python'))

    def test_12_disable_fairness_monitoring(self):
        TestAIOpenScaleClient.subscription.fairness_monitoring.disable()

    def test_13_get_metrics(self):
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics())
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(deployment_uid=TestAIOpenScaleClient.deployment_uid))
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(subscription_uid=TestAIOpenScaleClient.subscription.uid))
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(asset_uid=TestAIOpenScaleClient.subscription.source_uid))
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(asset_uid=TestAIOpenScaleClient.subscription.source_uid, metric_type=MetricTypes.FAIRNESS_MONITORING))
        print(TestAIOpenScaleClient.subscription.fairness_monitoring.get_metrics(TestAIOpenScaleClient.deployment_uid))

        self.assertTrue(len(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics()['deployment_metrics']) > 0)
        self.assertTrue(len(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(deployment_uid=TestAIOpenScaleClient.deployment_uid)['deployment_metrics']) > 0)
        self.assertTrue(len(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(subscription_uid=TestAIOpenScaleClient.subscription.uid)['deployment_metrics']) > 0)
        self.assertTrue(len(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(asset_uid=TestAIOpenScaleClient.subscription.source_uid)['deployment_metrics']) > 0)
        self.assertTrue(len(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(asset_uid=TestAIOpenScaleClient.subscription.source_uid, metric_type=MetricTypes.FAIRNESS_MONITORING)['deployment_metrics'][0]['metrics']) > 0)
        self.assertTrue(len(TestAIOpenScaleClient.subscription.fairness_monitoring.get_metrics(TestAIOpenScaleClient.deployment_uid)['metrics']) > 0)

    """
    def test_15_unsubscribe(self):
        TestAIOpenScaleClient.ai_client.data_mart.subscriptions.delete(TestAIOpenScaleClient.subscription.uid)
        wait_until_deleted(TestAIOpenScaleClient.ai_client, subscription_uid=TestAIOpenScaleClient.subscription.uid)

    def test_16_clean(self):
        self.wml_client.deployments.delete(TestAIOpenScaleClient.deployment_uid)
        self.wml_client.repository.delete(TestAIOpenScaleClient.model_uid)

    def test_17_unbind(self):
        TestAIOpenScaleClient.ai_client.data_mart.bindings.delete(TestAIOpenScaleClient.subscription.binding_uid)
        wait_until_deleted(TestAIOpenScaleClient.ai_client, binding_uid=TestAIOpenScaleClient.subscription.binding_uid)

    def test_18_delete_data_mart(self):
        TestAIOpenScaleClient.ai_client.data_mart.delete()
        wait_until_deleted(TestAIOpenScaleClient.ai_client, data_mart=True)
        delete_schema(get_postgres_credentials(), get_schema_name())


if __name__ == '__main__':
    unittest.main()
