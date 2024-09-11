import sys
import pickle
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

from src.visa_verdict.config.configuration import ConfigurationManager
from src.visa_verdict.entity.config_entity import ModelTrainingConfig
from src.visa_verdict.components.data_transformation import DataTransformation

from src.visa_verdict.logger import logging
from src.visa_verdict.exception import CustomException


class ModelTrainer:
    def __init__(self, config: ModelTrainingConfig):
        self.config = config

    def train_test_split(self, x_data: np.array, y_data: np.array) -> tuple[np.array, np.array, np.array, np.array]:
        try:
            logging.info("Splitting data into training and testing sets:")

            x_train, x_test, y_train, y_test = train_test_split(
                x_data,
                y_data,
                test_size=self.config.test_size,
                random_state=self.config.random_state
            )

            logging.info("Data split successfully!")

            return x_train, x_test, y_train, y_test

        except Exception as e:
            logging.error(f"Error splitting data!")
            raise CustomException(e, sys)

    def train_model(self, x_data: np.array, y_data: np.array):
        try:
            logging.info("Training model:")

            x_train, x_test, y_train, y_test = self.train_test_split(x_data, y_data)

            hyperparameters = {k: v for d in list(self.config.hyperparameters) for k, v in d.items()}
            rfc = RandomForestClassifier(**hyperparameters)

            rfc.fit(x_train, y_train)

            with open(self.config.model_path, 'wb') as model_file:
                pickle.dump(rfc, model_file)

            logging.info("Model trained successfully!")

        except Exception as e:
            logging.error(f"Error training model!")
            raise CustomException(e, sys)

    def main(self, x_data: np.array, y_data: np.array):
        self.train_model(x_data, y_data)


if __name__ == "__main__":
    data_transformation_config = ConfigurationManager().get_data_transformation_config()
    model_training_config = ConfigurationManager().get_model_training_config()

    data_transformer = DataTransformation(data_transformation_config)
    x_data, y_data = data_transformer.main()

    model_trainer = ModelTrainer(model_training_config)
    model_trainer.main(x_data, y_data)
