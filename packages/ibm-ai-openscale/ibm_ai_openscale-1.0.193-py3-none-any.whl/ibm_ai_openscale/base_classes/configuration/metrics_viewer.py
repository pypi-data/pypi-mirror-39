from datetime import datetime, timedelta
from ibm_ai_openscale.utils import *
from ibm_ai_openscale.base_classes import Table
from ibm_ai_openscale.base_classes.configuration.table_from_rest_api_viewer import TableFromRestApiViewer

_DEFAULT_LIST_LENGTH = 50


class MetricsViewer(TableFromRestApiViewer):
    def __init__(self, ai_client, subscription, metric_type, table_name):
        TableFromRestApiViewer.__init__(self, ai_client, subscription, self, table_name)
        self._ai_client = ai_client
        self._subscription = subscription
        self._metric_type = metric_type

    def get_metrics(self, deployment_uid):
        validate_type(deployment_uid, 'deployment_uid', str, True)
        subscription_details = self._subscription.get_details()

        start = datetime.strptime(subscription_details['metadata']['created_at'], "%Y-%m-%dT%H:%M:%S.%fZ") -timedelta(hours=1)

        response = requests_session.get(
            self._ai_client._href_definitions.get_metrics_href(
                'samples',
                self._metric_type,
                start.isoformat() + 'Z',
                datetime.utcnow().isoformat() + 'Z',
                self._subscription.binding_uid,
                self._subscription.uid,
                deployment_uid
            ),
            headers=self._ai_client._get_headers()
        )

        return handle_response(200, "getting {} metrics".format(self._metric_type), response, True)

    def show_table(self, limit=10):
        """
        Show records in payload logging table. By default 10 records will be shown.

        :param limit: maximal number of fetched rows. By default set to 10. (optional)
        :type limit: int

        A way you might use me is:

        >>> client.payload_logging.show_table()
        >>> client.payload_logging.show_table(limit=20)
        >>> client.payload_logging.show_table(limit=None)
        """
        validate_type(limit, u'limit', int, False)

        result = self.get_table_content(format='python', limit=limit)

        rows = result['values']
        col_names = result['fields']

        Table(col_names, rows, date_field_name='ts').list(
            limit=limit,
            default_limit=_DEFAULT_LIST_LENGTH,
            title="{} (binding_id={}, subscription_id={})".format(
                self._get_table_name(),
                self._subscription.binding_uid,
                self._subscription.uid
            )
        )

    def _prepare_rows(self, obj, deployment_uid=''):
        raise NotImplemented()

    def _get_data_from_rest_api(self):
        def get_rows(deployment_uid): # TODO - asynchronous?
            response = requests_session.get(
                "{}/v1/data_marts/{}/metrics?format=samples&metric_type={}&binding_id={}&subscription_id={}&deployment_id={}&start={}&end={}".format(
                    self._ai_client._service_credentials['url'],
                    self._ai_client._service_credentials['data_mart_id'],
                    self._metric_type,
                    self._subscription.binding_uid,
                    self._subscription.uid,
                    deployment_uid,
                    "2000-01-01T00:00:00Z",
                    datetime.now().isoformat() + "Z"
                ),
                headers=self._ai_client._get_headers()
            )

            return [row for metrics in response.json()['metrics'] for row in self._prepare_rows(metrics, deployment_uid)]

        return [row for uid in self._subscription.get_deployment_uids() for row in get_rows(uid)]

    def _get_schema(self):
        raise NotImplemented()

    def _get_fields(self):
        return [field['name'] for field in self._get_schema()['fields']]