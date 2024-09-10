from datetime import date

from src.visa_verdict.utils.monogdb_utilities import *
from src.visa_verdict.config.configuration import ConfigurationManager
from src.visa_verdict.entity.config_entity import DataPreprocessingConfig


class DataPreprocessing:
    def __init__(self, config: DataPreprocessingConfig):
        self.config = config

    def preprocess_data(self):
        raw_client = MongoDBUtilities(
            db_name=self.config.database,
            collection_name=self.config.raw_collection
        )

        raw_df = raw_client.read_all_as_df()

        # Perform data preprocessing
        todays_date = date.today()
        current_year = todays_date.year

        raw_df['company_age'] = current_year - raw_df['yr_of_estab']
        processed_df = raw_df.drop(['yr_of_estab', 'case_id'], axis=1)

        # save processed data as csv
        processed_df.to_csv(self.config.processed_data, index=False)

        processed_client = MongoDBUtilities(
            db_name=self.config.database,
            collection_name=self.config.processed_collection
        )

        processed_client.insert_many(processed_df.to_dict(orient="records"))

    def main(self):
        self.preprocess_data()


if __name__ == "__main__":
    config = ConfigurationManager().get_data_preprocessing_config()
    data_preprocessing = DataPreprocessing(config)
    data_preprocessing.main()
