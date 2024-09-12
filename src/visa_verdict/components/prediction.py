import sys
import pandas as pd

from src.visa_verdict.utils.common import load_object

from src.visa_verdict.logger import logging
from src.visa_verdict.exception import CustomException
from src.visa_verdict.entity.config_entity import PredictionConfig
from src.visa_verdict.config.configuration import ConfigurationManager


class Prediction:
    def __init__(self, config: PredictionConfig):
        self.config = config

        self.data_transformer = load_object(self.config.data_transformer)
        self.model = load_object(self.config.model_path)

    def predict(self, data: pd.DataFrame) -> pd.DataFrame:
        try:
            logging.info("Transforming data")
            data = self.data_transformer.transform(data)

            logging.info("Predicting")
            prediction = self.model.predict(data)[0]

            get_case_status_category = {0: "Certified", 1: "Denied"}

            case_status_category = get_case_status_category[prediction]

            logging.info(f"Prediction done successfully! Case_Status: {case_status_category}")

            return case_status_category
        except Exception as e:
            logging.error(f"Prediction failed: {e}")
            raise CustomException(e, sys)


class CustomData:
    def __init__(
            self, continent, education_of_employee, has_job_experience, requires_job_training, no_of_employees,
            region_of_employment, prevailing_wage, unit_of_wage, full_time_position, company_age
    ):
        self.continent = continent
        self.education_of_employee = education_of_employee
        self.has_job_experience = has_job_experience
        self.requires_job_training = requires_job_training
        self.no_of_employees = no_of_employees
        self.region_of_employment = region_of_employment
        self.prevailing_wage = prevailing_wage
        self.unit_of_wage = unit_of_wage
        self.full_time_position = full_time_position
        self.company_age = company_age

        self.custom_data = {
            "continent": self.continent,
            "education_of_employee": self.education_of_employee,
            "has_job_experience": self.has_job_experience,
            "requires_job_training": self.requires_job_training,
            "no_of_employees": self.no_of_employees,
            "region_of_employment": self.region_of_employment,
            "prevailing_wage": self.prevailing_wage,
            "unit_of_wage": self.unit_of_wage,
            "full_time_position": self.full_time_position,
            "company_age": self.company_age
        }

    def get_data_as_df(self):
        try:
            df = pd.DataFrame([self.custom_data])
            return df
        except Exception as e:
            logging.error(f"Failed to convert data to DataFrame!")
            raise CustomException(e, sys)


if __name__ == "__main__":
    config_manager = ConfigurationManager()
    prediction_config = config_manager.get_prediction_config()
    predictor = Prediction(prediction_config)

    custom_data = CustomData(
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

    data = custom_data.get_data_as_df()
    prediction = predictor.predict(data)

    print("prediction:", prediction)
