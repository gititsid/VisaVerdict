import sys

from src.visa_verdict.components.data_validation import DataValidation
from src.visa_verdict.config.configuration import ConfigurationManager

from src.visa_verdict.logger import logging
from src.visa_verdict.exception import CustomException

STAGE_NAME = "Data Validation"


class DataValidationPipeline:
    def __init__(self):
        self.config_manager = ConfigurationManager()
        self.data_validation_config = self.config_manager.get_data_validation_config()
        self.data_validation = DataValidation(config=self.data_validation_config)

    def main(self):
        validation_status = self.data_validation.main()
        return validation_status


if __name__ == '__main__':
    try:
        logging.info(f">>>>>> stage '{STAGE_NAME}' started <<<<<<")

        data_validator = DataValidationPipeline()
        data_validator.main()

        logging.info(f">>>>>> stage '{STAGE_NAME}' completed <<<<<<")

    except Exception as e:
        logging.error(f"Error occurred while running {STAGE_NAME}!")
        raise CustomException(e, sys)