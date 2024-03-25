from datetime import datetime
import pandas as pd
import numpy as np
import csv
import os
import sys

 

if len(sys.argv) == 4:
    mifecha = sys.argv[1] # Fecha del nombre de archivo (C2021061900703.csv)
    mihora = sys.argv[2] # Hora del archivo de Clientes
    mizona = sys.argv[3] # Zona
    # mipathpos = sys.argv[4] # "//dc10004/InterfacesSAP/INTPEDIDOS/"
    fijo = "00"
    zonasalida = int(mizona) + 2
    lalon1=len(mifecha)
    lalon2=len(mizona)
    zonasalida = str(zonasalida)
    rutasubida = "subidas\\"   # 
   # print("La ruta tal vez este mal")
    cabenombrearchivo = rutasubida + "C" + mifecha + fijo + mizona + ".csv"
    detanombrearchivo = rutasubida + "D" + mifecha + fijo + mizona + ".csv"
    clinombrearchivo  = rutasubida + "CLI" + mifecha + mihora + "_Z" + mizona + ".csv"

    
    # CLI20210710090908_Z703
    # Pandas haciendo un dataframe 
    # Tomo los archivos del CSV y los convierto en Dataframe de Pandas 
    cabe_df=pd.read_csv(cabenombrearchivo, dtype=str,quotechar = '"')
    deta_df=pd.read_csv(detanombrearchivo, dtype=str,quotechar = '"')
    cli_df=pd.read_csv(clinombrearchivo, dtype=str,quotechar = '"')

    demapas_df = pd.read_csv(rutasubida+"demapas.csv", dtype=str)   # Archivo CSV revend sin 000000

    # convert column "a" of a DataFrame
    # df[["a", "b"]] = df[["a", "b"]].apply(pd.to_numeric)
    
    cabe_df.cod_cliente=cabe_df.cod_cliente.fillna(0)
    deta_df.revend = deta_df.revend.str.strip()  #elimino los espacios del campo revend del Deta
    cabe_df.revend = cabe_df.cod_cliente.str.strip()  #elimino los espacios del campo cod_cliente del Cabe
    
    # cabe_df.cod_cliente= cabe_df.cod_cliente.astype(str)
    # df['filename'] = df['filename'].map(lambda x: str(x)[:-4])

    cabe_df['cod_cliente'] = cabe_df['cod_cliente'].str[:-1]
    cli_df['codcliente'] = cli_df['codcliente'].str[:-1]

    deta_df_type=deta_df.dtypes
    cli_df_type=cli_df.dtypes
    demapas_df_type=demapas_df.dtypes

    # cabe_df['cod_cliente']=int(cabe_df['cod_cliente']/10)
  
  #  print(cli_df_type)
  #  print("\n"*2)
  #  print(demapas_df_type)

    cabe_df_not=cabe_df[~cabe_df.cod_cliente.isin(demapas_df.cod_cliente)]
    cabe_df_in=cabe_df[cabe_df.cod_cliente.isin(demapas_df.cod_cliente)]
 
    # deta_df_not=deta_df[~deta_df.revend.isin(demapas_df.cod_cliente)]
    deta_df_not=deta_df[deta_df.n_comp.isin(cabe_df_not.n_comp)]
    #deta_df_in=deta_df[deta_df.revend.isin(demapas_df.cod_cliente)]
    deta_df_in=deta_df[deta_df.n_comp.isin(cabe_df_in.n_comp)]
    
 
    # Cambio los tipo sde datos para que no ponga comillas a los numericos
    # Las que están dentro de las lista de Mapas
    cabe_df_in.orden=cabe_df_in.orden.astype(int)
    cabe_df_in.cod_cliente=cabe_df_in.cod_cliente.astype(int)
    cabe_df_in.figura=cabe_df_in.figura.astype(int)
    cabe_df_in.importe=cabe_df_in.importe.astype(float)
    cabe_df_in.bonif_sin_imp=cabe_df_in.bonif_sin_imp.astype(float)
    cabe_df_in.imp_gravado=cabe_df_in.imp_gravado.astype(float)
    cabe_df_in.imp_exento=cabe_df_in.imp_exento.astype(float)
    cabe_df_in.imp_iva=cabe_df_in.imp_iva.astype(float)
    cabe_df_in.montib=cabe_df_in.montib.astype(float)
    cabe_df_in.boniflibro=cabe_df_in.boniflibro.astype(float)
    cabe_df_in.bonifivadic=cabe_df_in.bonifivadic.astype(float)
    cabe_df_in.zona=cabe_df_in.zona.astype(int)
    # Los que NO estan dentro de la lista de Mapas
    cabe_df_not.orden=cabe_df_not.orden.astype(int)
    cabe_df_not.cod_cliente=cabe_df_not.cod_cliente.astype(int)
    cabe_df_not.figura=cabe_df_not.figura.astype(int)
    cabe_df_not.importe=cabe_df_not.importe.astype(float)
    cabe_df_not.bonif_sin_imp=cabe_df_not.bonif_sin_imp.astype(float)
    cabe_df_not.imp_gravado=cabe_df_not.imp_gravado.astype(float)
    cabe_df_not.imp_exento=cabe_df_not.imp_exento.astype(float)
    cabe_df_not.imp_iva=cabe_df_not.imp_iva.astype(float)
    cabe_df_not.montib=cabe_df_not.montib.astype(float)
    cabe_df_not.boniflibro=cabe_df_not.boniflibro.astype(float)
    cabe_df_not.bonifivadic=cabe_df_not.bonifivadic.astype(float)
    cabe_df_not.zona=cabe_df_not.zona.astype(int)
    # los que estan dentro de la lista de Mapas 
    deta_df_in.orden=deta_df_in.orden.astype(int)
    deta_df_in.renglon=deta_df_in.renglon.astype(int)
    deta_df_in.cantidad=deta_df_in.cantidad.astype(int)
    deta_df_in.importe_neto=deta_df_in.importe_neto.astype(float)
    deta_df_in.precio_neto=deta_df_in.precio_neto.astype(float)
    deta_df_in.porc_iva=deta_df_in.porc_iva.astype(float)
    deta_df_in.precio_lista=deta_df_in.precio_lista.astype(float)
    deta_df_in.total_renglon=deta_df_in.total_renglon.astype(float)
    # deta_df_in.revend=deta_df_in.revend.astype(int)
    # Los que no estan dentro de lal lista de Mapas 
    deta_df_not.orden=deta_df_not.orden.astype(int)
    deta_df_not.renglon=deta_df_not.renglon.astype(int)
    deta_df_not.cantidad=deta_df_not.cantidad.astype(int)
    cabe_df_not.importe_neto=deta_df_not.importe_neto.astype(float)
    deta_df_not.precio_neto=deta_df_not.precio_neto.astype(float)
    deta_df_not.porc_iva=deta_df_not.porc_iva.astype(float)
    deta_df_not.precio_lista=deta_df_not.precio_lista.astype(float)
    deta_df_not.total_renglon=deta_df_not.total_renglon.astype(float)
    # deta_df_not.revend=deta_df_not.revend.fillna(0).astype(int)

    # Agrego el cliente una vez que quite el digito verificador del Nro de Cliente
    # cli_df.fecalta=cli_df.fecalta.astype('datetime64')
    cli_df['fecalta'] = pd.to_datetime(cli_df['fecalta'], errors='coerce')
    cli_df.tipdoc=cli_df.tipdoc.fillna(0).astype(int)
    cli_df.docnro=cli_df.docnro.fillna(0).astype(int)
    cli_df.altura=cli_df.altura.fillna(0).astype(int)
