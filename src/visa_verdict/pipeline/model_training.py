import sys

from src.visa_verdict.components.model_trainer import ModelTrainer
from src.visa_verdict.components.data_transformation import DataTransformation
from src.visa_verdict.config.configuration import ConfigurationManager

from src.visa_verdict.logger import logging
from src.visa_verdict.exception import CustomException

STAGE_NAME = "Model Training"


class ModelTrainingPipeline:
    def __init__(self):
        self.config_manager = ConfigurationManager()
        self.model_training_config = self.config_manager.get_model_training_config()
        self.model_trainer = ModelTrainer(config=self.model_training_config)

    def main(self, x_data, y_data):
        self.model_trainer.main(x_data, y_data)


if __name__ == '__main__':
    try:
        logging.info(f">>>>>> stage '{STAGE_NAME}' started <<<<<<")

        data_transformation_config = ConfigurationManager().get_data_transformation_config()
        data_transformer = DataTransformation(data_transformation_config)

        x_data, y_data = data_transformer.main()

        model_trainer = ModelTrainingPipeline()
        model_trainer.main(x_data, y_data)

        logging.info(f">>>>>> stage '{STAGE_NAME}' completed <<<<<<")

    except Exception as e:
        logging.error(f"Error occurred while running {STAGE_NAME}!")
        raise CustomException(e, sys)