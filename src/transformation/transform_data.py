import pandas as pd


def create_control_reporting_dataset(
    controls_df: pd.DataFrame,
    issues_df: pd.DataFrame,
    assessments_df: pd.DataFrame,
    applications_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Create a reporting-ready dataset by combining controls,
    issues, assessments, and application data.
    """

    controls_with_apps = controls_df.merge(
        applications_df,
        on="Application ID",
        how="left",
        suffixes=("", "_application")
    )

    issues_summary = issues_df.groupby("Control ID").agg(
        Total_Issues=("Issue ID", "count"),
        Open_Issues=("Issue Status", lambda x: (x == "Open").sum()),
        Critical_Issues=("Severity", lambda x: (x == "Critical").sum())
    ).reset_index()

    assessments_summary = assessments_df.groupby("Control ID").agg(
        Total_Assessments=("Assessment ID", "count"),
        Failed_Assessments=("Test Result", lambda x: (x == "Fail").sum())
    ).reset_index()

    reporting_df = controls_with_apps.merge(
        issues_summary,
        on="Control ID",
        how="left"
    )

    reporting_df = reporting_df.merge(
        assessments_summary,
        on="Control ID",
        how="left"
    )

    reporting_df[
        [
            "Total_Issues",
            "Open_Issues",
            "Critical_Issues",
            "Total_Assessments",
            "Failed_Assessments"
        ]
    ] = reporting_df[
        [
            "Total_Issues",
            "Open_Issues",
            "Critical_Issues",
            "Total_Assessments",
            "Failed_Assessments"
        ]
    ].fillna(0)

    print("Transformation completed successfully.")
    print(f"Reporting Dataset Shape: {reporting_df.shape}")

    return reporting_df