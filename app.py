"""Command-line calculator with REPL functionality, supporting arithmetic operations, plugins, and logging."""
import logging
import logging.config
import os
import sys


class App:
    """Main application class for the command-line calculator with REPL functionality."""
    def __init__(self):
        os.makedirs('logs', exist_ok=True)
        self.configure_logging()
     

    def configure_logging(self):
        """Configure logging settings from a file or set basic configuration."""
        logging_conf_path = 'logging.conf'
        if os.path.exists(logging_conf_path):
            logging.config.fileConfig(logging_conf_path, disable_existing_loggers=False)
        else:
            logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.info("Logging configured.")


    def repl(self):
        """Run the Read-Eval-Print Loop (REPL) for user input and command processing."""
        while True:
            # try:
                user_input = input(">>> ").strip()
                user_input_parts = user_input.split()
                if len(user_input_parts) == 0:
                    logging.warning("No command entered.")
                    continue  # Skip iteration if no input

    

    def start(self):   
      
        self.repl()



app = App()
app.start()