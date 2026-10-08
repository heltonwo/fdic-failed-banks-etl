"""Extract step: downloads the FDIC bank failures CSV."""

import pandas as pd

URL = "https://fdic.gov/bank-failures/download-data.csv"


def extract_fdic_data() -> pd.DataFrame:
    """Download the FDIC bank failures CSV into a DataFrame."""
    print("Loading FDIC data directly into memory...")

    # The FDIC file is not UTF-8 encoded
    df = pd.read_csv(URL, encoding="ISO-8859-1")

    print(f"Data loaded successfully! Total rows: {len(df)}")
    return df


if __name__ == "__main__":
    extract_fdic_data()