# Barre el directorio: c:/bodysoul/entradas, buscando: ingresos * .xlsx
# por cada excel, vacia y luego llena una temporal en sql (sin definir estructura previamente)
# dentro del lazo se ejecuta un query que incorpora esos datos en ficha_productos (siempre que 
# no hayan sido incluidos antes)

from ast import Delete
from datetime import datetime
import numpy as np
import sys
import sqlalchemy
import pyodbc
import urllib
from sqlalchemy import delete
from sqlalchemy import text
from sqlalchemy import column
import sqlalchemy as sa
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
#----------------------------------------

from sqlalchemy import Column, Integer, String, Date, DateTime, CHAR, NVARCHAR, NCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class FichaProducto(Base):
    __tablename__ = 'FICHA_PRODUCTO'

    id = Column(Integer, primary_key=True)
    CONTADOR = Column(Integer)
    CODIGO_PRODUCTO = Column(NVARCHAR(50))
    STOCK_INICIAL = Column(Integer)
    STOCK_ACTUAL = Column(Integer)
    FALTA = Column(DateTime)
    FECHADOC = Column(Date)
    NRODOC = Column(NVARCHAR(50))
    TIPOMOV = Column(NVARCHAR(50))
    CANTIDAD = Column(Integer)
    PRECIO = Column(Integer)
    PEDIDO = Column(CHAR)
    PROD_COMPENSA = Column(CHAR(18))
    PEDIDOID = Column(Integer)
    ZONA = Column(CHAR(3))
    AnioCampania = Column(CHAR(35))
    CODIGO_PROVEEDOR = Column(NCHAR(20))
    # Agrega más columnas según la estructura de tu tabla

# Luego, en tu código anterior, importa la definición del modelo:

#from tu_modelo import FichaProducto

#----------------------------------------
import pandas as pd
import glob, os
from pandas.core.frame import DataFrame
import pandas as pd

os.chdir('d:\\bodysoul\\entradas\\')
#trabajo=os.getcwd()
#---------------------------------------------------
query = """
INSERT INTO dbo.FICHA_PRODUCTO (CODIGO_PRODUCTO, STOCK_INICIAL, STOCK_ACTUAL, FALTA, FECHADOC, NRODOC, TIPOMOV, CANTIDAD, PRECIO, PEDIDO, PROD_COMPENSA, PEDIDOID, ZONA, AnioCampania, CODIGO_PROVEEDOR)
SELECT producto, 0, 0, GETDATE(), fechadoc, cbante, 
iif(movimiento=101,'ID','CR'), cantidad, costo, cbante, '', 0, ' ', ' ', '0'
FROM excel_temp
WHERE NOT EXISTS (
  SELECT 1
  FROM dbo.FICHA_PRODUCTO
  WHERE dbo.FICHA_PRODUCTO.CODIGO_PRODUCTO = excel_temp.producto
    AND dbo.FICHA_PRODUCTO.FECHADOC = excel_temp.fechadoc
    AND dbo.FICHA_PRODUCTO.NRODOC = excel_temp.cbante
    AND dbo.FICHA_PRODUCTO.TIPOMOV = iif(excel_temp.movimiento=101,'ID','CR'))
"""
#---------------------------------------------------
# Conexion a SQL Server
params = urllib.parse.quote_plus("DRIVER={SQL Server Native Client 11.0};"
                                 "SERVER=MARTIN-RYZEN;"
                                 "DATABASE=bodysoul;"
                                 "UID=Martin;"
                                 "PWD=Inicio.01")
engine = sqlalchemy.create_engine("mssql+pyodbc:///?odbc_connect={}".format(params))
#---------------------------------------------------
conn = urllib.parse.quote_plus(
    'Data Source Name=MssqlDataSource;'
    'Driver={SQL Server};'
    'Server=MARTIN-RYZEN;'
    'Database=bodysoul;'
    'Trusted_connection=yes;'
)
try:
    coxn = create_engine('mssql+pyodbc:///?odbc_connect={}'.format(conn))
    print("Passed")
except:
    print("failed!")
#--------------------------
def informo():
    Session = sessionmaker(bind=engine)
    session = Session()
    otroquery = session.query(func.count()).\
        filter(FichaProducto.FALTA.cast(sa.String(10)) == func.cast(func.getdate(), sa.String(10)))
    valor = otroquery.scalar()
    print(valor)    
    return valor
antes=informo()    
#---------------------------------------------------
for archi in glob.glob("ingresos"+"*"+".xlsx"):
    df = pd.read_excel(archi, engine = 'openpyxl')
    try:
        df.to_sql('excel_temp',con=coxn,if_exists='replace')
    except:
        pass
        print("Fallo!"     )
    else:
        print(f'Almacenado correctamente {archi}') 
        print(df)
        tabla1 = text(query)
        result1 = engine.execute(tabla1)



# Obtener el valor retornado
despues=informo()
print (f'Ingreso: {despues-antes}')
#---------------------------------------------------
