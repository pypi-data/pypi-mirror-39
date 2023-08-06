# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-J33
# Copyright IBM Corp. 2018
# The source code for this program is not published or other-wise divested of its trade 
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

from abc import ABC, abstractmethod


class AbstractModel(ABC):

    @abstractmethod
    def publish_to_wml(self, wml_client):
        pass

    @abstractmethod
    def get_model_props(self, wml_client):
        pass

    @abstractmethod
    def get_scoring_payload(self):
        pass


class AbstractFeedbackModel(ABC):

    @abstractmethod
    def publish_to_wml(self, wml_client, db2_credentials):
        pass

    @abstractmethod
    def get_model_props(self, wml_client, db2_credentials):
        pass

    @abstractmethod
    def get_training_data_reference(self, db2_credentials):
        pass

    @abstractmethod
    def get_feedback_data(self):
        pass

    @abstractmethod
    def get_scoring_payload(self):
        pass
