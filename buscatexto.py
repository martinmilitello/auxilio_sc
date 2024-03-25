import os
import re

def buscar_cadena_en_archivos(carpeta, cadena):
    # Obtener la lista de archivos en la carpeta
    archivos = [os.path.join(carpeta, archivo) for archivo in os.listdir(carpeta) if os.path.isfile(os.path.join(carpeta, archivo))]

    # Iterar sobre cada archivo
    for archivo in archivos:
        try:
            with open(archivo, 'r', encoding='utf-8') as file:
                # Leer el contenido del archivo
                contenido = file.read()
                
                # Buscar la cadena en el contenido del archivo
                if re.search(cadena, contenido):
                    print(f'Se encontró la cadena "{cadena}" en el archivo: {archivo}')
        except Exception as e:
            print(f'Error al leer el archivo {archivo}: {str(e)}')

# Ruta de la carpeta a buscar
carpeta_a_buscar = r'Y:\InterfacesSAP\INTPEDIDOS\BACKUP'

# Cadena a buscar
cadena_a_buscar = '203823'

# Llamar a la función de búsqueda
buscar_cadena_en_archivos(carpeta_a_buscar, cadena_a_buscar)

