from .AbstractModel import AbstractModel
import os
import xgboost as xgb
import scipy


class XGBoost(AbstractModel):

    model_path = os.path.join(os.getcwd(), 'artifacts', 'XGboost', 'xgboost_model.tar.gz')

    def publish_to_wml(self, wml_client):
        return wml_client.repository.store_model(model=self.model_path, meta_props=self.get_model_props(wml_client))

    def get_model_props(self, wml_client):
        return {
            wml_client.repository.ModelMetaNames.AUTHOR_NAME: "IBM",
            wml_client.repository.ModelMetaNames.AUTHOR_EMAIL: "ibm@ibm.com",
            wml_client.repository.ModelMetaNames.NAME: "LOCALLY created agaricus prediction model",
            wml_client.repository.ModelMetaNames.FRAMEWORK_NAME: "xgboost",
            wml_client.repository.ModelMetaNames.FRAMEWORK_VERSION: "0.6",
            wml_client.repository.ModelMetaNames.TRAINING_DATA_SCHEMA: self.get_training_data_schema()
        }

    def get_scoring_payload(self):
        labels = []
        row = []
        col = []
        dat = []
        i = 0

        with open(os.path.join(os.getcwd(), 'datasets', 'XGboost', 'agaricus.txt.test')) as f:
            for l in f:
                arr = l.split()
                labels.append(int(arr[0]))
                for it in arr[1:]:
                    k, v = it.split(':')
                    row.append(i)
                    col.append(int(k))
                    dat.append(float(v))
                i += 1
            csr = scipy.sparse.csr_matrix((dat, (row, col)))

            inp_matrix = xgb.DMatrix(csr)

        return {
            'values': csr.getrow(0).toarray().tolist()
        }

    def get_training_data_schema(self):
        field = lambda x: {"name": "f" + str(x), "type": "float"}
        label = lambda x: {"name": "l" + str(x), "type": "float"}
        fields = [field(i) for i in range(127)]
        labels = [label(i) for i in range(1)]

        return {
            "features": {
                "type": "ndarray",
                "fields": fields
            },
            "labels": {
                "type": "ndarray",
                "fields": labels
            }
        }
