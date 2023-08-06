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
from ibm_ai_openscale.engines import *
from test_base import TestBasePostgres


class TestAIOpenScaleClient(TestBasePostgres):
    function_uid = None

    def test_01_create_client(self):
        self.create_client()

    def test_02_setup_data_mart(self):
        self.setup_data_mart()

    def test_03_bind_wml_instance(self):
        self.bind_wml_instance()

    def test_04_get_wml_client(self):
        self.get_wml_client()

    def test_05_prepare_deployment(self):
        def score(payload):
            values = [[row[0]*row[1]] for row in payload['values']]
            return {'fields': ['multiplication'], 'values': values}

        ai_function_details = self.wml_client.repository.store_function(score, "My func")

        TestAIOpenScaleClient.function_uid = self.wml_client.repository.get_function_uid(ai_function_details)

        deployment = self.wml_client.deployments.create(artifact_uid=TestAIOpenScaleClient.function_uid, name="Test deployment",
                                                        asynchronous=False)
        TestBasePostgres.deployment_uid = self.wml_client.deployments.get_uid(deployment)

    def test_06_subscribe(self):
        TestAIOpenScaleClient.subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.add(WatsonMachineLearningAsset(TestAIOpenScaleClient.function_uid))

    def test_07_select_asset_and_get_details(self):
        self.select_asset_and_get_details()

    def test_08_list_deployments(self):
        self.list_deployments()

    def test_09_setup_payload_logging(self):
        TestAIOpenScaleClient.subscription.payload_logging.enable()

    def test_10_get_payload_logging_details(self):
        self.get_payload_logging_details()

    def test_11_score(self):
        deployment_details = self.wml_client.deployments.get_details(TestAIOpenScaleClient.deployment_uid)
        scoring_endpoint = self.wml_client.deployments.get_scoring_url(deployment_details)

        payload_scoring = {"fields": ["x", "y"],
                           "values": [[2, 3], [3.1, 2.2]]}

        self.wml_client.deployments.score(scoring_endpoint, payload_scoring)
        self.wml_client.deployments.score(scoring_endpoint, payload_scoring)
        time.sleep(20)

    def test_12_stats_on_payload_logging_table(self):
        self.stats_on_payload_logging_table()

    def test_13_disable_payload_logging(self):
        TestAIOpenScaleClient.subscription.payload_logging.disable()

    def test_14_unsubscribe(self):
        self.unsubscribe()

    def test_15_unbind(self):
        self.unbind()

    def test_16_delete_data_mart(self):
        self.delete_data_mart()


if __name__ == '__main__':
    unittest.main()
