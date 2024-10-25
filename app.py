"""
Command-line calculator with REPL functionality, 
supporting arithmetic operations, 
plugins, and logging.
"""
import logging
import logging.config
import os
import sys
from dotenv import load_dotenv  # Third-party import
from calculator import Calculator  # First-party import
from commands import CommandsFactory  # First-party import

class App:
    """Main application class for the command-line calculator with REPL functionality."""    
    def __init__(self):
        os.makedirs('logs', exist_ok=True)  # Ensure 'logs' directory exists
        self.configure_logging()  # Set up logging
        load_dotenv()  # Load environment variables from a .env file
        self.settings = self.load_environment_variables()
        self.calculator = Calculator()  # Initialize calculator instance
        self.command_handler = CommandsFactory()  # Initialize command handler for plugins

    def configure_logging(self):
        """Configure logging settings from a file or set basic configuration."""
        logging_conf_path = 'logging.conf'
        if os.path.exists(logging_conf_path):
            logging.config.fileConfig(logging_conf_path, disable_existing_loggers=False)
        else:
            # Default logging configuration
            logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.info("Logging configured.")

    def load_environment_variables(self):
        """Load and return environment variables as a dictionary."""
        settings = {key: value for key, value in os.environ.items()}
        logging.info("Environment variables loaded.")
        return settings

    def get_environment_variable(self, env_var: str = 'ENVIRONMENT'):
        """Return the value of the specified environment variable."""
        return self.settings.get(env_var, None)

    def repl(self):
        """Run the Read-Eval-Print Loop (REPL) for user input and command processing."""
        while True:
            try:
                user_input = input(">>> ").strip()
                if not user_input:  # Skip empty input
                    logging.warning("No command entered.")
                    continue

                user_input_parts = user_input.split()
                operation = user_input_parts[0]
                arguments = user_input_parts[1:]

                # Handle 'exit' and 'menu' commands
                if operation.lower() == 'exit':
                    logging.info("Exiting the calculator.")
                    print("Exiting the calculator.")
                    sys.exit(0)
                if operation.lower() == 'menu':
                    self.show_menu()
                    continue

                # Check for valid arithmetic and history commands
                if operation in self.get_supported_commands():
                    result = self.calculator.execute(operation, *arguments)
                    if result is not None:
                        print(f"Result: {result}")
                # Handle plugin commands
                elif operation in self.command_handler.commands:
                    self.execute_plugin_command(operation, *arguments)
                else:
                    logging.error("Unknown command: %s", operation)
                    print(f"No such command: unknown_command")

            except Exception as e:
                logging.error("Unexpected error: %s", e)
                print(f"An unexpected error occurred: {e}")

    def show_menu(self):
        """Display available commands to the user."""
        available_commands = self.get_supported_commands() + self.command_handler.all_plugins()
        print("Available commands:")
        for cmd in available_commands:
            print(f" - {cmd}")
        logging.info("Displayed available commands.")

    def get_supported_commands(self):
        """Return a list of supported arithmetic and history commands."""
        return ['add', 'subtract', 'multiply', 'divide', 'save_history', 'load_history', 'clear_history', 'delete_history_record']

    def execute_plugin_command(self, operation, *arguments):
        """Execute a plugin command."""
        try:
            self.command_handler.commands[operation].execute(*arguments)
            logging.info("Executed plugin command: %s", operation)
        except Exception as e:
            logging.error("Error executing command '%s': %s", operation, e)
            print(f"Error: Failed to execute '{operation}'. {e}")

    def start(self):
        """Initialize the calculator, load plugins, and start the REPL."""
        plugin_file_path = os.getenv("PLUGIN_FILE_PATH")
        if plugin_file_path:
            self.command_handler.import_plugins(plugin_file_path)
            logging.info("Plugins loaded from: %s", plugin_file_path)
        else:
            logging.warning("No plugin file path specified in environment variables.")

        logging.info("Calculator REPL started.")
        logging.info("Type 'exit' to exit.")
        logging.info("Type 'menu' to get available commands.")
        self.repl()
