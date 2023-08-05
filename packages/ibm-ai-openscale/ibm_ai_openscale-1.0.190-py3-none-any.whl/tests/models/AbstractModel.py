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
