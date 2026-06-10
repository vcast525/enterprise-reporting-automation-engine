from pathlib import Path
import pandas as pd

from src.utils.logger import (
    setup_logger
)

from src.reporting.generate_report import (
    generate_executive_report,
    generate_exception_report
)

from src.validation.data_validator import (
    check_duplicates,
    check_missing_values,
    check_referential_integrity
)

from src.transformation.transform_data import (
    create_control_reporting_dataset
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
logger = setup_logger(PROJECT_ROOT)
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw"

SOURCE_FILES = {
    "controls": "Control_Inventory.xlsx",
    "issues": "Issues_Report.xlsx",
    "assessments": "Assessment_Results.xlsx",
    "applications": "Application_Inventory.xlsx",
}

def load_excel_file(file_name: str) -> pd.DataFrame:
    """
    Load a single Excel file from the data/raw folder.
    """

    file_path = RAW_DATA_PATH / file_name

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    df = pd.read_excel(file_path)

    print(f"Loaded {file_name}: {df.shape[0]} rows, {df.shape[1]} columns")

    return df

def load_all_source_files() -> dict[str, pd.DataFrame]:
    """
    Load all source Excel files into pandas DataFrames.
    """
    dataframes = {}

    for dataset_name, file_name in SOURCE_FILES.items():
        dataframes[dataset_name] = load_excel_file(file_name)

    return dataframes

if __name__ == "__main__":
    print("Starting data ingestion...")
    logger.info("Pipeline execution started.")
    print(f"Project Root: {PROJECT_ROOT}")
    print(f"Raw Data Path: {RAW_DATA_PATH}")
    print("-" * 60)

    source_data = load_all_source_files()
    logger.info("Source files loaded successfully.")

    for dataset_name, dataframe in source_data.items():
        check_duplicates(
            dataframe,
            dataset_name
        )

        check_missing_values(
            dataframe,
            dataset_name
        )

    # ---------------------------
    # Referential Integrity Checks
    # ---------------------------

    controls_df = source_data["controls"]
    issues_df = source_data["issues"]
    assessments_df = source_data["assessments"]
    applications_df = source_data["applications"]

    print("-" * 60)
    print("Running referential integrity checks...")
    print("-" * 60)

    check_referential_integrity(
        source_df=issues_df,
        reference_df=controls_df,
        source_column="Control ID",
        reference_column="Control ID",
        source_name="issues",
        reference_name="controls"
    )

    check_referential_integrity(
        source_df=assessments_df,
        reference_df=controls_df,
        source_column="Control ID",
        reference_column="Control ID",
        source_name="assessments",
        reference_name="controls"
    )

    check_referential_integrity(
        source_df=controls_df,
        reference_df=applications_df,
        source_column="Application ID",
        reference_column="Application ID",
        source_name="controls",
        reference_name="applications"
    )

    print("-" * 60)
    print("Data ingestion and validation completed successfully.")
    logger.info("Validation completed successfully.")
    print("-" * 60)
    print("Running data transformation...")

    reporting_df = create_control_reporting_dataset(
        controls_df=controls_df,
        issues_df=issues_df,
        assessments_df=assessments_df,
        applications_df=applications_df
    )
    print(reporting_df.head())
    logger.info(
        f"Transformation completed. Reporting dataset shape: {reporting_df.shape}"
    )

    print("-" * 60)
    print("Generating executive report...")
    print("-" * 60)

    OUTPUT_DATA_PATH = PROJECT_ROOT / "data" / "output"

    executive_report_path = (
            OUTPUT_DATA_PATH / "Executive_Report.xlsx"
    )

    generate_executive_report(
        reporting_df=reporting_df,
        output_path=executive_report_path
    )
    logger.info("Executive report generated successfully.")

    print("-" * 60)
    print("Generating exception report...")
    print("-" * 60)

    exception_report_path = (
            OUTPUT_DATA_PATH / "Exception_Report.xlsx"
    )

    generate_exception_report(
        reporting_df=reporting_df,
        output_path=exception_report_path
    )

    logger.info("Exception report generated successfully.")

    PROCESSED_DATA_PATH = PROJECT_ROOT / "data" / "processed"
    PROCESSED_DATA_PATH.mkdir(parents=True, exist_ok=True)

    processed_file_path = PROCESSED_DATA_PATH / "Control_Reporting_Dataset.xlsx"

    reporting_df.to_excel(
        processed_file_path,
        index=False
    )

    print(f"Processed dataset saved to: {processed_file_path}")
    logger.info(f"Processed dataset saved successfully: {processed_file_path}")

    print("-" * 60)
    logger.info("Pipeline completed successfully.")
    print("Data ingestion, validation, transformation, reporting, and exception reporting completed successfully.")

    for dataset_name, dataframe in source_data.items():
        print(f"{dataset_name.title()}: {dataframe.shape}")