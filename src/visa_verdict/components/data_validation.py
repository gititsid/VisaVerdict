import sys

from src.visa_verdict.utils.monogdb_utilities import *
from src.visa_verdict.config.configuration import ConfigurationManager
from src.visa_verdict.entity.config_entity import DataValidationConfig

from src.visa_verdict.logger import logging
from src.visa_verdict.exception import CustomException


class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config

    def validate_data(self):
        raw_client = MongoDBUtilities(
            db_name=self.config.database,
            collection_name=self.config.raw_collection
        )

        processed_client = MongoDBUtilities(
            db_name=self.config.database,
            collection_name=self.config.processed_collection
        )
        try:
            logging.info("Performing Data Validation...")

            raw_df = raw_client.read_all_as_df()
            processed_df = processed_client.read_all_as_df()

            # Perform data validation:
            # Check if raw/processed collection is empty
            valid_raw_data = not raw_df.empty
            valid_processed_data = not processed_df.empty

            # Check if all unique _id in raw collection exists in processed collection
            raw_ids = sorted(raw_df['_id'].unique().tolist())
            processed_ids = sorted(processed_df['_id'].unique().tolist())
            all_rows_exist = raw_ids == processed_ids

            if valid_raw_data and valid_processed_data and all_rows_exist:
                logging.info("Data Validation Passed!")
                return True
            else:
                logging.error(
                    "Data Validation Failed. Status: valid_raw_data: {}, valid_processed_data: {}, all_rows_exist: {}"
                    .format(
                        valid_raw_data,
                        valid_processed_data,
                        all_rows_exist
                    )
                )
                raise CustomException("Data Validation Failed!", sys)

        except Exception as e:
            logging.error(f"Error occurred during Data Validation! Error: {e}")
            raise CustomException(e, sys)

    def main(self):
        self.validate_data()


if __name__ == "__main__":
    config = ConfigurationManager().get_data_validation_config()
    data_validation = DataValidation(config)
    data_validation.main()
