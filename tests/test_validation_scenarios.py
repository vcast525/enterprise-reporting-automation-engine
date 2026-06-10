import pandas as pd

def test_duplicate_row_detection():

    test_df = pd.DataFrame({
        "Control ID": ["CTRL-1001", "CTRL-1001", "CTRL-1002"],
        "Control Name": ["Access Review", "Access Review", "Backup Review"]
    })

    duplicate_count = test_df.duplicated().sum()

    assert duplicate_count == 1

def test_no_duplicate_rows():

    test_df = pd.DataFrame({
        "Control ID": ["CTRL-1001", "CTRL-1002", "CTRL-1003"]
    })

    duplicate_count = test_df.duplicated().sum()

    assert duplicate_count == 0

def test_missing_value_detection():

    test_df = pd.DataFrame({
        "Control ID": ["CTRL-1001", None, "CTRL-1003"]
    })

    missing_count = test_df.isnull().sum().sum()

    assert missing_count == 1

def test_no_missing_values():

    test_df = pd.DataFrame({
        "Control ID": ["CTRL-1001", "CTRL-1002", "CTRL-1003"]
    })

    missing_count = test_df.isnull().sum().sum()

    assert missing_count == 0