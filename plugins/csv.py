"""
Csv module.

This module defines the Csv class, which is a plugin for the 
Command framework. It provides functionality to read and display 
data from a specified CSV file.
"""
import logging
import os
import pandas as pd  
from commands import Command
class Csv(Command):
    """A plugin that displays data from a CSV file."""

    @staticmethod
    def execute():
        """Execute the data command to display contents of a CSV file."""
        filename = os.getenv("PRODUCT_FILE_PATH")
        try:
            df = pd.read_csv(filename)
            logging.info(df)     
            print(df.to_string())        
            logging.info("Displayed data from CSV file: %s", filename)
        except FileNotFoundError:
            print(f"Error: The file '{filename}' was not found.")
            logging.error("File not found: %s", filename)
        except Exception as e:
            print("Error reading the CSV file:", e)
            logging.error("Error reading CSV file %s: %s", filename, e)
