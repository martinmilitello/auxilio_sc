import re

# Abrir el archivo de texto
with open('PSTD20230427_151032posiciones.txt', 'r', encoding='utf-8') as archivo:
    # Leer el contenido del archivo
    contenido = archivo.read()

    # Definir una expresión regular para encontrar caracteres no válidos
    patron = re.compile(r'[^\x00-\x7F]+')

    # Función para limpiar una cadena de texto
    def limpiar_texto(cadena):
        return patron.sub(lambda x: f"{{{x.group()}}}", cadena)

    # Lista para almacenar los caracteres reemplazados
    caracteres_reemplazados = []

    # Aplicar la función de limpieza al contenido del archivo
    contenido_limpio = limpiar_texto(contenido)

    # Buscar los caracteres reemplazados y añadirlos a la lista
    for match in patron.finditer(contenido):
        caracteres_reemplazados.append(match.group())

# Abrir el archivo de texto en modo escritura y escribir el contenido limpio
with open('PSTD20230427_151032posiciones_limpio.txt', 'w', encoding='utf-8') as archivo_limpio:
    archivo_limpio.write(contenido_limpio)

# Imprimir la lista de caracteres reemplazados
print('Caracteres reemplazados:', caracteres_reemplazados)