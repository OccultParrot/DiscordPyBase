import atexit

import discord

from src.command_console import CommandConsole


class Root:
    command_console: CommandConsole
    bot: discord.client

    def __init__(self):
        self. command_console = CommandConsole()
        
        # Register the exit handler
        atexit.register(self.exit())

    def start(self):
        pass
    
    def exit(self):
        """
        Exit the application.
        """
        self.command_console.stop()
        # Add any additional cleanup if necessary
        print("Exiting application.")
        exit(0)
