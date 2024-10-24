"""
RandomQuote module.

This module defines the RandomQuote class, which is a plugin for the 
Command framework. It provides functionality to display a random quote.
"""
import logging
import random
from commands import Command

class RandomQuote(Command):
    """A plugin that displays a random quote."""
    command_name = "quote"

    quotes = [
        "The only way to do great work is to love what you do. – Steve Jobs",
        "Life is what happens when you're busy making other plans. – John Lennon",
        "Get busy living or get busy dying. – Stephen King",
        "You only live once, but if you do it right, once is enough. – Mae West",
        "To be yourself in a world that is constantly trying to make you something else is the greatest accomplishment. – Ralph Waldo Emerson",
    ]
    @staticmethod
    def execute():
        """Execute the quote command to display a random quote."""
        quote = random.choice(RandomQuote.quotes)
        print("Quote of the Day:", quote)
        logging.info("Displayed quote: %s", quote)
