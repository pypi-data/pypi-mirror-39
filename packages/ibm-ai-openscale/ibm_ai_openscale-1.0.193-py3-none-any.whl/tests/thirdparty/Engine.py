from abc import ABC, abstractmethod


class Engine(ABC):

    latest_request = None
    latest_response = None
    latest_response_time = None

    @abstractmethod
    def score(self, binding_details, subscription_details):
        pass

    def get_latest_scoring(self):
        return self.latest_request, self.latest_response, self.latest_response_time
