"""
Unit tests for the Csv plugin in the calculator project.
This module contains test cases that verify the behavior of the Csv plugin's
execute method, including successful execution, handling of missing files, and
generic exception handling.
"""
import logging
import pandas as pd
from plugins.csv import Csv

# Test case for successfully reading the CSV file
def test_data_plugin_execute_success(monkeypatch, capfd, caplog, tmpdir):
    """Test the execute method when the CSV file exists and is readable."""
    # Create a temporary CSV file with sample content using pandas
    test_csv = tmpdir.join("books.csv")
    df = pd.DataFrame({
        'Title': ['The Great Gatsby', '1984'],
        'Author': ['F. Scott Fitzgerald', 'George Orwell']
    })
    df.to_csv(test_csv, index=False)

    # Set the environment variable to point to the temp CSV file
    monkeypatch.setenv("PRODUCT_FILE_PATH", str(test_csv))

    # Capture the log output
    with caplog.at_level(logging.INFO):
        # Execute the data command
        Csv.execute()

        # Capture the printed output
        out, _ = capfd.readouterr()

        # Verify the printed output contains CSV data
        assert "The Great Gatsby" in out
        assert "1984" in out
        assert "F. Scott Fitzgerald" in out
        assert "George Orwell" in out

        # Verify the log output
        assert f"Displayed data from CSV file: {test_csv}" in caplog.text
# Test case for FileNotFoundError
def test_data_plugin_execute_file_not_found(monkeypatch, capfd, caplog):
    """Test the execute method when the CSV file does not exist."""
    # Set an invalid path for the environment variable
    monkeypatch.setenv("PRODUCT_FILE_PATH", "invalid/path/to/books.csv")    
    # Capture the log output
    with caplog.at_level(logging.ERROR):
        # Execute the data command
        Csv.execute()
        # Capture the printed output
        out, _ = capfd.readouterr()
        # Verify the error message is printed
        assert "Error: The file 'invalid/path/to/books.csv' was not found." in out
        # Verify the log output
        assert "File not found: invalid/path/to/books.csv" in caplog.text
# Test case for generic Exception
def test_data_plugin_execute_exception(monkeypatch, capfd, caplog):
    """Test the execute method when an unexpected exception occurs."""    
    # Set the environment variable to a directory instead of a file to trigger an exception
    monkeypatch.setenv("PRODUCT_FILE_PATH", "/")    
    # Capture the log output
    with caplog.at_level(logging.ERROR):
        # Execute the data command
        Csv.execute()

        # Capture the printed output
        out, _ = capfd.readouterr()

        # Verify the generic error message is printed
        assert "Error reading the CSV file:" in out

        # Verify the log output
        assert "Error reading CSV file /" in caplog.text
