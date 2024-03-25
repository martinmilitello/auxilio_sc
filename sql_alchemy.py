from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Configuración de la conexión a la base de datos SQL Server
server_name = 'LT00149\\LT00149'  # Doble barra invertida para el carácter de escape
database_name = 'VIOLETTAPRD'
connection_string = f'mssql+pyodbc://{server_name}/{database_name}?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server'

# Crear el motor de SQLAlchemy
engine = create_engine(connection_string, echo=True)

# Definir una clase base para las clases del modelo
Base = declarative_base()

# Definir la clase Objetivos que mapea a la tabla en la base de datos
class Objetivos(Base):
    __tablename__ = 'OBJETIVOS'
    PERIODO = Column(Integer, primary_key=True)
    MontoEfectivo = Column(String)

# Crear las tablas en la base de datos (opcional)
# Base.metadata.create_all(engine)

# Crear una sesión
Session = sessionmaker(bind=engine)
session = Session()

# Realizar una consulta SELECT simple
objetivos = session.query(Objetivos).all()

# Mostrar los resultados en un print()
for objetivo in objetivos:
    print(f"ID: {objetivo.PERIODO}, Descripción: {objetivo.MontoEfectivo}")

# Cerrar la sesión
session.close()
