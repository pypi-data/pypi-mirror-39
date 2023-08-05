from .Engine import Engine
import requests
import time
import json


class Azure(Engine):
    def score(self, binding_details, subscription_details):
        self.score_product_line(binding_details, subscription_details)

    def score_product_line(self, binding_details, subscription_details):
        scoring_url = subscription_details['entity']['deployments'][0]['scoring_endpoint']['url']

        data = {
            "Inputs": {
                "input1":
                    [
                        {
                            'GENDER': "F",
                            'AGE': "27",
                            'MARITAL_STATUS': "Single",
                            'PROFESSION': "Professional",
                            'PRODUCT_LINE': "Personal Accessories",
                        }
                    ],
            },
            "GlobalParameters": {
            }
        }

        body = str.encode(json.dumps(data))

        token = subscription_details['entity']['deployments'][0]['scoring_endpoint']['credentials']['token']
        headers = subscription_details['entity']['deployments'][0]['scoring_endpoint']['request_headers']
        headers['Authorization'] = ('Bearer ' + token)

        start_time = time.time()
        response = requests.post(url=scoring_url, data=body, headers=headers)
        response_time = time.time() - start_time
        result = response.json()
        print('Scoring results: ' + json.dumps(result, indent=2))

        request = {'fields': list(data['Inputs']['input1'][0]),
                   'values': [list(x.values()) for x in data['Inputs']['input1']]}

        response = {'fields': list(result['Results']['output1'][0]),
                    'values': [list(x.values()) for x in result['Results']['output1']]}

        print('request: ' + str(request))
        print('response: ' + str(response))

        self.latest_request = request
        self.latest_response = response
        self.latest_response_time = response_time

        return request, response, response_time

    def score_iris(self, binding_details, subscription_details):
        scoring_url = subscription_details['entity']['deployments'][0]['scoring_endpoint']['url']

        data = {
                "Inputs": {
                        "input1":
                        [
                            {
                                    'sepal_length': "1.1",
                                    'sepal_width': "15.5",
                                    'petal_length': "1.4",
                                    'petal_width': "1.2",
                            }
                        ],
                },
                "GlobalParameters":  {
                }
        }

        body = str.encode(json.dumps(data))

        token = subscription_details['entity']['deployments'][0]['scoring_endpoint']['credentials']['token']
        headers = subscription_details['entity']['deployments'][0]['scoring_endpoint']['request_headers']
        headers['Authorization'] = ('Bearer ' + token)

        start_time = time.time()
        response = requests.post(url=scoring_url, data=body, headers=headers)
        response_time = time.time() - start_time
        result = response.json()
        print('Scoring results: ' + json.dumps(result, indent=2))

        request = {'fields': list(data['Inputs']['input1'][0]),
                   'values': [list(x.values()) for x in data['Inputs']['input1']]}

        response = {'fields': list(result['Results']['output1'][0]),
                    'values': [list(x.values()) for x in result['Results']['output1']]}

        print('request: ' + str(request))
        print('response: ' + str(response))

        self.latest_request = request
        self.latest_response = response
        self.latest_response_time = response_time

        return request, response, response_time
