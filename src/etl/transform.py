import pandas as pd
import logging

logger = logging.getLogger(__name__)


def transform_hospital_records(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates new columns from existing data.
    Returns a transformed DataFrame.
    """

    df = df.copy()

    # --- charge_cost_ratio ---
    # How much the hospital charged vs what it actually cost
    df["charge_cost_ratio"] = df["Total Charges"] / df["Total Costs"]
    logger.info("Created column: charge_cost_ratio")

    # --- length_of_stay_numeric ---
    # "120+" is text — replace with 120 and convert to integer
    df["length_of_stay_numeric"] = (
        df["Length of Stay"]
        .astype(str)
        .str.replace("+", "", regex=False)
        .pipe(pd.to_numeric, errors="coerce")
    )
    logger.info("Created column: length_of_stay_numeric")

    # --- is_emergency ---
    # "Y" → True, anything else → False
    df["is_emergency"] = df["Emergency Department Indicator"] == "Y"
    logger.info("Created column: is_emergency")

    logger.info(f"Transformation complete. Shape: {df.shape}")

    return df