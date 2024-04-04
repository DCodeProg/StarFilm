# StarFilm
A Star Wars Movie Selector for "projet transversal sn1 python" at EPSI Lille

## Technology and Tools:
![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)


- [GitHub](https://github.com/DCodeProg/StarFilm)
- [Python 3.12](https://docs.python.org/3.12/)
- [Swapi](https://swapi.dev/)
- [SQLite](https://swapi.dev/)
- [SqlAlchemy](https://www.sqlalchemy.org/)

## Preps
### 1. Naming conventions
```py
# CamelCase
class MyClass():
    ...

# snake_case
def my_function(x: int = 0) -> None:
    ...

# snake_case
my_var: str = ""

# UPPER_CASE
MY_CONSTANT: float = 3.14
```

### 2. Versionning
```
Version number change 
X.0.0 When new major version
0.X.0 When new little feature
0.0.X When new minor change
```

### 3. Documentation
```py
# Docstring format: Google
def my_function(x: int = 0) -> None:
    """_summary_

    Args:
        x (int, optional): _description_. Defaults to 0.
    """
```

### 4. Communication
- Discord
- [Trello]()

### 5. Dev strategies
- Merge review
- Code review
- Peer programming
- Project management with Trello

### 6. Libs
- 
- 

## User stories
### Feature: Add favorite movies

#### En tant que client je souhaite enregistrer un des films de starwars en tant que favoris afin de le retrouver facilement plus tard
- Il faut pouvoir consulter la liste des films *(numéro d'épisode, titre, release_date)*
- En choisir un pour l'ajouter aux favoris
- Une confirmation doit être faite à l'utilisateur pour lui confirmer l'ajout en favoris

#### En tant que client je souhaite consulter ma liste de films favoris afin de retrouver rapidement mes films sauvegardés
- On affiche les mêmes infos que pour la liste des films mais uniquement les films favoris
- L'utilisateur doit accéder à ses favoris par une interface dédiés

#### En tant que client je souhaite supprimer un film de ma liste afin de gérer efficacement les films que j'ai sauvegardés
- La suppression se fait depuis la liste des films favoris
- L'utilisateur sélectionne un film pour l'effacer
- Il faut demander confirmation à l'utilisateur avant l'effacement
- Il faut confirmer l'effacement à l'utilisateur


----------
### Feature: Connexion 
#### En tant que client je souhaite me connecter afin que l'application se souvienne de moi à l'avenir.
- Connexion pour nom d'utilisateur et mot de passe
- Les favoris sont enregistrés pour un utilisateur spécifique

#### En tant qu'administrateur je souhaite pouvoir me connecter afin de gérer et consulter des statistiques de l'application
- L'administrateur est un rôle spécial qui peut consulter des statistiques inaccessible aux autres utilisateurs

----------
### Feature: Stats
#### En tant qu'administrateur je souhaite consulter le nombre d'utilisateurs ayant ajoutés en favoris les films star wars
- Se matérialise par une liste de films ainsi que le nombre d'ajout en favoris
- Les films sont triés du plus favoris au moins.