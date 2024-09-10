import os
import pandas as pd
from dotenv import load_dotenv
from pymongo import MongoClient
from concurrent.futures import ThreadPoolExecutor

from src.visa_verdict.logger import logging
from src.visa_verdict.exception import CustomException

# Load environment variables
load_dotenv()

# MongoDB Variables
MONGODB_CONNECTION_URL: str = os.getenv("MONGODB_CONNECTION_URL")


class MongoDBUtilities:
    def __init__(self, db_name: str, collection_name:str, connection_url: str = MONGODB_CONNECTION_URL) -> None:
        logging.info(f"Connecting to MongoDB! Database: {db_name}, Collection: {collection_name}")
        self.db_name = db_name
        self.collection_name = collection_name
        self.connection_url = connection_url

        self.client = MongoClient(self.connection_url, tls=True, tlsAllowInvalidCertificates=True)
        self.database = self.client[self.db_name]

        self.collection = self.database[self.collection_name]

        logging.info(f"Connected to MongoDB! Database: {db_name}, Collection: {collection_name}")

    def insert_one(self, data: dict):
        return self.collection.insert_one(data)

    def insert_many(self, data: list[dict]):
        try:
            logging.info(
                f"Inserting {len(data)} records to MongoDB! DB: {self.db_name}, Collection: {self.collection_name}"
            )
            load_data_to_db = self.collection.insert_many(data)
            logging.info(f"Successfully inserted {len(load_data_to_db.inserted_ids)} records to MongoDB!")
        except Exception as e:
            logging.error(f"Error inserting data to MongoDB! Error: {e}")

    def _fetch_batch(self, skip, limit):
        return list(self.collection.find().skip(skip).limit(limit))

    def read_all_as_df(self):
        try:
            logging.info(
                f"Reading all records from MongoDB! Database: {self.db_name}, Collection: {self.collection_name} ..."
            )

            # Parameters
            batch_size: int = 1000
            total_docs: int = self.collection.count_documents({})
            dataframe = pd.DataFrame()

            # Use ThreadPoolExecutor for parallel fetching
            with ThreadPoolExecutor() as executor:
                futures = [executor.submit(self._fetch_batch, i, batch_size) for i in range(0, total_docs, batch_size)]
                for future in futures:
                    batch = future.result()
                    dataframe = pd.concat([dataframe, pd.DataFrame(batch)], ignore_index=True)

            logging.info(f"Successfully read {len(dataframe)} records from MongoDB!")
            return dataframe
        except Exception as e:
            logging.error(f"Error reading data from MongoDB! Error: {e}")


if __name__ == "__main__":
    mongodb = MongoDBUtilities(
        db_name="visa_verdict",
        collection_name="raw_data"
    )

    df = mongodb.read_all_as_df()
    print(df.head())
