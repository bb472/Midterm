import pytest
from app import App

@pytest.fixture
def app():
    """Fixture for creating an instance of the App."""
    return App()

def test_app_get_environment_variable():
    app = App()
#   Retrieve the current environment setting
    current_env = app.get_environment_variable('ENVIRONMENT')
    # Assert that the current environment is what you expect
    assert current_env in ['DEVELOPMENT', 'TESTING', 'PRODUCTION'], f"Invalid ENVIRONMENT: {current_env}"

def test_app_start_exit_command(capfd, monkeypatch):
    """Test that the REPL exits correctly on 'exit' command."""
    # Simulate user entering 'exit'
    monkeypatch.setattr('builtins.input', lambda _: 'exit')
    app = App()
    with pytest.raises(SystemExit) as e:
        app.start()
    assert e.type == SystemExit

def test_app_start_unknown_command(capfd, monkeypatch):
    """Test how the REPL handles an unknown command before exiting."""
    # Simulate user entering an unknown command followed by 'exit'
    inputs = iter(['unknown_command', 'exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    app = App()
    with pytest.raises(SystemExit):
        app.start()
    # Verify that the unknown command was handled as expected
    captured = capfd.readouterr()
    assert "No such command: unknown_command" in captured.out

def test_menu(app, monkeypatch, capsys):
    """Test the menu command."""
    # Simulate user entering 'menu' followed by 'exit'
    inputs = iter(['menu', 'exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    app = App()
    # Run the REPL
    with pytest.raises(SystemExit):
        app.start()

    # Capture the printed output
    captured = capsys.readouterr()
    
    # Check if the expected output is present
    assert "Available commands:" in captured.out

def test_save_history(app, monkeypatch, capsys):
    """Test the save_history command."""
    # Add something to the calculator's history first
    app.calculator.add(1, 2)  # Assuming add method works as expected
    inputs = iter(['save_history', 'exit'])  # Simulate entering 'save_history' and then 'exit'
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    with pytest.raises(SystemExit):
        app.start()

    # Capture the printed output
    captured = capsys.readouterr()
    assert "History saved." in captured.out

def test_delete_history_record(app, monkeypatch, capsys):
    """Test the delete_history_record command."""
    app.calculator.add(1, 2)  # Add something to the history
    app.calculator.save_history()  # Save it first
    inputs = iter(['delete_history_record 0', 'exit'])  
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with pytest.raises(SystemExit):
        app.start()
    # Capture the printed output
    captured = capsys.readouterr()
    assert "Deleted record:" in captured.out  

def test_add(app, monkeypatch, capsys):
    """Test the add command."""
    monkeypatch.setattr('builtins.input', lambda _: 'add 2 3')
    inputs = iter(['add 2 3', 'exit'])  
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with pytest.raises(SystemExit):
        app.start()
    # Capture the printed output
    captured = capsys.readouterr()
    assert "Result: 5.0" in captured.out  

def test_subtract(app, monkeypatch, capsys):
    """Test the subtract command."""
    monkeypatch.setattr('builtins.input', lambda _: 'subtract 5 3')
    inputs = iter(['subtract 5 3', 'exit'])  
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with pytest.raises(SystemExit):
        app.start()
    # Capture the printed output
    captured = capsys.readouterr()
    assert "Result: 2.0" in captured.out 


def test_multiply(app, monkeypatch, capsys):
    """Test the multiply command."""
    monkeypatch.setattr('builtins.input', lambda _: 'multiply 2 3')
    inputs = iter(['multiply 2 3', 'exit'])  
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    with pytest.raises(SystemExit):
        app.start()

    # Capture the printed output
    captured = capsys.readouterr()
    assert "Result: 6.0" in captured.out 


def test_divide(app, monkeypatch, capsys):
    """Test the divide command."""
    monkeypatch.setattr('builtins.input', lambda _: 'divide 6 3')
    inputs = iter(['divide 6 3', 'exit'])  
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with pytest.raises(SystemExit):
        app.start()
    # Capture the printed output
    captured = capsys.readouterr()
    assert "Result: 2.0" in captured.out  


