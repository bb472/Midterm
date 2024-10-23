import importlib
import logging
import os
import inspect

class Command:
    """Base class for all plugins. Each plugin must implement the execute method."""
    def execute(self, *args):
        """Execute the plugin command with given arguments."""
        raise NotImplementedError("Plugin must implement the execute method.")

class CommandsFactory:
    """Class to manage loading plugins dynamically."""

    def __init__(self):
        """Initialize instance attributes."""
        self.commands = {}

    def register_command(self, command_name: str, command: Command):
        """Register a command with a given name.

        Args:
            command_name (str): The name of the command to register.
            command (Command): The command instance to associate with the command name.
        """
        self.commands[command_name] = command

    def execute_command(self, command_name: str):
        """Easier to ask for forgiveness than 
           permission (EAFP) - 
           Use when it's most likely to work."""
        try:
            self.commands[command_name].execute() 
            # depends on command_name calling the concrete command class
        except KeyError:
            logging.error("No such command: %s", command_name)

    def import_plugins(self, plugins_directory):
        """Dynamically load plugins from the specified directory."""
        for filename in os.listdir(plugins_directory):
            if filename.endswith(".py") and not filename.startswith("_"):
                module_name = filename[:-3]  # remove .py extension
                module = importlib.import_module(f"plugins.{module_name}")
                # Register each class that inherits from Command
                for _, cls in inspect.getmembers(module, inspect.isclass):
                    if issubclass(cls, Command) and cls is not Command:
                        # used to identify the arguments
                        self.create_plugin(module_name, cls())

    def create_plugin(self, command_name, plugin):
        """Register a new plugin and its commands."""
        if isinstance(plugin, Command):
            logging.info("Plugin '%s' registered successfully.", plugin.__class__.__name__)
            self.commands[command_name] = plugin

    def all_plugins(self):
        """List all available plugin commands."""
        return list(self.commands.keys())
