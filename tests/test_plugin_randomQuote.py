"""
Test suite for the RandomQuote plugin.

This module contains tests for the functionality of the RandomQuote class,
ensuring that the execute method behaves as expected and outputs the correct
quotes along with appropriate logging.
"""
import logging

from plugins.random_quote import RandomQuote

# Test case for RandomQuote
def test_random_quote_plugin_execute(capfd, caplog):
    """Test the execute method of RandomQuote."""
    # Capture the log output
    with caplog.at_level(logging.INFO):
        # Execute the quote command
        RandomQuote.execute()

        # Capture the printed output
        out, _ = capfd.readouterr()

        # Verify the printed output contains "Quote of the Day"
        assert "Quote of the Day:" in out

        # Verify that the printed output is one of the quotes from the list
        assert any(quote in out for quote in RandomQuote.quotes)

        # Verify the log output contains the displayed quote
        assert any(quote in caplog.text for quote in RandomQuote.quotes)
