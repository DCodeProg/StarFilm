from sqlalchemy import Column, ForeignKey, Integer, String, create_engine, select
from sqlalchemy.orm import sessionmaker, relationship 
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Users(Base):
    __tablename__ = "Users"

    def __init__(self):
        db_path = r'sqlite:///db/db_StarFilm.db'
        self.engine = create_engine(db_path)

    idUser = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(300), nullable=False)

    favorites = relationship("Favorites", secondary="user_has_favorite", back_populates="users")
    roles = relationship("Roles", secondary="user_has_role")

    def __repr__(self):
        return f"Users(idUser={self.idUser!r}, username={self.username!r})"
    
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
                select(Favorites)
                .join(user_has_favorite)
                .join(Users)
                .filter(Users.username == username)
            )
            favorites = session.execute(stmt).fetchall()
            return favorites
        
        except Exception as ex:
            print(ex)
            return None

    def add_favorites(self, username, episode_id):
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
                user.favorites.append(new_favorite)
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

    
class Favorites(Base):
    __tablename__ = "Favorites"

    idEpisode = Column(Integer, primary_key=True)
    
    users = relationship("Users", secondary="user_has_favorite", back_populates="favorites")
    
    def __repr__(self):
        return f"Favorites(idEpisode={self.idEpisode!r})"

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


# EXEMPLE D'UTILISATION #

###### get_favorites() #######
# user = Users()
# exemple_favorites = user.get_favorites("test")
# if exemple_favorites:
#     print(exemple_favorites)


###### add_favorites() #######
# user = Users()
# user.add_favorites("test", 2)


###### del_favorites() #######
# user = Users()
# user.del_favorites("test", 2)