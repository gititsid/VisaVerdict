import sys
import json

from src.visa_verdict.components.model_trainer import ModelTrainer
from src.visa_verdict.components.model_evaluation import ModelEvaluation
from src.visa_verdict.components.data_transformation import DataTransformation
from src.visa_verdict.config.configuration import ConfigurationManager

from src.visa_verdict.logger import logging
from src.visa_verdict.exception import CustomException


STAGE_NAME = "Model Evaluation"


class ModelEvaluationPipeline:
    def __init__(self):
        self.config_manager = ConfigurationManager()
        self.model_evaluation_config = self.config_manager.get_model_evaluation_config()
        self.model_evaluation = ModelEvaluation(config=self.model_evaluation_config)

    def main(self, x_train, y_train, x_test, y_test):

        train_accuracy_score, train_f1_score, test_accuracy_score, test_f1_score = self.model_evaluation.main(
            x_train, y_train, x_test, y_test
        )

        return train_accuracy_score, train_f1_score, test_accuracy_score, test_f1_score


if __name__ == '__main__':
    try:
        logging.info(f">>>>>> stage '{STAGE_NAME}' started <<<<<<")

        data_transformation_config = ConfigurationManager().get_data_transformation_config()
        data_transformer = DataTransformation(data_transformation_config)

        x_data, y_data = data_transformer.main()

        train_config = ConfigurationManager().get_model_training_config()
        model_training = ModelTrainer(train_config)

        x_train, x_test, y_train, y_test = model_training.train_test_split(x_data, y_data)

        model_evaluator = ModelEvaluationPipeline()
        train_accuracy_score, train_f1_score, test_accuracy_score, test_f1_score = model_evaluator.main(
            x_train, x_test, y_train, y_test
        )

        print(
            json.dumps(
                {
                    "train_accuracy_score": train_accuracy_score,
                    "train_f1_score": train_f1_score,
                    "test_accuracy_score": test_accuracy_score,
                    "test_f1_score": test_f1_score
                },
                indent=4
            )
        )

        logging.info(f">>>>>> stage '{STAGE_NAME}' completed <<<<<<")

    except Exception as e:
        logging.error(f"Error occurred while running {STAGE_NAME}!")
        raise CustomException(e, sys)
