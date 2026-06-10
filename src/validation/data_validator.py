import pandas as pd

def check_duplicates(df: pd.DataFrame, dataset_name: str) -> None:
    duplicate_count = df.duplicated().sum()

    print(f"{dataset_name.title()} Duplicate Check")
    print(f"Duplicate Rows: {duplicate_count}")
    print("-" * 50)

def check_missing_values(df: pd.DataFrame, dataset_name: str) -> None:
    missing_values = df.isnull().sum().sum()

    print(f"{dataset_name.title()} Missing Values Check")
    print(f"Missing Values: {missing_values}")
    print("-" * 50)

def check_referential_integrity(
        source_df: pd.DataFrame,
        reference_df: pd.DataFrame,
        source_column: str,
        reference_column: str,
        source_name: str,
        reference_name: str
) -> None:
    """
    Check whether values in one dataset exist in another dataset.
    """

    source_values = set(source_df[source_column].dropna())
    reference_values = set(reference_df[reference_column].dropna())

    invalid_values = source_values - reference_values

    print(f"{source_name.title()} → {reference_name.title()} Integrity Check")
    print(f"Source Column: {source_column}")
    print(f"Reference Column: {reference_column}")
    print(f"Invalid References: {len(invalid_values)}")

    if invalid_values:
        print("Invalid Values Found:")
        for value in sorted(invalid_values):
            print(f"- {value}")

    print("-" * 50)