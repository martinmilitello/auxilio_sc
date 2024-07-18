import pyodbc
direccion_servidor = 'ms40003.vfc.com.ar'    #'LT00149\LT00149'
nombre_bd = 'LADY_WAY_SRL'
nombre_usuario = 'Axoft'
password = 'Axoft'
try:
    # conexion = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' +
    #                         direccion_servidor+';DATABASE='+nombre_bd+';Trusted_Connection=yes;')
    # OK! conexión exitosa

    conexion = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + 
                         direccion_servidor + ';DATABASE=' + nombre_bd + ';UID=' + 
                         nombre_usuario + ';PWD=' + password + ';')
except Exception as e:
    # Atrapar error
    print("Ocurrió un error al conectar a SQL Server: ", e)

