import os
import sys
from pathlib import Path

from box.exceptions import BoxValueError
from box import ConfigBox

import pickle
import json
import yaml
import numpy as np
from pandas import DataFrame

from functools import wraps

from src.visa_verdict.logger import logging
from src.visa_verdict.exception import CustomException


def exception_handler(func: callable) -> callable:
    """
    This function is used to handle exceptions. It wraps the function and catches any exception raised by the function.
    To be used as a decorator.

    Args:
        func: Function to be wrapped.

    Returns:
        callable: Wrapped function.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            raise CustomException(e, sys)
    return wrapper


def log_handler(func: callable) -> callable:
    """
    This function is used to log the function name, arguments and keyword arguments before and after the function is
    executed.
    To be used as a decorator.

    Args:
        func: Function to be wrapped.

    Returns:
        callable: Wrapped function.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f"Calling function '{func.__name__}' with args: {args}, kwargs: {kwargs}")
        result = func(*args, **kwargs)
        logging.info(f"Function '{func.__name__}' executed successfully!")
        return result
    return wrapper


def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """reads yaml file and returns

    Args:
        path_to_yaml (str): path like input

    Raises:
        ValueError: if yaml file is empty
        e: empty file

    Returns:
        ConfigBox: ConfigBox type
    """
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logging.info(f"yaml file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e


def write_yaml(file_path: str, content: object, replace: bool = False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as e:
        raise CustomException(e, sys)


def write_json(file_path: str, content: object, replace: bool = False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            json.dump(content, file, indent=4)
    except Exception as e:
        raise CustomException(e, sys)


def load_object(file_path: str):
    logging.info("Entered the load_object method of utils")

    try:

        with open(file_path, "rb") as file_obj:
            obj = pickle.load(file_obj)

        logging.info("Exited the load_object method of utils")

        return obj

    except Exception as e:
        raise CustomException(e, sys) from e


def save_numpy_array_data(file_path: str, array: np.array):
    """
    Save numpy array data to file
    file_path: str location of file to save
    array: np.array data to save
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise CustomException(e, sys) from e


def load_numpy_array_data(file_path: str) -> np.array:
    """
    load numpy array data from file
    file_path: str location of file to load
    return: np.array data loaded
    """
    try:
        with open(file_path, 'rb') as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise CustomException(e, sys) from e


def save_object(file_path: str, obj: object) -> None:
    logging.info("Entered the save_object method of utils")

    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)

        logging.info("Exited the save_object method of utils")

    except Exception as e:
        raise CustomException(e, sys) from e


def drop_columns(df: DataFrame, cols: list) -> DataFrame:
    """
    drop the columns form a pandas DataFrame
    df: pandas DataFrame
    cols: list of columns to be dropped
    """
    logging.info("Entered drop_columns method of utils")

    try:
        df = df.drop(columns=cols, axis=1)

        logging.info("Exited the drop_columns method of utils")

        return df
    except Exception as e:
        raise CustomException(e, sys) from e


def create_directories(dirs: list) -> None:
    """
    Create directories if they do not exist
    dirs: list of directories to be created
    """
    logging.info("Entered create_directories method of utils")

    try:
        for directory in dirs:
            os.makedirs(directory, exist_ok=True)

        logging.info("Exited the create_directories method of utils")

    except Exception as e:
        raise CustomException(e, sys) from e


def get_size(path: Path) -> str:
    """get size in KB

    Args:
        path (Path): path of the file

    Returns:
        str: size in KB
    """
    size_in_kb = round(os.path.getsize(path)/1024)
    return f"~ {size_in_kb} KB"
