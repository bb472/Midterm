"""Test cases for the Greet execute method."""
import logging
from plugins.greet import Greet
# Test case for Greet
def test_greet_plugin_execute(capfd, caplog):
    """Test the execute method of Greet."""  
    # Capture the log output
    with caplog.at_level(logging.INFO):
        # Execute the greet command
        Greet.execute()

        # Capture the printed output
        out, _ = capfd.readouterr()

        # Verify the printed output
        assert "Hello World" in out
        assert "Hello World" in out

        # Verify the log output
        assert "Hello World" in caplog.text
