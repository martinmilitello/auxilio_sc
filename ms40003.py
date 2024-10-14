#----------------------------------------------------------------------------------#
# Genera juego de Cabeceras y detalles para la presentacion del formulario 722 
# para poder ingresar en la provincia de SAlta.
# Debe haberse ingresado en Tango los CSV de la zona 704 para obtener los N° de facturas correspondientes
# cabecera : 8|0003|00030541|
# Detalle : CR.HIDRATANTE MATIFICANTE CLEA|3599.99|3|unidad|


#----------------------------------------------------------------------------------#
import numpy as np
import pandas as pd
import glob, os
import pyodbc
from datetime import datetime, timedelta
import csv


from bd import conexion   # bd_violettaprd
###### Datos a ingresar 
fecha = '20240927' # Se ingresa la fecha 
diaDesde = '20' # El día desde que se comienza la busqueda de la facturacion a Tango
######
fecha_dt = datetime.strptime(fecha, '%Y%m%d')
anio=fecha[:4]
mes=fecha[4:6]
dia=fecha[6:]
zona = '704'
# fdesde = "'20240720'"
# fhasta = "'20240726'"
fdesde = f"'{anio}{mes}{diaDesde}'"
fhasta_dt = fecha_dt - timedelta(days=4)
fhasta = f"'{fecha}'"

filename_salida = 'detalles_Salvador_Mazza_CSV.txt'

try:
    with conexion.cursor() as cursor:
