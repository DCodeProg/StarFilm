import os
from rich.console import Console
from rich.table import Table
from rich.prompt import Confirm

from .swapi import swapi
from .utils import *
from .models import *

console = Console()
CUR_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.dirname(CUR_DIR)


class CliApp:
    """Command line interface for Star Film
    """
    
    def __init__(self) -> None:
        self.logged_in = False
        self.username = ""
        self.admin = False
        
        try:
            self._app_loop()
        except KeyboardInterrupt:
            self.quit(True)
            
            
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
        
        if self.admin:
            menu_choices = [
                ("Films menu", self.films_menu),
                ("Admin menu", self.admin_menu),
                ("Authentification", self.auth_menu),
                ("Credits", self.credits_menu),
                ("Quit", self.quit),
            ]
        else:
            menu_choices = [
                ("Films menu", self.films_menu),
                ("Authentification", self.auth_menu),
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
        
        try:
            self.episodes
        except:
            self._load_films()
        
        def clear_screen():
            self.show_menu('FILMS MENU', menu_choices)
        
        if self.logged_in:
            menu_choices = [
                ("Show all episodes", self.list_episodes),
                ("Show favories", self.list_favorites),
                ("Add favorite", self.add_favorite),
                ("Remove favorite", self.remove_favorite),
                ("Clear screen", clear_screen),
                ("Main menu", self.quit_menu),
                ("[dim italic]Refresh episodes[/dim italic]", self._load_films),
            ]
        else:
            menu_choices = [
                ("Show all episodes", self.list_episodes),
                ("Clear screen", clear_screen),
                ("Main menu", self.quit_menu),
                ("[dim italic]Refresh episodes[/dim italic]", self._load_films),
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
                
        for film in self.episodes.order_by('episode_id'):
            episodes_table.add_row(str(film.episode_id), film.title, film.director, film.release_date)
            
        console.print(episodes_table)
    
    def _load_films(self, show_done: bool = True) -> None:
        with console.status("[green]Loading episodes...[/green]") as status:
            self.episodes = swapi.get_all('films')
            if show_done:
                console.print("Done", style="green")
    
    def list_favorites(self) -> None:
        if not self.logged_in:
            console.print("You must be logged in!", style="red")
            return
            
        episodes_table = Table(header_style="magenta")
        episodes_table.add_column("ID")
        episodes_table.add_column("Title")
        episodes_table.add_column("Director")
        episodes_table.add_column("Release date")
        
        with console.status("Loading favorites...") as status:
            favorites = Users().get_favorites(self.username)

            for episode in self.episodes.order_by('episode_id'):
                if episode.episode_id in favorites:
                    episodes_table.add_row(f"{episode.episode_id}", episode.title, episode.director, episode.release_date) 
            
            
        console.print(episodes_table)
        
    def add_favorite(self) -> None:           
        console.print("[green]Add Favorite")
        choice = prompt.ask_episode_id([str(e.episode_id) for e in self.episodes.items])
        
        with console.status("Loadind episode infos...") as status:
            for episode in self.episodes.items:
                if episode.episode_id == choice:
                    console.print(f"\nEpisode {episode.episode_id}: \"{episode.title}\" by {episode.director}", highlight=False)
                    break
                
        if Confirm.ask("[green]Add to favorite?"):
            Users().add_favorite(self.username, choice)
        
        
    def remove_favorite(self) -> None:
        console.print("[red]Remove Favorite")
        fav_list = Users().get_favorites(self.username)
        
        if not fav_list:
            console.print("[red]You have no favorites!")
            return
        
        choice = prompt.ask_episode_id([str(i) for i in fav_list]) 
        with console.status("Loadind episode infos...") as status:
            for episode in self.episodes.items:
                if episode.episode_id == choice:
                    console.print(f"\nEpisode {episode.episode_id}: \"{episode.title}\" by {episode.director}", highlight=False)
                    break
        
        if Confirm.ask("[red]Remove of favorite?"):
            Users().del_favorites(self.username, choice)
    
    
    "AUTH MENU"
    def auth_menu(self):
        """Run the auth menu
        """
        
        if self.logged_in:
            menu_choices = [
                ("Logout", self.logout),
                ("Logout & quit", self.logout_and_exit),
                ("Main menu", self.quit_menu),
            ]
        else:
            menu_choices = [
                ("Login", self.login),
                # ("Register", None),
                ("[dim italic]Admin", self.admin_login),
                ("Main menu", self.quit_menu),
            ]
            
        
        
        self.show_menu('AUTH MENU', menu_choices)
        
        # Ask the user to choice
        choice = prompt.ask_choice(menu_choices)
            
        # If the user select back to main menu, left
        if menu_choices[choice-1][1] == self.quit_menu:
            return
        else:
            self.menu_func(menu_choices, choice)
                
    def admin_login(self) -> None:
        username = prompt.ask_username()
        password = prompt.ask_password()
        
        if Users().authenticate(username, password) and Users().is_admin(username):
            self.logged_in = True
            self.username = username
            self.admin = True
            display.login_success()
        else:
            display.login_fail()
            prompt.ask_continue()
            return self.auth_menu()
        
        prompt.back_to_main_menu()
                
    def login(self) -> None:
        username = prompt.ask_username()
        password = prompt.ask_password()
        
        if Users().authenticate(username, password):
            self.logged_in = True
            self.username = username
            display.login_success()
        else:
            display.login_fail()
            prompt.ask_continue()
            return self.auth_menu()
        
        prompt.back_to_main_menu()
        
    def logout(self) -> None:
        self.logged_in = False
        self.username = ""
        self.admin = False
        
        console.print("You have been logged out", style="red")
        prompt.back_to_main_menu()
        
    def logout_and_exit(self) -> None:
        self.logged_in = False
        self.username = ""
        self.admin = False
        
        console.print("You have been logged out", style="red")
        self.quit(True)
    
    
    "ADMIN MENU"
    def admin_menu(self) -> None:
        """Run the admin menu
        """
        
        try:
            self.episodes
        except:
            self._load_films(False)
        
        def clear_screen():
            self.show_menu('FILMS MENU', menu_choices)
        
        menu_choices = [
            ("Show fav stats", self.fav_stats),
            # ("Show user stat", self.list_favorites),
            ("Clear screen", clear_screen),
            ("Main menu", self.quit_menu),
        ]
            
        self.show_menu('ADMIN MENU', menu_choices)
        
        # Menu loop
        while True:
            # Ask the user to choice
            choice = prompt.ask_choice(menu_choices)
            
            # If the user select back to main menu, left
            if menu_choices[choice-1][1] == self.quit_menu:
                return
            else:
                self.menu_func(menu_choices, choice)
    
    def fav_stats(self) -> None:
        fav_list = Favorites.get_fav_stats()
        
        table = Table(header_style="magenta")
        table.add_column('Count Fav')
        table.add_column('ID')
        table.add_column('Title')
        table.add_column('Director')
        table.add_column('Release date')
        
        films_list = []            
        for key, value in fav_list.items():
            for episode in self.episodes.items:
                if episode.episode_id == key:
                    film = episode
                    films_list.append((value, key, episode.title, episode.director, episode.release_date))
                    
        films_list.sort(key=lambda key: key[0], reverse=True)
        
        for film in films_list:
            table.add_row(f"{film[0]}", f"{film[1]}", f"{film[2]}", f"{film[3]}", f"{film[4]}")
            
        console.print(table)
    
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
    def quit(self, on_newline: bool = False):
        """Exit the program
        """
        display.goodbye(on_newline)
        quit()