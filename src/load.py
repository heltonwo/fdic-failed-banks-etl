"""Load step: writes the transformed data to PostgreSQL."""

import pandas as pd

from src.db import get_engine


def load_data(df: pd.DataFrame) -> None:
    """Write the DataFrame to the `failed_banks` table."""
    engine = get_engine()

    # Full reload: the table is recreated on every run
    df.to_sql("failed_banks", con=engine, if_exists="replace", index=False)

    print("Data loaded successfully!")