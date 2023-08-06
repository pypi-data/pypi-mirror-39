# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-J33
# Copyright IBM Corp. 2018
# The source code for this program is not published or other-wise divested of its trade 
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

from ibm_ai_openscale.base_classes.assets import Asset
from ibm_ai_openscale.utils import *
from enum import Enum


class KnownServiceAsset(Asset):
    def __init__(self, source_uid, binding_uid=None, input_data_type=None, problem_type=None, label_column=None,
                 prediction_column=None, probability_column=None):
        validate_type(source_uid, 'source_uid', str, True)
        validate_type(binding_uid, 'binding_uid', str, False)
        validate_type(input_data_type, 'input_data_type', [str, Enum], False)
        validate_type(problem_type, 'problem_type', [str, Enum], False)
        validate_type(label_column, 'label_column', [str, Enum], False)
        validate_type(prediction_column, 'prediction_column', [str, Enum], False)
        validate_type(probability_column, 'probability_column', [str, Enum], False)

        Asset.__init__(self, binding_uid)
        self.source_uid = source_uid
        self.input_data_type = input_data_type
        self.problem_type = problem_type
        self.label_column = label_column
        self.prediction_column = prediction_column
        self.probability_column = probability_column

