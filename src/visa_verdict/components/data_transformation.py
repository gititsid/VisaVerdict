import sys
import pickle
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler, OrdinalEncoder, PowerTransformer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from imblearn.combine import SMOTETomek, SMOTEENN

from src.visa_verdict.utils.monogdb_utilities import *
from src.visa_verdict.config.configuration import ConfigurationManager
from src.visa_verdict.entity.config_entity import DataTransformationConfig

from src.visa_verdict.logger import logging
from src.visa_verdict.exception import CustomException


class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config

        self.processed_client = MongoDBUtilities(
            db_name=self.config.database,
            collection_name=self.config.processed_collection
        )

        self.processed_data = self.processed_client.read_all_as_df()

        self.num_features = ['no_of_employees', 'prevailing_wage', 'company_age']
        self.or_columns = ['has_job_experience', 'requires_job_training', 'full_time_position', 'education_of_employee']
        self.oh_columns = ['continent', 'unit_of_wage', 'region_of_employment']
        self.transform_columns = ['no_of_employees', 'company_age']

    def _get_data_transformer(self):
        try:
            logging.info("Setting up data transformer:")

            numeric_transformer = StandardScaler()
            oh_transformer = OneHotEncoder()
            ordinal_encoder = OrdinalEncoder()
            transform_pipe = Pipeline(
                steps=[
                    (
                        'transformer', PowerTransformer(method='yeo-johnson')
                    )
                ]
            )

            preprocessor = ColumnTransformer(
                [
                    ("OneHotEncoder", oh_transformer, self.oh_columns),
                    ("Ordinal_Encoder", ordinal_encoder, self.or_columns),
                    ("Transformer", transform_pipe, self.transform_columns),
                    ("StandardScaler", numeric_transformer, self.num_features)
                ]
            )

            logging.info("Data transformer set up successfully!")

            return preprocessor

        except Exception as e:
            logging.error(f"Error occurred in setting up data transformer!")
            raise CustomException(e, sys)

    def get_transformed_data(self):
        try:
            logging.info("Transforming data")

            x = self.processed_data.drop(['_id', 'case_status'], axis=1)

            y = self.processed_data['case_status']
            y = np.where(y == 'Denied', 1, 0)

            preprocessor = self._get_data_transformer()

            x = preprocessor.fit_transform(x)
            x, y = SMOTEENN(random_state=self.config.random_state, sampling_strategy='minority').fit_resample(x, y)

            with open(self.config.data_transformer, 'wb') as file:
                pickle.dump(preprocessor, file)

            logging.info("Data transformed successfully")

            return x, y

        except Exception as e:
            logging.error(f"Error occurred in transforming data")
            raise CustomException(e, sys)

    def main(self):
        try:
            x, y = self.get_transformed_data()
            return x, y
        except Exception as e:
            logging.error(f"Error occurred in transforming data")
            raise CustomException(e, sys)


if __name__ == '__main__':
    config = ConfigurationManager().get_data_transformation_config()
    data_transformer = DataTransformation(config)

    x, y = data_transformer.main()

    print(
        f"Shape of x: {x.shape}\n"
        f"Shape of y: {y.shape}"
    )
