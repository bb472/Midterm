"""
Module for testing the Calculator and DataFrameFacade classes.

This module contains pytest fixtures for setting up test environments 
and various test cases to validate the functionality of the Calculator 
and DataFrameFacade classes, ensuring operations like addition, subtraction, 
history management, and persistence are working as expected.
"""
import os  # Standard library imports
import pytest  # Third-party imports
from calculator import Calculator, DataFrameFacade  # Local application imports


# Helper function to reset the history file for test isolation
def reset_history_file():
    """Remove the history file if it exists to ensure test isolation."""
    history_file = "calcHistory.csv"
    if os.path.exists(history_file):
        os.remove(history_file)

# Fixture to create a fresh instance of Calculator for each test
@pytest.fixture
def calc_fixture():
    """Provide a fresh instance of Calculator with a reset history file."""
    reset_history_file()  # Ensure no pre-existing history
    return Calculator()
@pytest.fixture
def h_facade():
    """Provide a fresh instance of DataFrameFacade with a reset history file."""
    reset_history_file()
    return DataFrameFacade()

### Tests for the Calculator class ###

def test_add(calc_fixture):
    """Test the addition functionality of the Calculator."""
    assert calc_fixture.add(2, 3) == 5
    assert calc_fixture.add(-1, 1) == 0
    assert "Added 2 + 3 = 5" in calc_fixture.show_history()

def test_subtract(calc_fixture):
    """Test the subtraction functionality of the Calculator."""
    assert calc_fixture.subtract(5, 3) == 2
    assert calc_fixture.subtract(-3, -2) == -1
    assert "Subtracted 5 - 3 = 2" in calc_fixture.show_history()

def test_multiply(calc_fixture):
    """Test the multiplication functionality of the Calculator."""
    assert calc_fixture.multiply(3, 4) == 12
    assert calc_fixture.multiply(0, 10) == 0
    assert "Multiplied 3 * 4 = 12" in calc_fixture.show_history()

def test_divide(calc_fixture):
    """Test the division functionality of the Calculator."""
    assert calc_fixture.divide(10, 2) == 5
    assert calc_fixture.divide(-10, 5) == -2
    assert "Divided 10 / 2 = 5.0" in calc_fixture.show_history()

def test_divide_by_zero(calc_fixture):
    """Test that dividing by zero raises a ValueError."""
    with pytest.raises(ValueError, match="Cannot divide by zero."):
        calc_fixture.divide(10, 0)

def test_show_history(calc_fixture):
    """Test the history display functionality of the Calculator."""
    calc_fixture.add(1, 2)
    calc_fixture.multiply(3, 4)
    history = calc_fixture.show_history()
    assert "Added 1 + 2 = 3" in history
    assert "Multiplied 3 * 4 = 12" in history

def test_clearHistory(calc_fixture):
    """Test clearing the history in the Calculator."""
    calc_fixture.add(1, 1)
    calc_fixture.clearHistory()
    assert calc_fixture.show_history() == "No history available."

def test_deleteHistoryRecord(calc_fixture):
    """Test deleting a specific history record in the Calculator."""
    calc_fixture.add(1, 1)
    calc_fixture.add(2, 2)
    assert calc_fixture.deleteHistoryRecord(1) == "Deleted record: Added 2 + 2 = 4"
    assert "Added 2 + 2 = 4" not in calc_fixture.show_history()

def test_delete_invalid_index(calc_fixture):
    """Test attempting to delete an invalid history record index."""
    calc_fixture.add(1, 1)
    assert calc_fixture.deleteHistoryRecord(5) == "Invalid index. No record deleted."

def test_save_and_loadHistory(calc_fixture):
    """Test saving and loading the calculation history."""
    calc_fixture.add(5, 5)
    calc_fixture.saveHistory()
    assert os.path.exists("calcHistory.csv")

    # Create a new instance to test loading
    new_calc = Calculator()
    loaded_history = new_calc.loadHistory()
    assert "Added 5 + 5 = 10" in loaded_history