#    cli_df.piso=cli_df.piso.fillna(0).astype(int)
    cli_df.codpost=cli_df.codpost.fillna(0).astype(int)
    cli_df.telefono=cli_df.telefono.fillna(0).astype('int64')
    cli_df.cat_Iva=cli_df.cat_Iva.astype(int)
    cli_df.nucuil=cli_df.nucuil.fillna(0).astype(int)

    deta_df_type=deta_df.dtypes
    cli_df_type=cli_df.dtypes
    # print(cli_df_type)

    cabe_in_salida= rutasubida + "C" + mifecha + "_IN" + mizona + ".csv"
    deta_in_salida= rutasubida + "D" + mifecha + "_IN" + mizona + ".csv"
    cabe_not_salida= rutasubida + "C" + mifecha + "_NOT" + mizona + ".csv"
    deta_not_salida= rutasubida  + "D" + mifecha + "_NOT" + mizona + ".csv"
    cli_salida=  rutasubida + "CLI" + mifecha + "_" + mizona + "Cruzados.csv"
    
    #print(deta_df_not)
    #print(deta_df_in)

    cabe_df_in.to_csv(cabe_in_salida,quoting=csv.QUOTE_NONNUMERIC, index=False, header=True, )

    deta_df_in.to_csv(deta_in_salida,quoting=csv.QUOTE_NONNUMERIC, index=False, header=True, )

    cabe_df_not.to_csv(cabe_not_salida,quoting=csv.QUOTE_NONNUMERIC, index=False, header=True, )

    deta_df_not.to_csv(deta_not_salida,quoting=csv.QUOTE_NONNUMERIC, index=False, header=True, )

    cli_df.to_csv(cli_salida,quoting=csv.QUOTE_NONNUMERIC, index=False, header=True, date_format='%Y-%m-%d')


    #to_csv('cabe_in_salida.csv',doublequote=True,index =False, header=True)

    # print(deta_df)

    # print(cabe_df_not)
    # print("\n"*2)
    # print(cabe_df)

    # print(deta_df_not)
    # print("\n"*2)
    # print(cli_df)

else :
    print ("Faltan argumentos")

    # print(cabe_df)






