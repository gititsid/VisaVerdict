import sys

from src.visa_verdict.components.prediction import Prediction, CustomData
from src.visa_verdict.config.configuration import ConfigurationManager

from src.visa_verdict.logger import logging
from src.visa_verdict.exception import CustomException

STAGE_NAME = "Prediction"


class PredictionPipeline:
    def __init__(self):
        self.config_manager = ConfigurationManager()
        self.prediction_config = self.config_manager.get_prediction_config()
        self.predictor = Prediction(config=self.prediction_config)

    def predict(self, custom_data):
        # Input Data
        input_data = custom_data.get_data_as_df()

        return self.predictor.predict(input_data)


if __name__ == '__main__':
    try:
        logging.info(f">>>>>> stage '{STAGE_NAME}' started <<<<<<")

        prediction = PredictionPipeline()

        # Data for prediction
        pred_datapoint = CustomData(
            continent="Asia",
            education_of_employee="High School",
            has_job_experience="N",
            requires_job_training="N",
            no_of_employees=14513,
            region_of_employment="West",
            prevailing_wage=592.2029,
            unit_of_wage="Hour",
            full_time_position="Y",
            company_age=17
        )

        # Predict
        verdict = prediction.predict(pred_datapoint)

        logging.info(f"Prediction: {verdict}")

        logging.info(f">>>>>> stage '{STAGE_NAME}' completed <<<<<<")

    except Exception as e:
        logging.error(f"Error occurred while running {STAGE_NAME}!")
        raise CustomException(e, sys)
