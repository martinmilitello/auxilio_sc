try:
    import os
    import sys
    from datetime import datetime
    # import smbclient
    # from smb.SMBConnection import SMBConnection
    # from smbclient import SambaClient

    from smb.SMBConnection import SMBConnection

except ImportError:
    print("No se pudo importar una o varias bibliotecas de Python")




# Configura los parametros de conexion
SERVER_NAME  = 'ms10004.vfc.com.ar'
USERNAME  = 'mmilitello'
PASSWORD  = 'Violetta41'
SHARE_NAME = 'fileserver/grupales'
DOMAIN = 'VFC' # si aplica

server_name = "ms10004.vfc.com.ar"
share_name = "fileserver/grupales"
username = "mmilitello"
password = "Violetta41"

# Define los detalles del servidor y comparte la informacion
SERVER_NAME = 'ms10004.vfc.com.ar'
SHARE_NAME = 'fileserver'
'''
# Esta parte no funcionó ------------------------------------------------------------
try:
    # Conecta al servidor y autentica
    with SambaClient(server=SERVER_NAME, share=SHARE_NAME, username=USERNAME, password=PASSWORD, domain=DOMAIN) as client:
        # Lista los archivos en la carpeta
        file_stat = client.stat('/InterfacesSAP/INTPEDIDOS/C2023040400505.csv')
        print("Nombre de archivo: ", file_stat.name)
        print("Tamaño de archivo: ", file_stat.size)
        print("Fecha de creación: ", file_stat.create_time)
        print("Fecha de Ultima modificacin: ", file_stat.last_write_time)
except Exception as e:
    # Captura la excepcion y muestra el mensaje de error
    print("Error de conexion: ", str(e))
'''
try:
    # Establecer la conexión con el servidor SMB
    conn = SMBConnection(username, password, "cliente", server_name, use_ntlm_v2=True)
    conn.connect(server_name, 139)

    # Conectarse al recurso compartido
    share = conn.listPath(share_name, "/")

    # Listar los archivos del recurso compartido
    for file in share:
        print(file.filename)

    # Cerrar la conexión
    conn.close()

except Exception as e:
    print("Error: ", e)

# print("Hola estoy ejecutando desde PHP")