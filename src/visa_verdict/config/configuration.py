from src.visa_verdict.constants import *
from src.visa_verdict.utils.common import read_yaml, create_directories

from src.visa_verdict.entity.config_entity import (DataIngestionConfig,
                                                   DataPreprocessingConfig,
                                                   DataValidationConfig)


class ConfigurationManager:
    def __init__(
        self,
        config_filepath=CONFIG_FILE_PATH
    ):
        self.config = read_yaml(config_filepath)

        create_directories([self.config.artifacts_root])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        data_ingestion_config = self.config.data_ingestion

        create_directories([data_ingestion_config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir=data_ingestion_config.root_dir,
            remote_url=data_ingestion_config.remote_url,
            raw_data_path=data_ingestion_config.raw_data_path,
            database=data_ingestion_config.database,
            raw_collection=data_ingestion_config.raw_collection
        )

        return data_ingestion_config

    def get_data_preprocessing_config(self) -> DataPreprocessingConfig:
        data_preprocessing_config = self.config.data_preprocessing

        create_directories([data_preprocessing_config.root_dir])

        data_preprocessing_config = DataPreprocessingConfig(
            root_dir=data_preprocessing_config.root_dir,
            processed_data=data_preprocessing_config.processed_data,
            database=data_preprocessing_config.database,
            raw_collection=data_preprocessing_config.raw_collection,
            processed_collection=data_preprocessing_config.processed_collection
        )

        return data_preprocessing_config

    def get_data_validation_config(self) -> DataValidationConfig:
        data_validation_config = self.config.data_validation

        create_directories([data_validation_config.root_dir])

        data_validation_config = DataValidationConfig(
            root_dir=data_validation_config.root_dir,
            database=data_validation_config.database,
            raw_collection=data_validation_config.raw_collection,
            processed_collection=data_validation_config.processed_collection
        )

        return data_validation_config
