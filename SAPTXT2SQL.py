from ast import Delete
from datetime import datetime

import pandas as pd
import numpy as np
import os
import sys
import sqlalchemy
import pyodbc
import urllib

from sqlalchemy import delete
from sqlalchemy import text


archi_cabe='PSTD20230602_030540Cabecera.txt'
archi_deta='PSTD20230602_030540posiciones.txt'
archi_cli ='Cli_fact_20230602.txt'

# Cabeceras
os.chdir('Y:\\InterfacesSAP\\INTPEDIDOS\\BACKUP\\')

df_cabetxt=pd.read_csv(archi_cabe, delimiter = ";",  header=None)
df_cabetxt.columns = ['Zona','cod_cliente','DV','Anio','Campania','premeife','cancajas','Fecha','remito','impotot','ivatot1','ivatot2','impsobra','spbonval','nrocbte','prov','caiva','impbon1','impbon5','extracosm','impbon3','gtoadmin','exentos']

df_cabetxt['Zona'] = df_cabetxt["Zona"].str[0:3] 
df_cabetxt_agrupado = pd.DataFrame(df_cabetxt.groupby('Zona',as_index=False).sum())

df_cabetxt_agrupado.reset_index()
fecha=archi_cabe[4:12]

df_cabetxt_agrupado = df_cabetxt_agrupado[['Zona','cancajas','impotot','ivatot1','ivatot2']]

# Detalles

df_detatxt=pd.read_csv(archi_deta, delimiter = ";",  header=None)
df_detatxt.columns = ['zonasec','cod_cliente','DV','producto','digverpo','tipo','filler','aniocamp','cant','abastesp','iva2','prenp','iva1','descri','tipimpos','montib','a3','bonif','tipprod']



# Clientes

os.chdir('Y:\\InterfacesSAP\\VENTASCLI\\BACKUP\\')

df_clietxt=pd.read_csv(archi_cli, delimiter = ";",  header=None)
df_clietxt.columns = ['cod_cliente','DV','TIPREV','ZONASEC','inhabili','rasoc','TDOC','NDOC','domic','altura','piso','dpto','local','ECALL','partido','CP','CPROV','PROV','caiva','nucuit','nucuil','Barrio','retrapro']



# PEDIDOS PERSONALES -------------------------------------

df_mascara=df_clietxt["ZONASEC"].str[0:3] =='999'
df_cli999= df_clietxt[df_mascara]
df_cli999['EMPRESA']=df_cli999['ZONASEC'].str[3:6]
df_cli999['EMPRESA']=np.where(df_cli999.EMPRESA.str.contains('DRE'),'TRINDY',df_cli999.EMPRESA)
df_cli999['EMPRESA']=np.where(df_cli999.EMPRESA.str.contains('NEW'),'NEW LAB',df_cli999.EMPRESA)
df_cli999['EMPRESA']=np.where(df_cli999.EMPRESA.str.contains('CON'),'CERRITO',df_cli999.EMPRESA)
df_cli999['EMPRESA']=np.where(df_cli999.EMPRESA.str.contains('CIU'),'OESTE LOGISTIC',df_cli999.EMPRESA)


cli_columns=['','','','','','','','','','','','','','','','','','','','','','','','','',]
print(df_cli999)

df_mascara=df_cabetxt["Zona"] == "999"
df_cabe999 = df_cabetxt[df_mascara]

cabe_columns=['ivatot2','premeife', 'ivatot1', 'ivatot2', 'spbonval', 'prov', 'caiva', 'impbon1', 'impbon5','impsobra', 'extracosm', 'impbon3', 'gtoadmin', 'exentos']
df_cabe999.drop(cabe_columns,inplace=True,axis=1)
df_cabe999.columns = ['ZONA',  'NRO_CLIENTE',  'DV',  'AÑO',  'CAMPAÑA',  'CANTIDAD','FECHA','REMITO','IMPORTE','NROCBTE']



print(df_cabe999)



# Conexion a SQL Server
params = urllib.parse.quote_plus("DRIVER={SQL Server Native Client 11.0};"
                                 "SERVER=LT00149\LT00149;"
                                 "DATABASE=FacturacionTango;"
                                 "UID=tincho666;"
                                 "PWD=Inicio.01")

engine = sqlalchemy.create_engine("mssql+pyodbc:///?odbc_connect={}".format(params))


tabla1 = text("DROP TABLE dbo.Cabe_SAP_TXT")
tabla2 = text("DROP TABLE dbo.Deta_SAP_TXT")
tabla3 = text("DROP TABLE dbo.Clie_SAP_TXT")

result1 = engine.execute(tabla1)
result2 = engine.execute(tabla2)
result3 = engine.execute(tabla3)

#Guardo en SQLServer
df_cabetxt.to_sql('Cabe_SAP_TXT', con=engine, if_exists='append')
df_detatxt.to_sql('Deta_SAP_TXT', con=engine, if_exists='append')
df_clietxt.to_sql('Clie_SAP_TXT', con=engine, if_exists='append')

os.chdir('D:\\Excel')

#Guardo en XLSX
writer = pd.ExcelWriter(r"totales_SAP2TXT"+str(fecha)+".xlsx")
df_cabetxt_agrupado.to_excel(writer,'Hoja 1', index=False)
writer.save()
writer.close()


