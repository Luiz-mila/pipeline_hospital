import os
import logging

logger = logging.getLogger(__name__)


def validate_file(file_path: str) -> bool:
    """
    Validates that the CSV file exists and is not empty.
    Returns True if valid, raises an exception if not.
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    file_size = os.path.getsize(file_path)

    if file_size == 0:
        raise ValueError(f"File is empty: {file_path}")

    size_mb = file_size / (1024 * 1024)
    logger.info(f"File validated: {file_path} ({size_mb:.1f} MB)")

    return True