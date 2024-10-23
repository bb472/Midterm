"""Command-line calculator with REPL functionality, supporting arithmetic operations, plugins, and logging."""
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
        os.makedirs('logs', exist_ok=True)
        self.configure_logging()
        load_dotenv()
        self.settings = self.load_environment_variables()
        self.calculator = Calculator()
        self.command_handler = CommandsFactory()

    def configure_logging(self):
        """Configure logging settings from a file or set basic configuration."""
        logging_conf_path = 'logging.conf'
        if os.path.exists(logging_conf_path):
            logging.config.fileConfig(logging_conf_path, disable_existing_loggers=False)
        else:
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
            # try:
                user_input = input(">>> ").strip()
                user_input_parts = user_input.split()
                if len(user_input_parts) == 0:
                    logging.warning("No command entered.")
                    continue  # Skip iteration if no input

                operation = user_input_parts[0]
                arguments = user_input_parts[1:]
                
                if operation not in self.command_handler.all_plugins() +  ['add', 'subtract', 'multiply', 'divide',"menu","loadHistory", "saveHistory", "clearHistory", "deleteHistoryRecord","exit","menu"]:
                    logging.error("No such command: unknown_command %s", user_input)
                    sys.exit(1) 

                if user_input.lower() == 'exit':
                    logging.info("Exiting the calculator.")
                    print("Exiting the calculator.")
                    sys.exit(0)
                if user_input.lower() == 'menu':
                    logging.info("Available commands:")
                    logging.info(self.command_handler.all_plugins()+['add', 'subtract', 'multiply', 'divide',"saveHistory","loadHistory","delete history_record","clearHistory"])
                
     
                if operation in ['add', 'subtract', 'multiply', 'divide',"saveHistory","loadHistory","deleteHistoryRecord","clearHistory"] :
                    result =  self.calculator.execute(operation, *arguments)
                    print(f"Result: {result}")

                # Handle plugin commands
                elif operation in self.command_handler.commands.keys():
                    try:
                        self.command_handler.commands[operation].execute(*arguments)
                    except Exception as e:
                        logging.error("Error executing command '%s': %s", operation, e)
                        print(f"Error: Failed to execute '{operation}'. {e}")

                

    def start(self):   
        """Initialize the calculator, load plugins, and start the REPL.""" 
        self.command_handler.import_plugins(os.getenv("PLUGIN_FILE_PATH"))
        logging.info(self.command_handler.commands)
        logging.info("Calculator REPL started.")
        logging.info("Type 'exit' to exit.")
        logging.info("Type 'menu' to get available commands.")
        logging.info("Available history commands: loadHistory, saveHistory, clearHistory, deleteHistoryRecord <index>.")
        self.repl()



app = App()
app.start()