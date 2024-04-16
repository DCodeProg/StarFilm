import os
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine, select, insert, func
from sqlalchemy.orm import sessionmaker, relationship, declarative_base

CUR_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.dirname(CUR_DIR)

db_path = r'sqlite:///' + os.path.join(ROOT_DIR, r'db/db_StarFilm.db')
engine = create_engine(db_path)

Base = declarative_base()

class Users(Base):
    __tablename__ = "Users"

    def __init__(self):
        db_path = r'sqlite:///' + os.path.join(ROOT_DIR, r'db/db_StarFilm.db')
        self.engine = create_engine(db_path)

    idUser = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(300), nullable=False)

    favorites = relationship("Favorites", secondary="user_has_favorite", back_populates="users")
    roles = relationship("Roles", secondary="user_has_role")

    def __repr__(self):
        return f"Users(idUser={self.idUser!r}, username={self.username!r})"
    
    def is_admin(self, username):

        Session = sessionmaker(bind=self.engine)
        session = Session()

        try:
            stmt = (
                select(Roles.label)
                .join(user_has_role)
                .join(Users)
                .filter(Users.username == username)
            )
            
            list_role = []
            
            result = session.execute(stmt)
            for role in result:
                list_role.append(role[0])
                
            return 'admin' in list_role
        
        except Exception as ex:
            print(ex)
            return None
    
    def get_favorites(self, username): 
        """Liste tous les favoris de l'utilisateur

        Args:
            username (string): ...

        Returns:
            string: liste des Favoris
        """

        Session = sessionmaker(bind=self.engine)
        session = Session()

        try:
            stmt = (
                select(Favorites.idEpisode)
                .join(user_has_favorite)
                .join(Users)
                .filter(Users.username == username)
            )
            
            list_fav = []
            
            result = session.execute(stmt)
            for fav in result:
                list_fav.append(fav[0])
                
            return list_fav
        
        except Exception as ex:
            print(ex)
            return None

    def add_favorite(self, username, episode_id):
        """Ajoute un épisode aux favoris de l'utilisateur et met à jour les tables Favorites et user_has_favorite.

        Args:
            username (string): ...
            episode_id (int): ...
        """
        
        Session = sessionmaker(bind=self.engine)
        session = Session()
        
        try:
            user = session.query(Users).filter(Users.username == username).first()
            if user:
                if episode_id in [favorite.idEpisode for favorite in user.favorites]:
                    print("Cet épisode est déjà dans vos favoris.")
                    return
                
                new_favorite = Favorites(idEpisode=episode_id)
                                
                    # # Ajoute l'épisode aux favoris
                    # new_favorite = Favorites(idEpisode=episode_id)
                    # session.add(new_favorite)
                
                # Met à jour les tables user_has_favorite et Favorites
                uhf = user_has_favorite(idUser=user.idUser, idEpisode=episode_id)
                session.add(uhf)
                
                session.commit()
                
                print(f"L'épisode : {episode_id} a été ajouté aux favoris de l'utilisateur {username}.")
            else:
                print("Vous devez être connecté pour ajouter aux favoris.")
            
        except Exception as ex:
            session.rollback()
            print(f"Une erreur s'est produite lors de l'ajout du favori : {ex}")
            
    def del_favorites(self, username, episode_id):
        """Supprime un favori de l'utilisateur.

        Args:
            username (string): ...
            episode_id (int): ...
        """
        Session = sessionmaker(bind=self.engine)
        session = Session()

        try:
            user = session.query(Users).filter(Users.username == username).first()
            if user:
                favorite_entry = session.query(user_has_favorite).filter_by(idUser=user.idUser, idEpisode=episode_id).first()
                if favorite_entry:
                    session.delete(favorite_entry)
                    favorite = session.query(Favorites).filter_by(idEpisode=episode_id).first()
                    if favorite:
                        session.delete(favorite)
                        print(f"L'épisode : {episode_id} a été supprimée.")
                else:
                    print(f"Erreur dans la suppression du favoris")
                session.commit()
            else:
                print(f"Vous devez être connecté pour ajouter aux favoris.")
            
        except Exception as ex:
            session.rollback()
            print(f"Une erreur s'est produite lors de la suppression du favori : {ex}")

    def authenticate(self, username, password) -> bool:
        """Vérifie si le mot de passe correspond au nom d'utilisateur

        Args:
            username (str):
            password (str):
        """

        Session = sessionmaker(bind=self.engine)
        session = Session()

        if user:=session.query(Users).filter(Users.username == username).first():
            if user.password == password:
                return True
        else:
            return False
    
    def list_all_users(self):
        
        Session = sessionmaker(bind=self.engine)
        session = Session()
        try: 
            list_users = session.query(Users).all()
            users = []
            for user in list_users:
                users.append((user.idUser, user.username))
            return users
                
        except Exception as e: 
            print(f"Erreur de récupération des utilisateurs : {e}")

                        
    
