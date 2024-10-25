"""
calculator module
This module provides a calculator class that performs basic arithmetic operations
and manages a history of calculations using a Pandas DataFrame. The history can 
be saved to and loaded from a CSV file, and users can view, clear, or delete 
specific records from the history.
"""
import logging
import os
import pandas as pd
from commands import Command

class Calculator(Command):
    """The main calculator class that performs basic arithmetic operations and manages plugins."""
    def __init__(self):
        self.data_frame_facade = DataFrameFacade()    
    def execute(self, operation, *args):
        """Execute a specific operation based on the command provided."""
        if operation in ['save_history', 'load_history', 'clear_history', 'delete_history_record']:
                if operation == "save_history":
                    return self.save_history()
                if operation == "load_history":
                    return self.load_history()
                if operation == "clear_history":
                    return self.clear_history()
                if operation == "delete_history_record":
                    print("delete_history_record")
                    if len(args) == 1 and args[0].isdigit():
                        return self.delete_history_record(int(args[0]))
                    logging.error("Invalid index provided for delete_history_record.")
        if len(args) != 2:
             logging.error("please enter 2 arguments ")             
        try:
            arg1, arg2 = args
            arg1, arg2 = float(arg1), float(arg2)  # Convert inputs to numbers
        except ValueError:
            logging.error("Invalid arguments for arithmetic operation. Arguments must be numbers.")
            return
        if operation == "add":
            return self.add( arg1, arg2)
        if operation == "subtract":
            return self.subtract( arg1, arg2)
        if operation == "multiply":
            return self.multiply( arg1, arg2)
        if operation == "divide":
            try:
                result = self.divide(arg1, arg2)
                return result
            except ZeroDivisionError:
                logging.error("Division by zero error.")
                print("Error: Division by zero is not allowed.")
                return
        logging.error("Unknown operation: %s", operation)
    def add(self, a, b):
        """Return the sum of a and b."""
        result = a + b
        entry = f"Added {a} + {b} = {result}"
        self.data_frame_facade.add_entry(entry)
        logging.info(entry)
        print(entry)
        return result
    def subtract(self, a, b):
        """Return the result of a minus b."""
        result = a - b
        entry = f"Subtracted {a} - {b} = {result}"
        self.data_frame_facade.add_entry(entry)
        logging.info(entry)
        print(entry)
        return result
    def multiply(self, a, b):
        """Return the product of a and b."""
        result = a * b
        entry = f"Multiplied {a} * {b} = {result}"
        self.data_frame_facade.add_entry(entry)
        logging.info(entry)
        print(entry)
        return result
    def divide(self, a, b):
        """Return the result of a divided by b, or handle division by zero."""
        if b == 0.0:
            logging.error("Division by zero attempted.")
            print("Cannot divide by zero.")
            raise ValueError("Cannot divide by zero.")
        result = a / b
        entry = f"Divided {a} / {b} = {result}"
        self.data_frame_facade.add_entry(entry)
        logging.info(entry)
        return result
    def show_history(self):
        """Show the current calculation history."""
        return self.data_frame_facade.show_history()
    def save_history(self):
        """Save the current history to a CSV file."""
        self.data_frame_facade.save_history()
        return "History saved."
    def load_history(self):
        """Load history from a CSV file and return it as a string."""
        loaded_history = self.data_frame_facade.load_history()
        if not loaded_history.empty:
            logging.info(loaded_history.to_string(index=False))
            return loaded_history.to_string(index=False)
        return "No history found."
    def clear_history(self):
        """Clear the current calculation history."""
        self.data_frame_facade.clear_history()
        return "History cleared."
    def delete_history_record(self, index):
        """Delete a specific record from the history."""
        return self.data_frame_facade.delete_entry(index)
class DataFrameFacade:
    """Facade class for managing history using Pandas DataFrame."""    
    def __init__(self, history_file="calcHistory.csv"):
        self.history_file = history_file
        self.history_df = pd.DataFrame(columns=["Calculation"])  # Initialize an empty DataFrame
        if os.path.exists(self.history_file):
            self.history_df = pd.read_csv(self.history_file)
        else:
            self.save_history()  # Create an empty history file if it doesn't exist
    def add_entry(self, entry):
        """Add a new entry to the history DataFrame."""
        new_entry = {"Calculation": entry}
        self.history_df = pd.concat([self.history_df, pd.DataFrame([new_entry])], ignore_index=True)
    def delete_entry(self, index):
        """Delete a specific entry by index."""
        if len(self.history_df) == 0:
            logging.info("empty dataframe")
            return "Invalid index. No record deleted."  # Return directly if empty
        if 0 <= index < len(self.history_df):
            deleted_record = self.history_df.iloc[index]
            self.history_df = self.history_df.drop(index).reset_index(drop=True)
            self.history_df.to_csv(self.history_file, index=False)
            logging.info("Deleted record: %s", deleted_record['Calculation'])
            return f"Deleted record: {deleted_record['Calculation']}"
        logging.error("Invalid index provided for deletion.")
        return "Invalid index. No record deleted."
    def save_history(self):
        """Save the DataFrame to a CSV file."""
        self.history_df.to_csv(self.history_file, index=False)
        logging.info("History saved to '%s'.", self.history_file)
    def load_history(self):
        """Load the history from a CSV file."""
        if os.path.exists(self.history_file):
            self.history_df = pd.read_csv(self.history_file)
            logging.info("History loaded from '%s'.", self.history_file)
            return self.history_df
        logging.warning("No history file found.")
        return pd.DataFrame(columns=["Calculation"])  # Return empty DataFrame if file not found
    def clear_history(self):
        """Clear the history DataFrame."""
        self.history_df = pd.DataFrame(columns=["Calculation"])
        self.history_df.to_csv(self.history_file, index=False)
        logging.info("History cleared.")
    def show_history(self):
        """Return a string representation of the current history."""
        if not self.history_df.empty:
            return self.history_df.to_string(index=False)
        return "No history available."
