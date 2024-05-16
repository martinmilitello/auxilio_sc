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

try:
    with conexion.cursor() as cursor:
#               "cursor.execute('SET NOCOUNT ON; EXEC schema.proc @muted = 1')
        consultaR="select * from GVA14"
        df_clie = pd.read_sql_query(consultaR, conexion)

    
except Exception as e:
        print("Ocurrió un error al insertar: ", e)
finally:
        #conexion.close()
        conexion.commit()
        cursor.close()            

print(df_clie)