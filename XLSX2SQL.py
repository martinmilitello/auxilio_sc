# Programa para el INgreso de una planilla XLSX en formato
# Tabla SQL Server .
# Cambiar la linea de conexion con servidor SQL Server 
# y elegir una planilla Excel

from ast import Delete
from datetime import datetime
import pandas as pd
import numpy as np
import os
import sqlalchemy
import urllib
from sqlalchemy import delete
from sqlalchemy import text



archi_xlsx='Cosmeticos_20221125.xlsx'
nombreTabla = archi_xlsx.split('.')
nombreTabla = nombreTabla[0]



os.chdir('D:\\Excel')
# Levanto archivo Excel
df_archiXLSX=pd.read_excel(archi_xlsx, sheet_name=None)
# Junto todas las hojas en un Dataframe

df_archiXLSX = pd.concat(df_archiXLSX, ignore_index=True)


print(df_archiXLSX)


# Conexion a SQL Server
params = urllib.parse.quote_plus("DRIVER={SQL Server Native Client 11.0};"
                                 "SERVER=MARTIN-RYZEN;"
                                 "DATABASE=FacturacionTango;"
                                 "UID=tincho666;"
                                 "PWD=Inicio.01")

engine = sqlalchemy.create_engine("mssql+pyodbc:///?odbc_connect={}".format(params))
connection = engine.connect()

if not engine.dialect.has_table(connection,nombreTabla):  #Verifico que la tabla no exista
    df_archiXLSX.to_sql(nombreTabla, con=engine)
else:   #Si existe la borro y le inserto los datos
    truncate_query = sqlalchemy.text("TRUNCATE TABLE "+ nombreTabla)
    connection = engine.connect()
    connection.execution_options(autocommit=True).execute(truncate_query)
    df_archiXLSX.to_sql(nombreTabla, con=engine, if_exists='append')
#Guardo en SQLServer


os.chdir('D:\\Excel')



