import threading
from typing import Callable, Dict

from rich.console import Console


class Command:
    """
    Represents a command that can be executed in the console.
    """
    def __init__(self, name: str, description: str, function: Callable[..., None]):
        self.name: str = name
        self.description: str = description
        self.function: Callable[..., None] = function

    def __call__(self, *args, **kwargs) -> None:
        return self.function(*args, **kwargs)


class CommandConsole:
    """
    Console for running commands in a separate thread.
    """
    # Thread stuff
    is_running: bool
    _console_thread: threading.Thread

    _console: Console
    commands: Dict[str, Command]

    def __init__(self):
        self.is_running = False
        self._console_thread = threading.Thread(target=self._run_console, daemon=True)
        self._console = Console()

        self.commands = {
            "help": Command("help", "Display this help message.", self.help),
            "exit": Command("exit", "Exit the console.", lambda: exit(0)),
            # Add more commands here as needed
        }

    def start(self):
        self._console_thread.start()

    def stop(self):
        self.is_running = False
        if self._console_thread.is_alive():
            self._console_thread.join()

    def _run_console(self):
        if self.is_running:
            self._console.print("[yellow]Console is already running, ending new thread.")
            return

        self.is_running = True
        while self.is_running:
            try:
                self._interpret_input(input("> ").strip())
            except EOFError:
                self._console.print("[red]Console input ended.[/red]")
                self.is_running = False

    def _interpret_input(self, line: str):
        if len(line) == 0:
            return

        args = line.split()

        if args[0].lower() in self.commands:
            command = self.commands[args[0].lower()]
            try:
                command(*args[1:])
            except Exception as e:
                self._console.print(f"[red]Error[/]: [yellow]{e}[/]")

    # region Command Methods
    def help(self, *args):
        """Display this help message."""
        self._console.print("[bold]Available commands:[/]")
        for name, command in self.commands.items():
            self._console.print(f"[green]{name}[/]: {command.description}")

    # endregion
