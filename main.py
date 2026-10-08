from src.extract import extract_fdic_data
from src.transformations import transform_data
from src.load import load_data


def run_pipeline():
    print("=== STARTING ETL PIPELINE ===")

    # 1. Extract
    raw_df = extract_fdic_data()

    # 2. Transform
    clean_df = transform_data(raw_df)

    # 3. Load
    load_data(clean_df)

    print("=== PIPELINE COMPLETED SUCCESSFULLY ===")


if __name__ == "__main__":
    run_pipeline()