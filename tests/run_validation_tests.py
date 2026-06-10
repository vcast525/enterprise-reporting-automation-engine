from pathlib import Path
import pandas as pd


def run_test(test_name: str, actual_value: int, expected_value: int) -> dict:
    status = "PASS" if actual_value == expected_value else "FAIL"

    return {
        "Test Name": test_name,
        "Expected": expected_value,
        "Actual": actual_value,
        "Status": status
    }


def main():
    test_results = []

    duplicate_df = pd.DataFrame({
        "Control ID": ["CTRL-1001", "CTRL-1001", "CTRL-1002"],
        "Control Name": ["Access Review", "Access Review", "Backup Review"]
    })

    test_results.append(
        run_test(
            "Duplicate Row Detection",
            duplicate_df.duplicated().sum(),
            1
        )
    )

    no_duplicate_df = pd.DataFrame({
        "Control ID": ["CTRL-1001", "CTRL-1002", "CTRL-1003"]
    })

    test_results.append(
        run_test(
            "No Duplicate Rows",
            no_duplicate_df.duplicated().sum(),
            0
        )
    )

    missing_value_df = pd.DataFrame({
        "Control ID": ["CTRL-1001", None, "CTRL-1003"]
    })

    test_results.append(
        run_test(
            "Missing Value Detection",
            missing_value_df.isnull().sum().sum(),
            1
        )
    )

    no_missing_value_df = pd.DataFrame({
        "Control ID": ["CTRL-1001", "CTRL-1002", "CTRL-1003"]
    })

    test_results.append(
        run_test(
            "No Missing Values",
            no_missing_value_df.isnull().sum().sum(),
            0
        )
    )
    # --------------------------------------------------
    # Referential Integrity Test: Invalid Control ID
    # --------------------------------------------------

    issues_test_df = pd.DataFrame({
        "Issue ID": ["ISS-2001", "ISS-2002"],
        "Control ID": ["CTRL-1001", "CTRL-9999"]
    })

    controls_reference_df = pd.DataFrame({
        "Control ID": ["CTRL-1001", "CTRL-1002"]
    })

    invalid_control_ids = set(
        issues_test_df["Control ID"]
    ) - set(
        controls_reference_df["Control ID"]
    )

    test_results.append(
        run_test(
            "Invalid Control ID Detection",
            len(invalid_control_ids),
            1
        )
    )

    # --------------------------------------------------
    # Referential Integrity Test: No Invalid Control IDs
    # --------------------------------------------------

    valid_issues_test_df = pd.DataFrame({
        "Issue ID": ["ISS-2001", "ISS-2002"],
        "Control ID": ["CTRL-1001", "CTRL-1002"]
    })

    valid_control_ids = set(
        valid_issues_test_df["Control ID"]
    ) - set(
        controls_reference_df["Control ID"]
    )

    test_results.append(
        run_test(
            "No Invalid Control IDs",
            len(valid_control_ids),
            0
        )
    )

    # --------------------------------------------------
    # Referential Integrity Test: Invalid Application ID
    # --------------------------------------------------

    controls_test_df = pd.DataFrame({
        "Control ID": ["CTRL-1001", "CTRL-1002"],
        "Application ID": ["APP-4001", "APP-9999"]
    })

    applications_reference_df = pd.DataFrame({
        "Application ID": ["APP-4001", "APP-4002"]
    })

    invalid_application_ids = set(
        controls_test_df["Application ID"]
    ) - set(
        applications_reference_df["Application ID"]
    )

    test_results.append(
        run_test(
            "Invalid Application ID Detection",
            len(invalid_application_ids),
            1
        )
    )

    # --------------------------------------------------
    # Referential Integrity Test: No Invalid Application IDs
    # --------------------------------------------------

    valid_controls_test_df = pd.DataFrame({
        "Control ID": ["CTRL-1001", "CTRL-1002"],
        "Application ID": ["APP-4001", "APP-4002"]
    })

    valid_application_ids = set(
        valid_controls_test_df["Application ID"]
    ) - set(
        applications_reference_df["Application ID"]
    )

    test_results.append(
        run_test(
            "No Invalid Application IDs",
            len(valid_application_ids),
            0
        )
    )
    results_df = pd.DataFrame(test_results)

    print("\nVALIDATION TEST RESULTS")
    print("=" * 60)
    print(results_df.to_string(index=False))
    print("=" * 60)

    passed = (results_df["Status"] == "PASS").sum()
    failed = (results_df["Status"] == "FAIL").sum()

    print(f"Passed: {passed}")
    print(f"Failed: {failed}")

    project_root = Path(__file__).resolve().parents[1]

    output_data_path = project_root / "data" / "output"
    output_data_path.mkdir(parents=True, exist_ok=True)

    output_path = output_data_path / "Validation_Test_Results.xlsx"

    print("\nSaving validation test report to:")
    print(output_path)

    results_df.to_excel(
        output_path,
        index=False
    )

    print(f"\nValidation test report saved successfully: {output_path}")

if __name__ == "__main__":
    main()