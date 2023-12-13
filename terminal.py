from rich.console import Console
from rich import print as rich_print

console = Console()

def styled_print(message, style):
    rich_print(style + message)


def info(message):
    styled_print(message, "[bold purple]")


def success(message):
    styled_print(message, "[bold green]")


def error(message):
    styled_print(message, "[bold red]")


def input_prompt(message):
    return console.input(f"[bold cyan]{message}[/bold cyan]")
