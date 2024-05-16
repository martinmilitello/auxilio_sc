#----------------------------------------------------------------------------------#
# En CAB_TANGO_CRUDO, DET idem y CLI idem, estan los TXT levantados (crudos de PSTD)
# Este genera salidas CSV (cabeza, detalle y clientes, aptos para TANGO)
#----------------------------------------------------------------------------------#
import numpy as np
import pandas as pd
import glob, os
import pyodbc
from datetime import datetime
from bd import conexion   # bd_violettaprd



now = datetime.now()
eldi=(f'{now.day:02}')
#eldi='24'      # si proceso al otro dia informar fecha del excel hardcodeando o cambiar nombre a excel
elme=(f'{now.month:02}')
elan=str(now.year)
elamd=elan+elme+eldi
lahor=datetime.now().strftime('%Y-%m-%d %H%M%S')
lahor=lahor[11:20]
#qzoquie='984'

os.chdir('.\subidasr\\')
trabajo=os.getcwd()
#---------------------------- leo sql
from bd import conexion   # bd_violettaprd

try:
    with conexion.cursor() as cursor:
#               "cursor.execute('SET NOCOUNT ON; EXEC schema.proc @muted = 1')
        consultaR="select * from CLIENTES_SAP"
        df_clie = pd.read_sql_query(consultaR, conexion)

    
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

# df_muynuevo['fecalta'] = df_muynuevo['fecalta'].dt.date
print(df_muynuevo.dtypes)

# df_muynuevo['as_date'] = pd.to_datetime(df_muynuevo['fecalta'], format='%d/%m/%Y')
# df_muynuevo['fecalta'] = pd.to_datetime(df_muynuevo['fecalta'], format='%Y-%m-%d %H:%M:%S.%f')
# ['fecalta'] = df_muynuevo['fecalta'].dt.date

df_muynuevo['codcliente'] = df_muynuevo['codcliente'].str.strip().fillna(0) # ddf['docnro'] = df['docnro'].                  str.strip().fillna(0).astype(float)
df_muynuevo['codcliente'] = pd.to_numeric(df_muynuevo['codcliente'], errors='coerce').astype(pd.Int64Dtype())

df_muynuevo['fecalta'] = pd.to_datetime(df_muynuevo['fecalta'], errors='coerce')

df_muynuevo[['codcliente','DVojo']] = df_muynuevo[['codcliente','DVojo']].astype(str)
df_muynuevo["codcliente"] = df_muynuevo["codcliente"] + df_muynuevo["DVojo"]
df_muynuevo= df_muynuevo.drop(['DVojo'], axis=1)

df_muynuevo.tipdoc=df_muynuevo.tipdoc.fillna(0).astype(int)

df_muynuevo['docnro'] = df_muynuevo['docnro'].str.strip().fillna(0) # ddf['docnro'] = df['docnro'].                  str.strip().fillna(0).astype(float)
df_muynuevo['docnro'] = pd.to_numeric(df_muynuevo['docnro'], errors='coerce').astype(pd.Int64Dtype())

df_muynuevo['altura'] = df_muynuevo['altura'].str.strip().fillna(0)  #df_muynuevo.altura=df_muynuevo.altura.fillna(0).astype(int)
df_muynuevo['altura'] = pd.to_numeric(df_muynuevo['altura'], errors='coerce').astype(pd.Int64Dtype())
#    cli_df.piso=cli_df.piso.fillna(0).astype(int)
#df_muynuevo.codpost=df_muynuevo.codpost.fillna(0).astype(int)
df_muynuevo['codpost'] = df_muynuevo['codpost'].str.strip().fillna(0)  #df_muynuevo.altura=df_muynuevo.altura.fillna(0).astype(int)
df_muynuevo['codpost'] = pd.to_numeric(df_muynuevo['codpost'], errors='coerce').astype(pd.Int64Dtype())

# df_muynuevo.cat_Iva=df_muynuevo.cat_Iva.astype(int)
df_muynuevo['cat_Iva'] = df_muynuevo['cat_Iva'].str.strip().fillna(0)  #df_muynuevo.altura=df_muynuevo.altura.fillna(0).astype(int)
df_muynuevo['cat_Iva'] = pd.to_numeric(df_muynuevo['cat_Iva'], errors='coerce').astype(pd.Int64Dtype())

df_muynuevo.to_csv(r'CLI'+elamd +'_Z'+'.txt', header=True, index=None, sep=',', mode='a', quotechar='"')
