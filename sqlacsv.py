#----------------------------------------------------------------------------------#
# En CAB_TANGO_CRUDO, DET idem y CLI idem, estan los TXT levantados (crudos de PSTD)
# Este genera salidas CSV (cabeza, detalle y clientes, aptos para TANGO)
#----------------------------------------------------------------------------------#
import numpy as np
import pandas as pd
import glob, os
import pyodbc
from datetime import datetime
from tkinter import messagebox as MessageBox
from tkinter import *
from tkinter import ttk


now = datetime.now()
eldi=(f'{now.day:02}')
#eldi='24'      # si proceso al otro dia informar fecha del excel hardcodeando o cambiar nombre a excel
elme=(f'{now.month:02}')
elan=str(now.year)
elamd=elan+elme+eldi
lahor=datetime.now().strftime('%Y-%m-%d %H%M%S')
lahor=lahor[11:20]
#qzoquie='984'

os.chdir('.\subidas\\')
trabajo=os.getcwd()
#---------------------------- leo sql
from bd import conexion   # bd_violettaprd
try:
    with conexion.cursor() as cursor:
#               "cursor.execute('SET NOCOUNT ON; EXEC schema.proc @muted = 1')
        consultaR="select * from CLIENTES_SAP WHERE ZONA = '062'"
        df_clie = pd.read_sql_query(consultaR, conexion)


        consultaC="select * from PEDIDOS_CAB_TANGO WHERE ZONA = '062'"
        df_cabe = pd.read_sql_query(consultaC, conexion)
    
#           
        consultaD="SELECT * FROM PEDIDOS_DET_SAP WHERE PEDIDOID IN(SELECT PEDIDOID FROM PEDIDOS_CAB_SAP WHERE ZONA = '062' AND FALTASAP >= '20220613' )"
        df_deta = pd.read_sql_query(consultaD, conexion)

except Exception as e:
        print("Ocurrió un error al insertar: ", e)
finally:
        #conexion.close()
        conexion.commit()
        cursor.close()            

trozos = []
#-----------------------------------------------
# sql:
# #(CLIENTE_CODIGO,DIGITO_VERIFICADOR,"\
#"GRUPO_CUENTAS,ZONA,SECCION,ESTADO,NOMBRE,TIPO_DOC,NUMERO_DOC,CALLE,CALLE_NUMERO,"\
#"PISO,DEPTO,LOCALIDAD,ENTRE_CALLE,CIUDAD,CODIGO_POSTAL,REGION,PROVINCIA,CUIT,CUIL,"\
#"BARRIO,FALTA,FMODI,EMAIL )    
#-----------------------------------------------   
# 

df_clie.columns = ['CLIENTE_CODIGO','DIGITO_VERIFICADOR','GRUPO_CUENTAS','ZONA','SECCION','ESTADO','NOMBRE',
                'TIPO_DOC','NUMERO_DOC','CALLE','CALLE_NUMERO','PISO','DEPTO','LOCALIDAD','ENTRE_CALLE','CIUDAD',
                'CODIGO_POSTAL','REGION','PROVINCIA','CUIT','CUIL','BARRIO','FALTA','FMODI','EMAIL']
# estructura del sql (input)

#CSV: codcliente,fecalta,rasoc,tipdoc,docnro,domic,altura,piso,dpto,local,ecall,calle1,calle2,
# partido,codpost,telefono,prov,cat_Iva,nucuit,nucuil,conyuge,profesio,iva_d,iva_I,alic_perc,zona                
indexclie = df_clie[ df_clie['CLIENTE_CODIGO'] > '0' ].index 


df_clie_sale=df_clie.copy()
df_muynuevo= df_clie_sale.drop(['SECCION','GRUPO_CUENTAS','EMAIL','FMODI','REGION','BARRIO'], axis=1)
# columnas que sobran

df_muynuevo = df_muynuevo [['CLIENTE_CODIGO','DIGITO_VERIFICADOR','FALTA','NOMBRE','TIPO_DOC','NUMERO_DOC',
        'CALLE','CALLE_NUMERO','PISO','DEPTO','LOCALIDAD','ENTRE_CALLE','CIUDAD','CODIGO_POSTAL','PROVINCIA',
        'ESTADO','CUIT','CUIL','ZONA']]
# las que ahora tengo
#         
df_muynuevo.columns = ['codcliente','DVojo','fecalta','rasoc','tipdoc','docnro',
        'domic','altura','piso','dpto','local','ecall','partido','codpost','prov',
        'cat_Iva','nucuit','nucuil','zona']

