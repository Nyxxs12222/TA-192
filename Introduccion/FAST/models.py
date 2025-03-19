from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class User(Base):
    __tablename__ = 'tbl_users' # Corregido el nombre de la tabla (era_tablename_)
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    age = Column(Integer)
    email = Column(String) # El error estaba en el uso de un espacio noválido en "email"
