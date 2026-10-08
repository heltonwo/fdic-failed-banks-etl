"""Transform step: cleans the raw data and adds date-derived columns."""

import pandas as pd


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """Return a cleaned copy of the raw DataFrame with month, year and quarter columns."""
    print("Starting data transformation...")
    df_clean = df.copy()

    # Standardize column names (e.g. 'Bank Name' -> 'bank_name')
    df_clean.columns = df_clean.columns.str.strip().str.lower().str.replace(" ", "_")

    # Parse dates like "25-Sep-26"; invalid values become NaT instead of failing
    df_clean["closing_date"] = pd.to_datetime(
        df_clean["closing_date"], format="%d-%b-%y", errors="coerce"
    )

    df_clean["closing_month"] = df_clean["closing_date"].dt.month
    df_clean["closing_year"] = df_clean["closing_date"].dt.year
    df_clean["closing_quarter"] = df_clean["closing_date"].dt.quarter

    # Quick validation of the transformed data
    print("\nShape:")
    print(df_clean.shape)
    print("\nColumns:")
    print(df_clean.columns.tolist())
    print("\nData types:")
    print(df_clean.dtypes)
    print("\nFirst rows:")
    print(df_clean.head())

    return df_clean