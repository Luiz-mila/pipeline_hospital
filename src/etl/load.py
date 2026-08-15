import pandas as pd
import logging
from sqlalchemy import create_engine

logger = logging.getLogger(__name__)

DB_CONN = "postgresql+psycopg2://airflow:airflow@postgres/airflow"
TABLE_NAME = "hospital_records"


def load_to_postgres(df: pd.DataFrame) -> None:
    """
    Loads the transformed DataFrame into PostgreSQL.
    Creates the table if it doesn't exist.
    Replaces data on each run.
    """

    engine = create_engine(DB_CONN)

    df.to_sql(
        name=TABLE_NAME,
        con=engine,
        if_exists="replace",
        index=False,
        chunksize=1000,
    )

    logger.info(f"Loaded {len(df)} rows into table '{TABLE_NAME}'.")

    engine.dispose()