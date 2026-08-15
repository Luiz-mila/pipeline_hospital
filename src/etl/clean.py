import pandas as pd
import logging

logger = logging.getLogger(__name__)


def clean_hospital_records(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the hospital records DataFrame.
    Returns a cleaned DataFrame.
    """

    df = df.copy()

    # --- Fix financial columns ---
    # They came as text like "$12,345.00" — strip $ and commas, then convert to float
    financial_cols = ["Total Charges", "Total Costs"]
    for col in financial_cols:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace("$", "", regex=False)
                .str.replace(",", "", regex=False)
                .str.strip()
            )
            df[col] = pd.to_numeric(df[col], errors="coerce")
            logger.info(f"Converted '{col}' to numeric.")

    # --- Fill nulls in payment columns ---
    payment_cols = [
        "Payment Typology 1",
        "Payment Typology 2",
        "Payment Typology 3",
    ]
    for col in payment_cols:
        if col in df.columns:
            df[col] = df[col].fillna("Not Provided")
            logger.info(f"Filled nulls in '{col}' with 'Not Provided'.")

    # --- Fill nulls in provider columns ---
    provider_cols = [
        "Attending Provider License Number",
        "Operating Provider License Number",
        "Other Provider License Number",
    ]
    for col in provider_cols:
        if col in df.columns:
            df[col] = df[col].fillna("Unknown")
            logger.info(f"Filled nulls in '{col}' with 'Unknown'.")

    logger.info(f"Cleaning complete. Shape: {df.shape}")

    return df