# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-J33
# Copyright IBM Corp. 2018
# The source code for this program is not published or other-wise divested of its trade 
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

import unittest
from test_base import TestBasePostgres
from models.spark import Telco

@unittest.skip("Already covered ...")
class TestAIOpenScaleClient(TestBasePostgres):

    model = Telco()
    local_subscription = None

    def test_01_create_client(self):
        self.create_client()

    def test_02_setup_data_mart(self):
        self.setup_data_mart()

    def test_03_setup_data_mart_again(self):
        message = r"""Warning during setup of data mart.\nStatus code: 409, body: {"trace":"(.*)","errors":\[{"code":"AISCS0004W","message":"Data Mart with this id is already defined"}]}"""
        self.assert_stdout(self.setup_data_mart, message)
        self.assert_stdout(self.setup_data_mart, message)

    def test_04_bind_wml_instance(self):
        self.bind_wml_instance()

    def test_05_rebind(self):
        message = r"""Warning during bind instance.\nStatus code: 409, body: {"trace":"(.*)","errors":\[{"code":"AISCS0004W","message":"Binding with service_type `watson_machine_learning` is already defined: `(.*)`"}]}"""
        self.assert_stdout(self.bind_wml_instance, message)
        self.assert_stdout(self.bind_wml_instance, message)

    def test_06_get_wml_client(self):
        self.get_wml_client()

    def test_07_prepare_deployment(self):
        self.prepare_deployment(self.model)

    def test_08_subscribe(self):
        self.subscribe()
        TestAIOpenScaleClient.local_subscription = TestBasePostgres.subscription

    def test_09_resubscribe(self):
        message = r"""Warning during subscription of asset.\nStatus code: 409, body: {"trace":"(.*)","errors":\[{"code":"AISCS0004W","message":"Subscription for asset `(.*)` is already defined: `(.*)`"}]}"""
        self.assert_stdout(self.subscribe, message)
        self.assert_stdout(self.subscribe, message)

    def test_10_unsubscribe(self):
        self.subscription = TestAIOpenScaleClient.local_subscription
        TestBasePostgres.subscription = TestAIOpenScaleClient.local_subscription
        self.unsubscribe()

    def test_11_unbind(self):
        self.unbind()

    def test_12_delete_data_mart(self):
        self.delete_data_mart()


if __name__ == '__main__':
    unittest.main()
