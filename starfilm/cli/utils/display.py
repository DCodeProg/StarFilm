import rich
from rich.console import Console

def app_title():
    """Display app title in concole
    """    
    console = Console()
    console.print(r""" _____ _              ______ _ _           
/  ___| |             |  ___(_) |          
\ `--.| |_ __ _ _ __  | |_   _| |_ __ ___  
 `--. \ __/ _` | '__| |  _| | | | '_ ` _ \ 
/\__/ / || (_| | |    | |   | | | | | | | |
\____/ \__\__,_|_|    \_|   |_|_|_| |_| |_|                               
""", style="#FFE81F", highlight=False)