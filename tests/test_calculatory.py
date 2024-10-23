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
def calc_instance():
    """Provide a fresh instance of Calculator with a reset history file."""
    reset_history_file()  # Ensure no pre-existing history
    return Calculator()
@pytest.fixture
def data_frame_facade_instance():
    """Provide a fresh instance of DataFrameFacade with a reset history file."""
    reset_history_file()
    return DataFrameFacade()

### Tests for the Calculator class ###

def test_add(calc_instance):
    """Test the addition functionality of the Calculator."""
    assert calc_instance.add(2, 3) == 5
    assert calc_instance.add(-1, 1) == 0
    assert "Added 2 + 3 = 5" in calc_instance.show_history()

def test_subtract(calc_instance):
    """Test the subtraction functionality of the Calculator."""
    assert calc_instance.subtract(5, 3) == 2
    assert calc_instance.subtract(-3, -2) == -1
    assert "Subtracted 5 - 3 = 2" in calc_instance.show_history()

def test_multiply(calc_instance):
    """Test the multiplication functionality of the Calculator."""
    assert calc_instance.multiply(3, 4) == 12
    assert calc_instance.multiply(0, 10) == 0
    assert "Multiplied 3 * 4 = 12" in calc_instance.show_history()

def test_divide(calc_instance):
    """Test the division functionality of the Calculator."""
    assert calc_instance.divide(10, 2) == 5
    assert calc_instance.divide(-10, 5) == -2
    assert "Divided 10 / 2 = 5.0" in calc_instance.show_history()

def test_divide_by_zero(calc_instance):
    """Test that dividing by zero raises a ValueError."""
    with pytest.raises(ValueError, match="Cannot divide by zero."):
        calc_instance.divide(10, 0)

def test_show_history(calc_instance):
    """Test the history display functionality of the Calculator."""
    calc_instance.add(1, 2)
    calc_instance.multiply(3, 4)
    history = calc_instance.show_history()
    assert "Added 1 + 2 = 3" in history
    assert "Multiplied 3 * 4 = 12" in history

def test_clear_history(calc_instance):
    """Test clearing the history in the Calculator."""
    calc_instance.add(1, 1)
    calc_instance.clear_history()
    assert calc_instance.show_history() == "No history available."

def test_delete_history_record(calc_instance):
    """Test deleting a specific history record in the Calculator."""
    calc_instance.add(1, 1)
    calc_instance.add(2, 2)
    assert calc_instance.delete_history_record(1) == "Deleted record: Added 2 + 2 = 4"
    assert "Added 2 + 2 = 4" not in calc_instance.show_history()

def test_delete_invalid_index(calc_instance):
    """Test attempting to delete an invalid history record index."""
    calc_instance.add(1, 1)
    assert calc_instance.delete_history_record(5) == "Invalid index. No record deleted."

def test_save_and_load_history(calc_instance):
    """Test saving and loading the calculation history."""
    calc_instance.add(5, 5)
    calc_instance.save_history()
    assert os.path.exists("calcHistory.csv")

    # Create a new instance to test loading
    new_calc = Calculator()
    loaded_history = new_calc.load_history()
    assert "Added 5 + 5 = 10" in loaded_history

### Tests for the DataFrameFacade class ###

def test_add_entry(data_frame_facade_instance):
    """Test adding an entry to the history via DataFrameFacade."""
    data_frame_facade_instance.add_entry("Test Entry")
    assert "Test Entry" in data_frame_facade_instance.show_history()

def test_save_history(data_frame_facade_instance):
    """Test saving the history via DataFrameFacade."""
    data_frame_facade_instance.add_entry("Entry to Save")
    data_frame_facade_instance.save_history()
    assert os.path.exists("calcHistory.csv")

def test_load_history(data_frame_facade_instance):
    """Test loading history entries via DataFrameFacade."""
    data_frame_facade_instance.add_entry("Entry to Load")
    data_frame_facade_instance.save_history()

    new_facade = DataFrameFacade()
    assert "Entry to Load" in new_facade.show_history()

def test_clear_history_facade(data_frame_facade_instance):
    """Test clearing the history via DataFrameFacade."""
    data_frame_facade_instance.add_entry("Clear This Entry")
    data_frame_facade_instance.clear_history()
    assert data_frame_facade_instance.show_history() == "No history available."


def test_delete_entry(data_frame_facade_instance):
    """Test deleting an entry in the history via DataFrameFacade."""
    data_frame_facade_instance.add_entry("Delete Me")
    assert data_frame_facade_instance.delete_entry(0) == "Deleted record: Delete Me"
    assert data_frame_facade_instance.show_history() == "No history available."

def test_delete_invalid_entry(data_frame_facade_instance):
    """Test attempting to delete a non-existent entry in the history."""
    assert data_frame_facade_instance.delete_entry(5) == "Invalid index. No record deleted."

# pylint: disable=redefined-outer-name