class Favorites(Base):
    __tablename__ = "Favorites"
    
    idEpisode = Column(Integer, primary_key=True)
    
    users = relationship("Users", secondary="user_has_favorite", back_populates="favorites")        
    
    def __repr__(self):
        return f"Favorites(idEpisode={self.idEpisode!r})"
    
    def get_fav_stats():
        Session = sessionmaker(bind=engine)
        session = Session()

        try:
            query = (
                session.query(
                Favorites.idEpisode,
                func.count(user_has_favorite.idUser))
                .join(user_has_favorite)
                .group_by(Favorites.idEpisode)
                .order_by(Favorites.idEpisode.desc())
            )
            dict_fav = {}
            results = query.all()
            if results:
                for episode_id, count_favorites in results:
                    dict_fav[episode_id] = count_favorites
            return dict_fav
        except Exception as ex:
            print(ex)
            return None
        

    def list_user_favorites(target_username):
        """Liste les favoris de l'utilisateur par son nom.

        Args:
            session: SQLAlchemy
            target_username (str): target username 
        """
        Session = sessionmaker(bind=engine)
        session = Session()
        
        try:
            target_user = session.query(Users).filter(Users.username == target_username).first()
            if target_user:
                favorites = target_user.favorites
                user_favorites = []
                for favorite in favorites:
                    user_favorites.append((target_user.username, favorite.idEpisode))
                return user_favorites
            else:
                print(f"L'utilisateur avec le nom d'utilisateur {target_username} n'existe pas.")
        except Exception as ex:
            print(f"Une erreur s'est produite lors de la récupération des favoris : {ex}")
            
class Roles(Base):
    __tablename__ = "Roles"

    idRole = Column(Integer, primary_key=True)
    label = Column(String(50), nullable=False)

    def __repr__(self):
        return f"Roles(idRole={self.idRole!r}, label={self.label!r})"

class user_has_favorite(Base):
    __tablename__ = "user_has_favorite"

    idUser = Column(Integer, ForeignKey("Users.idUser"), primary_key=True)
    idEpisode = Column(Integer, ForeignKey("Favorites.idEpisode"), primary_key=True)

class user_has_role(Base):
    __tablename__ = "user_has_role"

    idUser = Column(Integer, ForeignKey("Users.idUser"), primary_key=True)
    idRole = Column(Integer, ForeignKey("Roles.idRole"), primary_key=True)


if __name__ == "__main__":
    ...
    # EXEMPLE D'UTILISATION #

    ##### get_favorites() #######
    # user = Users()
    # print(user.get_favorites("test2"))
    ##### add_favorites() #######
    # user = Users()
    # user.add_favorite("client", 1)
    # print(Favorites.get_fav_stats())


    # print(user.get_favorites("test"))

    # ##### del_favorites() #######
    # user = Users()
    # user.del_favorites("test", 2)