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
    root_dir: Path
    processed_data: str
    database: str
    raw_collection: str
    processed_collection: str


@dataclass(frozen=True)
class DataValidationConfig:
    root_dir: Path
    database: str
    raw_collection: str
    processed_collection: str


@dataclass(frozen=True)
class DataTransformationConfig:
    root_dir: Path
    database: str
    processed_collection: str
    random_state: int
    data_transformer: Path


@dataclass(frozen=True)
class ModelTrainingConfig:
    root_dir: Path
    test_size: float
    random_state: int
    hyperparameters: dict
    experiment_name: str
    model_path: Path


@dataclass(frozen=True)
class ModelEvaluationConfig:
    root_dir: Path
    data_transformer: Path
    model_path: Path
    train_metrics: Path
    test_metrics: Path

