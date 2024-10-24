"""
Greet module.

This module defines the Greet class, which is a plugin for the 
Command framework. It provides functionality to greet users by 
printing specified arguments along with a greeting message.
"""
import logging
from commands import Command

class Greet(Command):
    """An example plugin that provides additional functionality."""
    @staticmethod
    def execute():
        """Execute the greet command with two arguments."""
        print("Hello World")
        logging.info("Hello World")
