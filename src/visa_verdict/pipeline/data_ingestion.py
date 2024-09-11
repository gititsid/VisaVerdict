import sys

from src.visa_verdict.components.data_ingestion import DataIngestion
from src.visa_verdict.config.configuration import ConfigurationManager

from src.visa_verdict.logger import logging
from src.visa_verdict.exception import CustomException

STAGE_NAME = "Data Ingestion"


class DataIngestionPipeline:
    def __init__(self):
        self.config_manager = ConfigurationManager()
        self.data_ingestion_config = self.config_manager.get_data_ingestion_config()
        self.data_ingestion = DataIngestion(config=self.data_ingestion_config)

    def main(self):
        self.data_ingestion.main()


if __name__ == '__main__':
    try:
        logging.info(f">>>>>> stage '{STAGE_NAME}' started <<<<<<")

        data_ingestor = DataIngestionPipeline()
        data_ingestor.main()

        logging.info(f">>>>>> stage '{STAGE_NAME}' completed <<<<<<")

    except Exception as e:
        logging.error(f"Error occurred while running {STAGE_NAME}!")
        raise CustomException(e, sys)