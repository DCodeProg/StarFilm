from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Users(Base):
    __tablename__ = "Users"

    idUser = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(300), nullable=False)
    
    favorites = relationship("Favorites", secondary="user_has_favorite")
    roles = relationship("Roles", secondary="user_has_role")
    
    def __repr__(self):
        return f"Users(idUser={self.idUser!r}, username={self.username!r})"

class Roles(Base):
    __tablename__ = "Roles"

    idRole = Column(Integer, primary_key=True)
    label = Column(String(50), nullable=False)
    
    users = relationship("Users", secondary="user_has_role")
    
    def __repr__(self):
        return f"Roles(idRole={self.idRole!r}, label={self.label!r})"

class Favorites(Base):
    __tablename__ = "Favorites"

    idEpisode = Column(Integer, primary_key=True)
    
    def __repr__(self):
        return f"Favorites(idEpisode={self.idEpisode!r})"

class user_has_favorite(Base):
    __tablename__ = "user_has_favorite"

    idUser = Column(Integer, ForeignKey("Users.idUser"), primary_key=True)
    idEpisode = Column(Integer, ForeignKey("Favorites.idEpisode"), primary_key=True)
    
    user = relationship("Users", back_populates="favorites")
    favorite = relationship("Favorites")

class user_has_role(Base):
    __tablename__ = "user_has_role"

    idUser = Column(Integer, ForeignKey("Users.idUser"), primary_key=True)
    idRole = Column(Integer, ForeignKey("Roles.idRole"), primary_key=True)
    
    user = relationship("Users", back_populates="roles")
    role = relationship("Roles")