from ibm_ai_openscale.utils import *
from ibm_ai_openscale.supporting_classes import *
from ibm_ai_openscale.subscriptions import Subscriptions
from ibm_ai_openscale.bindings import Bindings
import inspect


class DataMart:
    """
    Manages DB Instance.

    :var bindings: Manage bindings of you AI OpenScale instance.
    :vartype bindings: Bindings
    :var subscriptions: Manage subscriptions of you AI OpenScale instance.
    :vartype subscriptions: Subscriptions
    """
    def __init__(self, ai_client):
        from ibm_ai_openscale.client import APIClient
        validate_type(ai_client, 'ai_client', APIClient, True)
        self._logger = logging.getLogger(__name__)
        self._ai_client = ai_client
        self._internal_db = False
        self.bindings = Bindings(ai_client)
        self.subscriptions = Subscriptions(ai_client)

    def setup(self, postgres_credentials=None, db_credentials=None, schema=None, internal_db=False):
        """
        Setups db instance.

        :param db_credentials: describes the instance which should be connected
        :type db_credentials: dict

        :param schema: schema in your database under which the tables should be created
        :type schema: str

        :param internal_db: you can use internally provided database. Please note that this db comes with limitations.
        :type internal_db: bool
        """

        if internal_db is False:
            if postgres_credentials is not None:
                # DeprecationWarning does not work in notebook - need to use print as workaround sic!
                # TODO remove in next major release support for this and optional Schema
                print("DeprecationWarning: 'postgres_credentials' parameter is deprecated and will be removed in 1.1.0 release; use 'db_credentials' instead.")
                db_credentials = postgres_credentials

            validate_type(db_credentials, 'db_credentials', dict, True)
            validate_type(schema, 'schema', str, True)
            validate_type(db_credentials['uri'], 'db_credentials.uri', str, True)

            db_type = None
            db_name = None

            if 'postgres' in db_credentials['uri']:
                db_type = "postgresql"
            elif 'db2' in db_credentials['uri']:
                db_type = "db2"

            if 'name' in db_credentials.keys():
                db_name = db_credentials['name']
            else:
                db_name = str(db_type)

            database_configuration = {
                "database_type": db_type,
                "name": db_name,
                "credentials": db_credentials,
                "location": {"schema": schema}
            }

            payload = {"database_configuration": database_configuration}
        else:
            self._internal_db = internal_db
            payload = {"internal_database": internal_db}

        response = requests_session.put(
            self._ai_client._href_definitions.get_data_mart_href(),
            json=payload,
            headers=self._ai_client._get_headers()
        )

        try:
            handle_response(200, "setup of data mart", response, False)
        except ApiRequestWarning:
            ApiRequestWarning.print_msg(error_msg=u'Warning during {}.'.format('setup of data mart'), response=response)
            return

    def update(self, postgres_credentials=None, db_credentials=None, schema=None):
        """
         Updates data mart configuration to work with new db instance. There is no data migration.

         :param db_credentials: describes the instance which should be connected
         :type db_credentials: dict

         :param schema: schema in your database under which the tables should be created (optional)
         :type schema: str
        """

        if postgres_credentials is not None:
            self._logger.warning("'postgres_credentials' parameter is deprecated; use 'db_credentials' instead.")
            db_credentials = postgres_credentials

        validate_type(db_credentials, 'db_credentials', dict, True)
        validate_type(db_credentials['uri'], 'db_credentials.uri', str, True)

        db_type = None
        db_name = None

        if 'postgres' in db_credentials['uri']:
            db_type = "postgresql"

        if 'name' in db_credentials.keys():
            db_name = db_credentials['name']
        else:
            db_name = str(db_type)

        payload = {
            "database_type": db_type,
            "name": db_name,
            "credentials": db_credentials
        }

        if schema is not None:
            payload['location'] = {
                "schema": schema
            }

        response = requests_session.put(
            self._ai_client._href_definitions.get_data_mart_href() + '?force=true',
            json={"database_configuration": payload},
            headers=self._ai_client._get_headers()
        )

        handle_response(200, "setup of data mart", response, False)

    def get_details(self):
        """
        Get db instance details.

        :return: db instance details
        :rtype: dict
        """
        response = requests_session.get(
            self._ai_client._href_definitions.get_data_mart_href(),
            headers=self._ai_client._get_headers()
        )

        if self._internal_db:
            # check if get_details() is called internally or externally
            if '._ai_client' not in str(inspect.stack()[1]):
                return handle_response(200, "getting data mart details", response, True, True)
            else:
                return handle_response(200, "getting data mart details", response, True)
        else:
            return handle_response(200, "getting data mart details", response, True)

    def get_deployment_metrics(self, subscription_uid=None, asset_uid=None, deployment_uid=None, metric_type=None):
        """
        Get metrics.

        :param subscription_uid: UID of subscription for which the metrics which be prepared (optional)
        :type subscription_uid: str

        :param asset_uid: UID of asset for which the metrics which be prepared (optional)
        :type asset_uid: str

        :param deployment_uid: UID of deployment for which the metrics which be prepared (optional)
        :type deployment_uid: str

        :param metric_type: metric type which should be returned (optional)
        :type metric_type: str

        :return: metrics
        :rtype: dict
        """
        validate_type(subscription_uid, 'subscription_uid', str, False)
        validate_type(asset_uid, 'asset_uid', str, False)
        validate_type(deployment_uid, 'deployment_uid', str, False)

        # TODO MetricTypes should be enum
        validate_type(metric_type, 'metric_type', [MetricTypes, str], False)

        response = requests_session.get(
            self._ai_client._href_definitions.get_deployment_metrics_href(),
            headers=self._ai_client._get_headers()
        )

        details = handle_response(200, "getting deployment metrics", response, True)['deployment_metrics']

        if subscription_uid is not None:
            details = list(filter(lambda x: x['subscription']['subscription_id'] == subscription_uid, details))

        if asset_uid is not None:
            details = list(filter(lambda x: x['asset']['asset_id'] == asset_uid, details))

        if deployment_uid is not None:
            details = list(filter(lambda x: x['deployment']['deployment_id'] == deployment_uid, details))

        if metric_type is not None:
            for record in details:
                record['metrics'] = list(filter(lambda m: m['metric_type'] == metric_type, record['metrics']))

        return {'deployment_metrics': details}

    def delete(self, force=True):
        """
        Delete data_mart configuration.

        :param force: force configuration deletion
        :type force: bool
        """

        validate_type(force, 'force', bool, True)
        response = requests_session.delete(
            self._ai_client._href_definitions.get_data_mart_href() + '?force=' + str(force).lower(),
            headers=self._ai_client._get_headers()
        )

        handle_response(202, "delete of data mart", response, False)

        start_time = time.time()
        elapsed_time = 0
        timeout = 120
        while True and elapsed_time < timeout:
            try:
                self.get_details()
                elapsed_time = time.time() - start_time
                time.sleep(10)
            except ApiRequestFailure as ex:
                if "404" in str(ex.error_msg):
                    return
                else:
                    raise ex

        self._logger.info("Deletion takes more than {} seconds - switching to background mode".format(timeout))

