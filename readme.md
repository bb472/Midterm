# Advanced Python Calculator for Software Engineering Graduate Course

This project entails the creation of a sophisticated calculator application built in Python, designed as part of a graduate course. The primary focus is on applying professional software development methodologies, featuring well-structured and maintainable code, implementation of design patterns, robust logging mechanisms, dynamic configuration through environment variables, effective data management using Pandas, and an interactive command-line interface (REPL) for real-time engagement.


# Getting Started

**Prerequisites:**
- Python 3.7 or higher
- pytest for running tests


**Installation:**

1. **Clone the repository:**:
```
git clone https://github.com/bb472/Midterm.git
cd Midterm-project
```
2. **Create a virtual environment (optional but recommended):**:
```
python3 -m venv projectenv
source projectenv/bin/activate  # On Windows: projectenv\Scripts\activate
```

3. **Install the dependencies:**:
```
pip install -r requirements.txt

```

4. **Set up environment variables:**: Create a .env file in the project root and define any necessary variables, such as:

- ENVIRONMENT=PRODUCTION
- PLUGIN_FILE_PATH=plugins
- PRODUCT_FILE_PATH=data/books.csv

# Usage Examples

1. **Run the application:**:

```
python main.py

```


2. **Basic commands:**:
- Add: ``` add 4 1 ```
- Subtract: ``` subtract 13 4 ```
- Divide: ``` divide 12 2 ```
- Exit: ``` exit ```
- View history: ``` history ```
- Save history: ``` save_history ```
- Load history: ``` load_history ```
- Clear history: ``` clear_history ```
- Delete history record:``` delete_history_record <index> ```
- Menu: ``` menu ```


# Calculator Class

The Calculator class handles basic arithmetic operations and tracks calculation history using the DataFrameFacade. Each operation is logged into the history and stored for future reference.

# History Management

"The DataFrameFacade class handles calculation history with a Pandas DataFrame, enabling the addition, saving, loading, and clearing of history records."


# Design Patterns Used:
1. **Facade Pattern:**: Implemented in the DataFrameFacade class to simplify interactions with the history management functionalities. This pattern hides the complexities of the underlying operations (like adding, saving, loading, and clearing history) and provides a simplified interface.

Code: (https://github.com/bb472/Midterm.git/calculator/__init__.py)

2. **Singleton Pattern:**: Utilized in the CommandsFactory class to guarantee that a single instance oversees command registration and execution, ensuring consistent behavior throughout the application.

Code: (https://github.com/bb472/Midterm.git/commands/__init__.py)

3. **Factory Method:**: The Factory Method pattern is applied in the CommandsFactory class, which dynamically loads and registers command plugins during runtime. This enables flexible integration of new commands by creating subclasses of the Command base class without altering existing code, improving scalability and maintainability.

Code: (https://github.com/bb472/Midterm.git/commands/__init__.py)


# Environment Variables

Environment Variables: The python-dotenv library is used to load environment variables for managing configurations like logging levels and plugin paths. This approach keeps sensitive data out of the codebase and enables easy configuration changes without modifying the code.

Link to Code: (https://github.com/bb472/Midterm.git/.env)

```
load_dotenv()
self.settings = self.load_environment_variables()

```

# Logging Strategy
Logging Implementation: Logging is set up during application startup to monitor user interactions and errors. It utilizes a logging configuration file (logging.conf) or falls back to a basic configuration. Log messages offer insights into operational processes and encountered errors, facilitating debugging and monitoring.

```

    def configure_logging(self):
        """Configure logging settings from a file or set basic configuration."""
        logging_conf_path = 'logging.conf'
        if os.path.exists(logging_conf_path):
            logging.config.fileConfig(logging_conf_path, disable_existing_loggers=False)
        else:
            logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.info("Logging configured.")

```
# Error Handling
The application implements two approaches for error handling:

**Easier to Ask for Forgiveness than Permission (EAFP):** Assumes operations will succeed and handles exceptions if they occur.

**Example:**: This code attempts to convert input arguments to floats and logs an error if the conversion fails. It then checks if the operation exists in the command handler and executes it, logging any errors that arise during execution.


```python

try:
          
    arg1, arg2 = args
    arg1, arg2 = float(arg1), float(arg2)  # Convert inputs to numbers
except ValueError:
    logging.error("Invalid arguments for arithmetic operation. Arguments must be numbers.")

elif operation in self.command_handler.commands.keys():
    try:
        self.command_handler.commands[operation].execute(*arguments)
    except Exception as e:
        logging.error("Error executing command '%s': %s", operation, e)

```

**Look Before You Leap (LBYL):** Uses condition checks before performing actions (e.g., verifying command arguments).

**Example:**: This code checks if exactly two arguments are provided and logs an error if not. It then attempts to convert the arguments to floats and performs the specified arithmetic operation, logging an error for invalid inputs or unknown operations.

```python
        if len(args) != 2:
             logging.error("please enter 2 arguments ")
             
        else : 
            try:
                a, b = args
                a, b = float(a), float(b)  # Convert inputs to numbers
            except ValueError:
                logging.error("Invalid arguments for arithmetic operation. Arguments must be numbers.")

            if operation == "add":
                return self.add(a, b)
            elif operation == "subtract":
                return self.subtract(a, b)
            elif operation == "multiply":
                return self.multiply(a, b)
            elif operation == "divide":
                return self.divide(a, b)  # Handle division here
            else:
                logging.error(f"Unknown operation: {operation}")


Code: [app.py](https://github.com/bb472/Midterm.git/calculator.py)

```

