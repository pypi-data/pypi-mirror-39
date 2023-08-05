class Properties:
    """
    For configuration, describes possible asset properties.

    """

    # TODO - add enums and make return list dynamic

    @staticmethod
    def get_properties_names():
        return ["model_type", "runtime_environment", "training_data_reference", "training_data_schema",
                "input_data_schema", "output_data_schema", "label_column", "input_data_type",
                "predicted_target_field", "prediction_probability_field"]
