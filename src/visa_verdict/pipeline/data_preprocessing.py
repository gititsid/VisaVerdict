import sys

from src.visa_verdict.components.data_preprocessing import DataPreprocessing
from src.visa_verdict.config.configuration import ConfigurationManager

from src.visa_verdict.logger import logging
from src.visa_verdict.exception import CustomException

STAGE_NAME = "Data Preprocessing"


class DataPreprocessingPipeline:
    def __init__(self):
        pass

    @staticmethod
    def main():
        config_manager = ConfigurationManager()
        data_preprocessing_config = config_manager.get_data_preprocessing_config()
        data_preprocessing = DataPreprocessing(config=data_preprocessing_config)

        data_preprocessing.main()


if __name__ == '__main__':
    try:
        logging.info(f">>>>>> stage '{STAGE_NAME}' started <<<<<<")

        data_preprocessor = DataPreprocessingPipeline()
        data_preprocessor.main()

        logging.info(f">>>>>> stage '{STAGE_NAME}' completed <<<<<<")

    except Exception as e:
        logging.error(f"Error occurred while running {STAGE_NAME}!")
        raise CustomException(e, sys)