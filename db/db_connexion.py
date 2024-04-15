from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import Session

from model import *


db_path = r'sqlite:///db/db_StarFilm.db'

engine = create_engine(db_path)

try: 
    conn = engine.connect()
    print("Success!")

    session = Session(engine)
    stmt = select(Users)
    
except Exception as ex: 
    print(ex)

