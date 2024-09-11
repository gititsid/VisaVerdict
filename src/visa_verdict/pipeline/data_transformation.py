import sys

from src.visa_verdict.components.data_transformation import DataTransformation
from src.visa_verdict.config.configuration import ConfigurationManager

from src.visa_verdict.logger import logging
from src.visa_verdict.exception import CustomException

STAGE_NAME = "Data Transformation"


class DataTransformationPipeline:
    def __init__(self):
        self.config_manager = ConfigurationManager()
        self.data_transformation_config = self.config_manager.get_data_transformation_config()
        self.data_transformation = DataTransformation(config=self.data_transformation_config)

    def main(self):
        x, y = self.data_transformation.main()

        return x, y


if __name__ == '__main__':
    try:
        logging.info(f">>>>>> stage '{STAGE_NAME}' started <<<<<<")

        data_transformer = DataTransformationPipeline()
        data_transformer.main()

        logging.info(f">>>>>> stage '{STAGE_NAME}' completed <<<<<<")

    except Exception as e:
        logging.error(f"Error occurred while running {STAGE_NAME}!")
        raise CustomException(e, sys)