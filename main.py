import sys
import json

from src.visa_verdict.pipeline.data_ingestion import DataIngestionPipeline
from src.visa_verdict.pipeline.data_validation import DataValidationPipeline
from src.visa_verdict.pipeline.data_preprocessing import DataPreprocessingPipeline
from src.visa_verdict.pipeline.data_transformation import DataTransformationPipeline
from src.visa_verdict.pipeline.model_training import ModelTrainingPipeline
from src.visa_verdict.pipeline.model_evaluation import ModelEvaluationPipeline

from src.visa_verdict.logger import logging
from src.visa_verdict.exception import CustomException


logging.info(">>>>>> Visa Verdict pipeline started <<<<<<\n")

STAGE_NAME = "Data Ingestion"

try:
    logging.info(f">>>>>> stage '{STAGE_NAME}' started <<<<<<")

    data_ingestor = DataIngestionPipeline()
    data_ingestor.main()

    logging.info(f">>>>>> stage '{STAGE_NAME}' completed <<<<<<\n")

except Exception as e:
    logging.error(f"Error occurred while running {STAGE_NAME}!")
    raise CustomException(e, sys)


STAGE_NAME = "Data Preprocessing"

try:
    logging.info(f">>>>>> stage '{STAGE_NAME}' started <<<<<<")

    data_preprocessor = DataPreprocessingPipeline()
    data_preprocessor.main()

    logging.info(f">>>>>> stage '{STAGE_NAME}' completed <<<<<<\n")

except Exception as e:
    logging.error(f"Error occurred while running {STAGE_NAME}!")
    raise CustomException(e, sys)

STAGE_NAME = "Data Validation"

try:
    logging.info(f">>>>>> stage '{STAGE_NAME}' started <<<<<<")

    data_validator = DataValidationPipeline()
    data_validator.main()

    logging.info(f">>>>>> stage '{STAGE_NAME}' completed <<<<<<\n")

except Exception as e:
    logging.error(f"Error occurred while running {STAGE_NAME}!")
    raise CustomException(e, sys)


STAGE_NAME = "Data Transformation"

try:
    logging.info(f">>>>>> stage '{STAGE_NAME}' started <<<<<<")

    data_transformer = DataTransformationPipeline()
    x, y = data_transformer.main()

    logging.info(f">>>>>> stage '{STAGE_NAME}' completed <<<<<<\n")

except Exception as e:
    logging.error(f"Error occurred while running {STAGE_NAME}!")
    raise CustomException(e, sys)


STAGE_NAME = "Model Training"

try:
    logging.info(f">>>>>> stage '{STAGE_NAME}' started <<<<<<")

    model_trainer_ = ModelTrainingPipeline()

    model_trainer_.main(x_data=x, y_data=y)
    x_train, x_test, y_train, y_test = model_trainer_.model_trainer.train_test_split(x, y)

    logging.info(f">>>>>> stage '{STAGE_NAME}' completed <<<<<<\n")

except Exception as e:
    logging.error(f"Error occurred while running {STAGE_NAME}!")
    raise CustomException(e, sys)


STAGE_NAME = "Model Evaluation"

try:
    logging.info(f">>>>>> stage '{STAGE_NAME}' started <<<<<<")

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

    logging.info(f">>>>>> stage '{STAGE_NAME}' completed <<<<<<\n")
    logging.info(">>>>>> Rural Credit Predictor Pipeline completed <<<<<<")

except Exception as e:
    logging.error(f"Error occurred while running {STAGE_NAME}!")
    raise CustomException(e, sys)