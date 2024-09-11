import json
import sys

from sklearn.metrics import accuracy_score, f1_score

from src.visa_verdict.utils.common import *
from src.visa_verdict.config.configuration import ConfigurationManager
from src.visa_verdict.entity.config_entity import ModelEvaluationConfig

from src.visa_verdict.components.data_transformation import DataTransformation
from src.visa_verdict.components.model_trainer import ModelTrainer

from src.visa_verdict.logger import logging
from src.visa_verdict.exception import CustomException


class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config
        self.preprocessor = load_object(self.config.data_transformer)
        self.model = load_object(self.config.model_path)

    @staticmethod
    def _evaluate_model(true, predicted):
        accuracy = accuracy_score(true, predicted)
        f1 = f1_score(true, predicted)
        return accuracy, f1

    def evaluate(self, train_data, test_data, y_train, y_test):
        try:
            logging.info("Model Evaluation Started")

            # Evaluate the model
            train_accuracy_score, train_f1_score = self._evaluate_model(y_train, self.model.predict(train_data))
            test_accuracy_score, test_f1_score = self._evaluate_model(y_test, self.model.predict(test_data))

            # Save the metrics
            write_json(self.config.train_metrics, {"accuracy": train_accuracy_score, "f1": train_f1_score})
            write_json(self.config.test_metrics, {"accuracy": test_accuracy_score, "f1": test_f1_score})

            logging.info("Model Evaluation Completed!")

            return train_accuracy_score, train_f1_score, test_accuracy_score, test_f1_score

        except Exception as e:
            logging.error(f"Error occurred while evaluating the model!")
            raise CustomException(e, sys)

    def main(self, x_train, x_test, y_train, y_test):
        try:
            train_accuracy_score, train_f1_score, test_accuracy_score, test_f1_score = self.evaluate(
                x_train, x_test, y_train, y_test
            )
            return train_accuracy_score, train_f1_score, test_accuracy_score, test_f1_score
        except Exception as e:
            logging.error(f"Error occurred while evaluating the model!")
            raise CustomException(e, sys)


if __name__ == "__main__":
    data_transformation_config = ConfigurationManager().get_data_transformation_config()
    data_transformer = DataTransformation(data_transformation_config)

    x_data, y_data = data_transformer.main()

    train_config = ConfigurationManager().get_model_training_config()
    model_training = ModelTrainer(train_config)

    x_train, x_test, y_train, y_test = model_training.train_test_split(x_data, y_data)

    model_evaluation_config = ConfigurationManager().get_model_evaluation_config()
    model_evaluation = ModelEvaluation(model_evaluation_config)

    train_accuracy_score, train_f1_score, test_accuracy_score, test_f1_score = model_evaluation.main(
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

