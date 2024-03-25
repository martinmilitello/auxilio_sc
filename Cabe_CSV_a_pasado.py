import os
import shutil
from datetime import datetime

# Directorio de origen y destino
directorio_origen = r'Y:\\InterfacesSAP\\INTPEDIDOS'
directorio_destino = r'Y:\\InterfacesSAP\\INTPEDIDOS\\PASADO\\DICIEMBRE 2023'

# Obtener la fecha actual en el formato requerido (YYYYMMDD)
# fecha_actual = datetime.now().strftime('%Y%m%d')
fecha_actual = '20231229'

# Construir el nombre del archivo a buscar
prefijo_archivo = 'C' + fecha_actual + '00'

# Lista para almacenar los archivos a copiar
archivos_a_copiar = []

# Recorrer los archivos en el directorio de origen
for archivo in os.listdir(directorio_origen):
    if archivo.startswith(prefijo_archivo) and os.path.isfile(os.path.join(directorio_origen, archivo)):
        archivos_a_copiar.append(archivo)

# Verificar si hay archivos para copiar
if archivos_a_copiar:
    # Verificar si el directorio destino no existe y crearlo si es necesario
    if not os.path.exists(directorio_destino):
        os.makedirs(directorio_destino)

    # Copiar los archivos al directorio destino
    for archivo in archivos_a_copiar:
        origen_archivo = os.path.join(directorio_origen, archivo)
        destino_archivo = os.path.join(directorio_destino, archivo)

        # Verificar si el archivo no existe en el directorio destino antes de copiar
        if not os.path.exists(destino_archivo):
            shutil.copy2(origen_archivo, destino_archivo)
            print(f'Archivo copiado: {archivo}')
        else:
            print(f'El archivo ya existe en el directorio destino: {archivo}')
else:
    print('No hay archivos para copiar.')