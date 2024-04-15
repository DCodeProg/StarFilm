import os
from rich.console import Console
from rich.table import Table

from starfilm.swapi import swapi
from .utils import *

console = Console()
CUR_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.dirname(os.path.dirname(CUR_DIR))


class CliApp:
    """Command line interface for Star Film
    """
    
    def __init__(self) -> None:
        try:
            self._app_loop()
        except KeyboardInterrupt:
            self.quit()
            
            
    def _app_loop(self) -> None:
        """App main loop
        """
        while True:
            self.main_menu()
           
    
    "MENUS FUNCTIONS"
    def show_menu(self, title: str, choices: list[tuple] | None) -> None:
        """Show the given menu and choices

        Args:
            title (str): Menu title
            choices (list[tuple] | None): Menu choices
        """
        
        # Clear the console
        display.clear()
        
        # Display the app title
        display.app_title()
        
        # Display the menu title
        display.menu_title(title)
        
        # If choices given, list the choices in console
        if choices:
            for i, choice in enumerate(choices):
                    console.print(f"{i+1}. {choice[0]}")
           
    def quit_menu(self):
        """Quit the current menu
        """
        return
        
    def menu_func(self, choices: list[tuple[str, callable]], choice: int, *args, **kwargs):
        """Call the function specified in the list of choices

        Args:
            choices (list[tuple[str, callable]]): List of choices
            choice (int): Menu choice
            *args: Arguments for the function

        Returns:
            Any: returns of the called function
        """        
        return choices[choice-1][1](*args, **kwargs)
        

    
    "MAIN MENU"
    def main_menu(self) -> None:
        """Run the main menu
        """
        
        menu_choices = [
            ("Films menu", self.films_menu),
            ("Credits", self.credits_menu),
            ("Quit", self.quit),
        ]
        
        # Display main menu
        self.show_menu('MAIN MENU', menu_choices)
        
        # Handles the choices
        choice = prompt.ask_choice(menu_choices)
        self.menu_func(menu_choices, choice)
    
    "FILMS MENU"
    def films_menu(self) -> None:
        """Run the films menu
        """
        def clear_screen():
            self.show_menu('FILMS MENU', menu_choices)
        
        menu_choices = [
            ("Show all episodes", self.list_episodes),
            # ("Show favories", None),
            # ("Add favorite", None),
            # ("Remove favorite", None),
            ("Clear screen", clear_screen),
            ("Main menu", self.quit_menu),
            ("[dim italic]Refresh episodes[/dim italic]", self.load_films),
        ]
        
        self.show_menu('FILMS MENU', menu_choices)
        
        # Menu loop
        while True:
            # Ask the user to choice
            choice = prompt.ask_choice(menu_choices)
            
            # If the user select back to main menu, left
            if menu_choices[choice-1][1] == self.quit_menu:
                return
            else:
                self.menu_func(menu_choices, choice)
    
    def list_episodes(self) -> None:
        """List all the episode
        """
        
        episodes_table = Table(header_style="magenta")
        episodes_table.add_column("ID")
        episodes_table.add_column("Title")
        episodes_table.add_column("Director")
        episodes_table.add_column("Release date")
        
        
        try:
            self.episodes
        except:
            self.load_films(False)

        for film in self.episodes.order_by('episode_id'):
            episodes_table.add_row(str(film.episode_id), film.title, film.director, film.release_date)
            
        console.print(episodes_table)
    
    def load_films(self, show_done: bool = True):
        with console.status("[green]Loading episodes...[/green]") as status:
            self.episodes = swapi.get_all('films')
            if show_done:
                console.print("Done", style="green")
    
    
    
    "CREDITS MENU"
    def credits_menu(self) -> None:
        """Displays information about author and licence
        """
        # Clear the console
        display.clear()
                
        # Game title
        display.app_title()
        
        # Project description
        display.section_title("DESCRIPTION")
        console.print("A Star Wars Movie Selector for \"projet transversal sn1 python\" at [link=https://www.epsi.fr/]EPSI Lille[/link=https://www.epsi.fr/]", highlight=False)
        console.print("Created in april 2024", style="dim italic", highlight=False)
        
        # Author infos
        display.section_title("AUTHOR INFOS")
        table = Table()
        table.add_column("Name")
        table.add_column("Email")
        table.add_column("Github")
        
        table.add_row("Danaël LEGRAND", "danael.legrand@ecoles-epsi.net", "[link=https://github.com/DCodeProg]DCodeProg[/link=https://github.com/DCodeProg]")
        table.add_row("Mathis SINEUX", "mathis.sineux@ecoles-epsi.net", "[link=https://github.com/MathissGit]MathissGit[/link=https://github.com/MathissGit]")
        table.add_row("Alcée LOUMOUAMOU", "a.loumouamou@ecoles-epsi.net", "[link=https://github.com/Alcee242]Alcee242[/link=https://github.com/Alcee242]")
        table.add_row("Alexis FABRE", "alexis.fabre@ecoles-epsi.net", "[link=https://github.com/sixelasido]Sixelasido[/link=https://github.com/sixelasido]")
        table.add_row("Mathis THIBAUT", "mathis.thibaut@ecoles-epsi.net", "[link=https://github.com/mthibaut710]mthibaut710[/link=https://github.com/mthibaut710]")
        
        console.print(table)
        
        
        # Licence infos
        display.section_title("LICENCE")
        try:
            with open(os.path.join(ROOT_DIR, "LICENSE"), "r") as file:
                console.print(file.read(), highlight=False)
        except:
            console.print("Licence file not found!", style="red")
            console.print("[link=https://github.com/DCodeProg/Integripy/blob/main/LICENSE]See the licence on github[/link=https://github.com/DCodeProg/Integripy/blob/main/LICENSE]")
        
        # Back to main menu prompt
        prompt.back_to_main_menu()
    
    
    "OTHER"
    def quit(self):
        """Exit the program
        """
        display.goodbye(False)
        quit()