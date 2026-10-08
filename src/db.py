"""Database connection helper, shared by the ETL pipeline and the dashboard."""

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL, Engine

load_dotenv()

REQUIRED_VARS = ["DB_USER", "DB_PASSWORD", "DB_HOST", "DB_PORT", "DB_NAME"]


def get_engine() -> Engine:
    """Build a SQLAlchemy engine from environment variables.

    Raises:
        ValueError: If any required variable is missing.
    """
    missing = [v for v in REQUIRED_VARS if not os.getenv(v)]
    if missing:
        raise ValueError(f"Missing environment variables: {', '.join(missing)}")

    # URL.create handles special characters in the password safely
    url = URL.create(
        drivername="postgresql+psycopg2",
        username=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        host=os.environ["DB_HOST"],
        port=int(os.environ["DB_PORT"]),
        database=os.environ["DB_NAME"],
    )
    return create_engine(url)