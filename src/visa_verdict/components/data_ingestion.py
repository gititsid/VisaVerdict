import os
import urllib.request as request
from pathlib import Path

import pandas as pd

from src.visa_verdict.logger import logging
from src.visa_verdict.utils.common import get_size

from src.visa_verdict.utils.monogdb_utilities import *
from src.visa_verdict.config.configuration import ConfigurationManager
from src.visa_verdict.entity.config_entity import DataIngestionConfig


class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def download_data(self):
        if not os.path.exists(self.config.raw_data_path):
            filename, headers = request.urlretrieve(
                url=self.config.remote_url,
                filename=self.config.raw_data_path
            )
            logging.info(f"{filename} download! with following info: \n{headers}")
        else:
            logging.info(f"File already exists of size: {get_size(Path(self.config.raw_data_path))}")

    def _get_raw_data_as_dict(self) -> list[dict]:
        df = pd.read_csv(self.config.raw_data_path)
        data = df.to_dict(orient="records")
        return data

    def ingest_data(self):
        data = self._get_raw_data_as_dict()
        logging.info("Ingesting data to database")
        mongodb = MongoDBUtilities(
            db_name=self.config.database,
            collection_name=self.config.raw_collection
        )
        mongodb.insert_many(data)
        logging.info(f"Data ingested successfully! Total records: {len(data)}")

    def main(self):
        self.download_data()
        self.ingest_data()


if __name__ == "__main__":
    config = ConfigurationManager().get_data_ingestion_config()
    data_ingestion = DataIngestion(config)
    data_ingestion.main()
