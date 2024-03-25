import pandas as pd
import matplotlib.pyplot as plt
import base64
import io

data = {'Nombre': ['Alice', 'Bob', 'Charlie'],
        'Edad': [25, 30, 22]}

df = pd.DataFrame(data)

# Imprimir el DataFrame
print(df)

# Generar un gráfico simple
ax = df.plot(kind='bar', x='Nombre', y='Edad')
plt.title('Edades de Personas')
plt.xlabel('Nombre')
plt.ylabel('Edad')

# Guardar la imagen generada
buffer = io.BytesIO()
plt.savefig(buffer, format='png')
buffer.seek(0)

image_base64 = base64.b64encode(buffer.read()).decode('utf-8')

# Imprimir la representación base64 de la imagen
print("Base64Image:")
print(image_base64)
'''
def calcular_algo():
    resultado = "Esto es el resultado desde Python y lo veremos en una vista C#"
    return resultado

print(calcular_algo())
'''