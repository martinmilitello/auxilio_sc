from datetime import datetime
import pandas as pd
import numpy as np
import csv
import os
import sys
import glob, os

os.chdir('..\subidasp\\')
for cabenombrearchivo in glob.glob("C*.csv"):
    for pos,char in enumerate(cabenombrearchivo):
        os.chdir('..\subidasp\\')
        if(ord(char) >= 48 and ord(char) <= 57 and pos == 2 and cabenombrearchivo[0]== 'C'):
            cabe_df=pd.read_csv(cabenombrearchivo, dtype=str,quotechar = '"')
            texto = "D"+cabenombrearchivo[1:18]
            for detanombrearchivo in glob.glob(texto):
                deta_df=pd.read_csv(detanombrearchivo, dtype=str,quotechar = '"')
                revend_df = pd.read_csv(cabenombrearchivo, dtype=str,quotechar = '"', sep=',', usecols=("cod_cliente","importe"))
                revend_df2 =  revend_df[revend_df['importe'].apply(lambda x : float(x)) > 338.99]
                revend_df2['cod_cliente'] = revend_df2['cod_cliente'].str[:-1]
                cabe_df.cod_cliente=cabe_df.cod_cliente.fillna(0)
                deta_df.revend = deta_df.revend.str.strip()  #elimino los espacios del campo revend del Deta
                cabe_df.revend = cabe_df.cod_cliente.str.strip()  #elimino los espacios del campo cod_cliente del Cabe

                # Extraigo cabezas csv
                os.chdir('..\salidas\\')
                cabe_in_salida=  cabenombrearchivo
                kk=cabe_df.loc[cabe_df.loc[: , 'importe'].apply(lambda x : float(x)) > 338.99]
                kk.orden=kk.orden.astype(int)
                kk.cod_cliente=kk.cod_cliente.astype(int)
                kk.figura=kk.figura.astype(int)
                kk.importe=kk.importe.astype(float)
                kk.bonif_sin_imp=kk.bonif_sin_imp.astype(float)
                kk.imp_gravado=kk.imp_gravado.astype(float)
                kk.imp_exento=kk.imp_exento.astype(float)
                kk.imp_iva=kk.imp_iva.astype(float)
                kk.montib=kk.montib.astype(float)
                kk.boniflibro=kk.boniflibro.astype(float)
                kk.bonifivadic=kk.bonifivadic.astype(float)
                kk.zona=kk.zona.astype(int)
                kk.to_csv(cabe_in_salida,quoting=csv.QUOTE_NONNUMERIC, index=False, header=True, )
                
                cabe_df['cod_cliente'] = cabe_df['cod_cliente'].str[:-1]
                deta_df_type=deta_df.dtypes
                revend_df2_type=revend_df2.dtypes
                cabe_df_in=cabe_df[cabe_df.cod_cliente.isin(revend_df2.cod_cliente)]
                deta_df_in=deta_df[deta_df.revend.isin(revend_df2.cod_cliente)]

                # Cambio los tipo sde datos para que no ponga comillas a los numericos
                # los que estan dentro de la extraccion 
                deta_df_in.orden=deta_df_in.orden.astype(int)
                deta_df_in.renglon=deta_df_in.renglon.astype(int)
                deta_df_in.cantidad=deta_df_in.cantidad.astype(float)
                deta_df_in.importe_neto=deta_df_in.importe_neto.astype(float)
                deta_df_in.precio_neto=deta_df_in.precio_neto.astype(float)
                deta_df_in.porc_iva=deta_df_in.porc_iva.astype(float)
                deta_df_in.precio_lista=deta_df_in.precio_lista.astype(float)
                deta_df_in.total_renglon=deta_df_in.total_renglon.astype(float)
                deta_df_in.revend=deta_df_in.revend.astype(int)
                deta_df_type=deta_df.dtypes

                deta_df_in.to_csv(detanombrearchivo,quoting=csv.QUOTE_NONNUMERIC, index=False, header=True, )
            
