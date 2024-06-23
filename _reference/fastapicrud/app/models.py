from sqlalchemy import Column, Integer, String, ForeignKey
from Conexion import Base

class User(Base):
    __tablename__ = 'usuario'
    id = Column(Integer,primary_key=True,index=True)
    username = Column(String(20))
    nombre = Column(String(200))
    estado = Column(Integer)
    rol_id = Column(Integer, ForeignKey('rol.id'))
    
class Rol(Base):
    __tablename__ = 'rol'
    id = Column(Integer,primary_key=True,index=True)
    nombre = Column(String(20))
    descripcion = Column(String(200))

