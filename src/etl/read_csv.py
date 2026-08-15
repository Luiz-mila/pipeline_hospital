import pandas as pd
import logging

logger = logging.getLogger(__name__)


def read_hospital_records(file_path: str, nrows: int = 10000) -> pd.DataFrame:
    """
    Reads the hospital records CSV file.
    Returns a DataFrame with the first nrows rows.
    """

    logger.info(f"Reading file: {file_path} (nrows={nrows})")

    df = pd.read_csv(
        file_path,
        nrows=nrows,
        low_memory=False,
    )

    logger.info(f"File loaded: {df.shape[0]} rows x {df.shape[1]} columns")

    return df