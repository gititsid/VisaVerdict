import os
import pandas as pd
from dotenv import load_dotenv
from pymongo import MongoClient
from src.visa_verdict.logger import logging

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
        return self.collection.insert_many(data)

    def read_all_as_df(self):
        data = list(self.collection.find())
        return pd.DataFrame(data)


if __name__ == "__main__":
    mongodb = MongoDBUtilities(
        db_name="visa_verdict",
        collection_name="raw_data"
    )

    df = mongodb.read_all_as_df()
    print(df.head())
