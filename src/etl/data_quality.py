import pandas as pd
import logging

logger = logging.getLogger(__name__)


def check_data_quality(df: pd.DataFrame) -> dict:
    """
    Analyzes the DataFrame and returns a quality report.
    """

    report = {}

    # Total rows and columns
    report["total_rows"] = df.shape[0]
    report["total_columns"] = df.shape[1]

    # Null counts per column
    null_counts = df.isnull().sum()
    report["null_counts"] = null_counts[null_counts > 0].to_dict()

    # Data types per column
    report["dtypes"] = df.dtypes.astype(str).to_dict()

    # Check if financial columns are numeric
    financial_cols = ["Total Charges", "Total Costs"]
    report["financial_cols_dtype"] = {
        col: str(df[col].dtype)
        for col in financial_cols
        if col in df.columns
    }

    logger.info(f"Total rows: {report['total_rows']}")
    logger.info(f"Total columns: {report['total_columns']}")
    logger.info(f"Columns with nulls: {list(report['null_counts'].keys())}")
    logger.info(f"Financial columns dtypes: {report['financial_cols_dtype']}")

    return report