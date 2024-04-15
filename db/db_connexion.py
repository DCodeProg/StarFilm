from sqlalchemy import create_engine
from sqlalchemy import select

db_path = r'sqlite:///db/db_StarFilm.db'

engine = create_engine(db_path)

try: 
    conn = engine.connect()
    # print("Success!")
    
except Exception as ex: 
    print(ex)