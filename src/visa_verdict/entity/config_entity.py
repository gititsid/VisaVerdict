from pathlib import Path
from dataclasses import dataclass


@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    remote_url: str
    raw_data_path: Path
    database: str
    raw_collection: str


@dataclass(frozen=True)
class DataPreprocessingConfig:
    database: str
    raw_collection: str
    processed_collection: str