# las que ahora tengo con nombres correctos
df_muynuevo.insert(12,"calle1","")
df_muynuevo.insert(13,"calle2","")
df_muynuevo.insert(16,"telefono","")
df_muynuevo.insert(21,"conyuge","")
df_muynuevo.insert(22,"profesio","")
df_muynuevo.insert(23,"iva_d","N")
df_muynuevo.insert(24,"iva_I","S")
df_muynuevo.insert(25,"alic_perc","")
# agrega columnas vacias que necesito: calle1, calle2, telefono, conyuge, profesio
# agrega columnas con datos fijos que necesito: iva_d, iva_I, alic_perc ("N","S","")
print(df_muynuevo.dtypes)
# df_muynuevo['fecalta'] = df_muynuevo['fecalta'].dt.date


df_muynuevo['as_date'] = pd.to_datetime(df_muynuevo['fecalta'], format='%d/%m/%Y')
# df['formated_date'] = df['as_date'].dt.strftime('%b-%Y')
####df_muynuevo['fecalta'] = df_muynuevo['fecalta'].apply(lambda x: x.split(' ')[0])
# Se convierte a datetime
###df_muynuevo['fecalta'] = pd.to_datetime(df_muynuevo['fecalta'], format='%d/%m/%Y')
#df_muynuevo['Value'] = df_muynuevo.codcliente * df_muynuevo.DVojo
print(df_muynuevo)
################df_muynuevo['codcliente'] = df_muynuevo['codcliente'].astype(str)
#df_muynuevo.codcliente=df_muynuevo.codcliente.astype(str)
df_muynuevo[['codcliente','DVojo']] = df_muynuevo[['codcliente','DVojo']].astype(str)
df_muynuevo["codcliente"] = df_muynuevo["codcliente"] + df_muynuevo["DVojo"]
df_muynuevo= df_muynuevo.drop(['DVojo'], axis=1)

#df_muynuevo['codcliente'] = df_muynuevo['codcliente'].apply(lambda _: str(_))
#df_muynuevo['codcliente'] = df_muynuevo['codcliente'].apply(lambda _: str(_), quotechar = '"')
#dtype=str,quotechar = '"'
#df_muynuevo['codcliente'] = df_muynuevo.assign(Value = lambda x: x.codcliente * 10 + x.DVojo)

#order_df['Value'] = order_df.apply(lambda row: (row['Prices']*row['Amount']
#                                               if row['Action']=='Sell'
#                                               else -row['Prices']*row['Amount']),
#                                   axis=1)
#df_muynuevo["codcliente"] = df_muynuevo["codcliente"] * 10 + df_muynuevo["DVojo"]
#df_muynuevo["codcliente"] = df_muynuevo["codcliente"] + " " + df_muynuevo["DVojo"]

df_muynuevo.tipdoc=df_muynuevo.tipdoc.fillna(0).astype(int)
df_muynuevo.docnro=df_muynuevo.docnro.fillna(0).astype(int)
df_muynuevo.altura=df_muynuevo.altura.fillna(0).astype(int)
#    cli_df.piso=cli_df.piso.fillna(0).astype(int)
df_muynuevo.codpost=df_muynuevo.codpost.fillna(0).astype(int)
######df_muynuevo.telefono=df_muynuevo.telefono.fillna(0).astype('int64')
df_muynuevo.cat_Iva=df_muynuevo.cat_Iva.astype(int)
## df_muynuevo.nucuil=df_muynuevo.nucuil.fillna(0).astype(int)



# formato final buscado
#df_muynuevo.columns = ['codcliente','fecalta','rasoc','tipdoc','docnro','domic','altura','piso','dpto',
#        'local','ecall','calle1','calle2','partido','codpost','telefono','prov','cat_Iva','nucuit','nucuil',
#        'conyuge','profesio','iva_d','iva_I','alic_perc','zona']
# resp.insc. (sin adic)    S  S   "A"
# sug.no cat. (con adic)   N  C   "B"
# cons. final (sin adic)   N  S   "B"
# todos juntan 2 columnas en una
# df["Full Name"] = df["First"] + " " + df["Last"]
# df["Full Name"] = df["First"].map(str) + " " + df["Last"]
# df['Full Name'] = df[['First', 'Last']].apply(' '.join, axis=1)
# df['Full Name'] = df['First'].str.cat(df['Last'],sep=" ")
# df['Full Name'] = df[['First', 'Last']].agg(' '.join, axis=1)
# agregar una columna
# city = ['Lahore','Dehli','New York']   df['city'] = city
# df.insert(3,"city",['Lahore','Dehli','New York'],True)
# df = df.assign(city = ['Lahore','Dehli','New York'])
# df = df.assign(city = ['Lahore','Dehli','New York'], score = [20,30,40])
# df.loc[:,'city'] = ['Lahore','Dehli','New York']

# a salida csv
lora='080808'
lazo='777'
df_muynuevo.to_csv(r'CLI'+elamd+lora+'_Z'+lazo+'.txt', header=True, index=None, sep=',', mode='a', quotechar='"')
