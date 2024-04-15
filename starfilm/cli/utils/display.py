import os
from rich.console import Console


def app_title() -> None:
    """Display app title in console
    """
    
    # Instancing the console
    console = Console()
    
    # Displaying title in console
    console.print(r""" _____ _            ______ _ _           
/  ___| |           |  ___(_) |          
\ `--.| |_ __ _ _ __| |_   _| |_ __ ___  
 `--. \ __/ _` | '__|  _| | | | '_ ` _ \ 
/\__/ / || (_| | |  | |   | | | | | | | |
\____/ \__\__,_|_|  \_|   |_|_|_| |_| |_|""", 
    style='cyan', highlight=False)


def goodbye(on_new_line: bool = True) -> None:
    """Display goodby message in console

    Args:
        on_new_line (bool, optional): Skipping a line before the message. Defaults to True.
    """
    
    # Instancing the console
    console = Console()
    
    # If on new line, skipping a line
    if on_new_line:
        console.print()
    
    # Displaying goodby message in console
    console.print("👋 Goodbye!", style='green')
    console.print("\n❌ Quitting...\n", style='red')


def menu_title(title: str, on_new_line: bool = True) -> None:
    """Display given menu title in console

    Args:
        title (str): Menu title
        on_new_line (bool, optional): Skipping a line before the title. Defaults to True.
    """
    
    # Instancing the console
    console = Console(highlight=False)
    
    # If on new line, skipping a line
    if on_new_line:
        console.print()
        
    # Displaying menu title in console
    console.print(f"{title}:", style="yellow", )
    
    
def section_title(title: str, on_new_line: bool = True) -> None:
    """Display given section title in console

    Args:
        title (str): Section title
        on_new_line (bool, optional): Skipping a line before the title. Defaults to True.
    """    
    
    # Instancing the console
    console = Console(highlight=False)
    
    # If on new line, skipping a line
    if on_new_line:
        console.print()
        
    # Displaying section title in console
    console.print(f"{title}:", style="magenta")
    
    
def clear() -> None:
    """Clear the console
    """
    
    # Clearing the console
    os.system('cls' if os.name == 'nt' else 'clear')