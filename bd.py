import pyodbc
direccion_servidor = ''
nombre_bd = 'VIOLETTAPRD'
nombre_usuario = 'oscar'
password = 'Inicio.01'
try:
    conexion = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' +
                              direccion_servidor+';DATABASE='+nombre_bd+';Trusted_Connection=yes;')
    # OK! conexión exitosa
except Exception as e:
    # Atrapar error
    print("Ocurrió un error al conectar a SQL Server: ", e)

