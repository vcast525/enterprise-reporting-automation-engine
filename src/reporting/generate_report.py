from pathlib import Path
import pandas as pd


def generate_executive_report(
    reporting_df: pd.DataFrame,
    output_path: Path
) -> None:
    """
    Generate an executive reporting workbook with summary,
    control health, and exception report tabs.
    """

    output_path.parent.mkdir(parents=True, exist_ok=True)

    executive_summary = pd.DataFrame({
        "Metric": [
            "Total Controls",
            "Total Issues",
            "Open Issues",
            "Critical Issues",
            "Total Assessments",
            "Failed Assessments"
        ],
        "Value": [
            reporting_df["Control ID"].nunique(),
            reporting_df["Total_Issues"].sum(),
            reporting_df["Open_Issues"].sum(),
            reporting_df["Critical_Issues"].sum(),
            reporting_df["Total_Assessments"].sum(),
            reporting_df["Failed_Assessments"].sum()
        ]
    })

    control_health = reporting_df.copy()

    exceptions = reporting_df[
        (reporting_df["Open_Issues"] > 0) |
        (reporting_df["Critical_Issues"] > 0) |
        (reporting_df["Failed_Assessments"] > 0)
    ].copy()

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        executive_summary.to_excel(
            writer,
            sheet_name="Executive Summary",
            index=False
        )

        control_health.to_excel(
            writer,
            sheet_name="Control Health",
            index=False
        )

        exceptions.to_excel(
            writer,
            sheet_name="Exceptions",
            index=False
        )

    print(f"Executive report generated successfully: {output_path}")

def generate_exception_report(
    reporting_df: pd.DataFrame,
    output_path: Path
) -> None:
    """
    Generate a standalone exception report for controls requiring attention.
    """

    output_path.parent.mkdir(parents=True, exist_ok=True)

    exceptions_df = reporting_df[
        (reporting_df["Open_Issues"] > 0) |
        (reporting_df["Critical_Issues"] > 0) |
        (reporting_df["Failed_Assessments"] > 0)
    ].copy()

    exception_summary = pd.DataFrame({
        "Metric": [
            "Total Controls Reviewed",
            "Controls With Exceptions",
            "Total Open Issues",
            "Total Critical Issues",
            "Total Failed Assessments"
        ],
        "Value": [
            reporting_df["Control ID"].nunique(),
            exceptions_df["Control ID"].nunique(),
            exceptions_df["Open_Issues"].sum(),
            exceptions_df["Critical_Issues"].sum(),
            exceptions_df["Failed_Assessments"].sum()
        ]
    })

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        exception_summary.to_excel(
            writer,
            sheet_name="Exception Summary",
            index=False
        )

        exceptions_df.to_excel(
            writer,
            sheet_name="Exception Details",
            index=False
        )

    print(f"Exception report generated successfully: {output_path}")