#               "cursor.execute('SET NOCOUNT ON; EXEC schema.proc @muted = 1')
        consultaR=f"""
                        select '8' as tipo_fac,  '0003' as pto_vta , SUBSTRING(n_comp, 7, LEN(n_comp)- 1) as comprobante 
                        from gva12 where COD_VENDED = {zona}  and FECHA_EMIS between {fdesde} and {fhasta}
                """   
        df_cabe = pd.read_sql_query(consultaR, conexion)
        
        df_cabe_1 = df_cabe
        print (df_cabe_1)
        os.chdir('zona703\\')

      
        # for index, row in df_cabe.iterrows():
        filename = f'cabecera_Salvador_Mazza.txt'
        
           
        df_cabe_1.to_csv(filename, index=False, sep='|', header=False, quoting=csv.QUOTE_NONE )
            
        with open(filename, 'r') as file:
               lines = file.readlines()

        with open(filename, 'w') as file:
               for line in lines:
                    file.write(line.strip() + '|\n')
   
        consultaQ = f"""
        
                   
                        SELECT gv.COD_ARTICU,
                        gv12.n_comp,
                        st.DESCRIPCIO,
                        1 AS Precio,
                        'unidad' AS unidad_medida,
                        gv.CANTIDAD,
                        isnull(j.articulo,'1') as articulo
                        FROM gva53 gv
                        RIGHT JOIN STA11 st ON gv.COD_ARTICU = st.COD_ARTICU
                        INNER JOIN gva12 gv12 ON gv12.n_comp = gv.N_COMP
                        OUTER APPLY (
                        SELECT TOP 1 isnull(desc_adic,'1') AS articulo
                        FROM gva45 
                        WHERE n_comp = gv12.n_comp
                         AND desc_adic COLLATE Latin1_General_BIN LIKE '%' + LEFT(gv.COD_ARTICU, 10) + '%'
                        ) j
                        WHERE gv.FECHA_MOV BETWEEN  {fdesde} and {fhasta}
                         AND COD_VENDED =  {zona}
                         AND gv.PRECIO_PAN > 1
                         AND gv.COD_ARTICU NOT IN ('04','02', '03', '06')
                         order by gv12.n_comp;

        """
       
        # PRECIO_PAN reemplazar por IMP_NETO_P

        df_detalle = pd.read_sql_query(consultaQ, conexion)

        
        archi= 'D'+anio+mes+dia+'_IN_'+zona+'.csv'
        df_detaCSV=pd.read_csv(archi, delimiter = ",")

        mask = df_detaCSV["precio_neto"] > 1.00
        # df_detaCSV["precio_neto_modificado"] = df_detaCSV["importe_neto"] / 1.21
        df_detaCSV["precio_neto_modificado"] = (df_detaCSV["importe_neto"] / df_detaCSV["cantidad"]) / 1.21
        # df_detaCSV["precio_neto_modificado"] = df_detaCSV["precio_neto"].where(mask, df_detaCSV["precio_neto"] / 1.21)

                # Verificar que las columnas existen
        if 'cod_art' not in df_detaCSV.columns:
               print("La columna 'cod_art' no existe en df_detaCSV")
        else:
               print("La columna 'cod_art' existe en df_detaCSV")

        if 'articulo' not in df_detalle.columns:
               print("La columna 'articulo' no existe en df_detalle")
        else:
               print("La columna 'articulo' existe en df_detalle")

        try:
                df_merged = pd.merge(df_detaCSV, df_detalle[['articulo', 'DESCRIPCIO']], left_on='cod_art', right_on='articulo', how='left')
        
        # Reemplazar 'cod_art' por 'DESCRIPCIO'
                # df_merged['cod_art'] = df_merged['DESCRIPCIO']
                df_merged['cod_art'] = df_merged['DESCRIPCIO'].fillna(df_merged['cod_art'])
        
        # Eliminar columnas no deseadas
                df_resultado = df_merged.drop(columns=['articulo', 'DESCRIPCIO']).drop_duplicates()
                df_resultado.sort_values(by='n_comp', ascending=True)
        
        # Mostrar el resultado final
                print(df_resultado)
        except Exception as e:
                print(f"Ocurrió un error con el merge: {e}")


        df_detaCSV['cod_art'] = df_detaCSV['cod_art'].str.strip().str.lower()
        df_detalle['articulo'] = df_detalle['articulo'].str.strip().str.lower()

        # df_merged = pd.merge(df_detaCSV, df_detalle, left_on='articulo', right_on='cod_art', how='left')
        # print(df_merged)
        # df_combinado = df_detalle.merge(df_detaCSV, on='articulo', how='left')
        # print (df_combinado)
        
        # df_detalle.to_csv("detalle_Tango.csv", index=False, sep=',')
        # print(df_detaCSV)
        print(df_detaCSV.info())
        print(df_detalle.info())
        
        df_archivosalta = df_resultado.drop(columns=['importe_neto','precio_neto','porc_iva','adicional','precio_lista','total_renglon','cuales','revend','renglon','orden'])
        
        df_archivosalta.sort_values(by=["n_comp"], ascending=False)

        df_archivosalta = df_archivosalta.drop(columns=['n_comp'])
        # cambio los encabezados de nombre
        df_archivosalta = df_archivosalta.rename(columns={
                'cod_art': 'descripcion',
                'precio_neto_modificado': 'precio'
        })
        # limpio el string y agrego campo unidad
        df_archivosalta['descripcion'] = df_archivosalta['descripcion'].str.replace(r"\(.*\)", "", regex=True).str.strip()
        df_archivosalta["unidad_medida"] = "unidad"

        # ordeno por n_comp
        column_order = [
        'descripcion', 'precio', 'unidad_medida', 'cantidad'
        ]
        df_archivosalta = df_archivosalta[column_order]

        # quito los 0.01
        df_archivosalta_1 = df_archivosalta[df_archivosalta["precio"] >= 1]

        df_archivosalta_1['precio'] = df_archivosalta_1['precio'].astype(float)
        df_archivosalta_1['cantidad'] = df_archivosalta_1['cantidad'].astype(int)

        df_archivosalta_1['precio'] = df_archivosalta_1['precio'].apply(lambda x: f'{x:.2f}')
        df_archivosalta_1['cantidad'] = df_archivosalta_1['cantidad'].apply(lambda x: f'{int(x)}')



        # Genero la version definitiva del archivo cruzandolo con el CSV de la zona     
        df_archivosalta_1.to_csv(filename_salida, index=False, sep='|', header=False) 
        with open(filename_salida, 'r') as file:
                lines = file.readlines()

        with open(filename_salida, 'w') as file:
                for line in lines:
                        file.write(line.strip() + '|\n')



                # Definir el nombre del archivo CSV
        filename = f'detalles_Salvador_Mazza.txt'
                # quito la columna n_comp
        df_filtered = df_detalle.drop(columns=['n_comp'])
                # Guardar el DataFrame filtrado en un archivo CSV
        df_filtered['Precio'] = df_filtered['Precio'].astype(float)
        df_filtered['CANTIDAD'] = df_filtered['CANTIDAD'].astype(int)

        df_filtered['Precio'] = df_filtered['Precio'].apply(lambda x: f'{x:.2f}')
        df_filtered['CANTIDAD'] = df_filtered['CANTIDAD'].apply(lambda x: f'{int(x)}')
                
        # Genero la version SQL solamente en la que hay que descontar las bonificaciones
        df_filtered.to_csv(filename, index=False, sep='|', header=False)

                # Agrego el | al final de cada linea
        with open(filename, 'r') as file:
                lines = file.readlines()

        with open(filename, 'w') as file:
                for line in lines:
                        file.write(line.strip() + '|\n')
                
        print(f"Archivo CSV generado para : {filename}")

        
        filename_cabe = f'cabeceras_zona.csv'
        
        df_cabe.to_csv(filename_cabe, index=False, sep='|')
        # df_filtered.to_csv(filename, index=False, sep='|', header=False)

        print(f"Archivo CSV generado para: {filename_cabe}")
        
except Exception as e:
        print("Ocurrió un error con el dataframe: ", e)
finally:
        #conexion.close()
        conexion.commit()
        cursor.close()            

