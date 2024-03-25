import pandas as pd

# Ruta al archivo TXT
ruta_archivo = "subidasr\\PSTD20231215_030514Cabecera.txt"

# Lee el archivo TXT con Pandas


# Imprime el dataframe
df_nuevo = df[["ZONA", "REVEND", "col3","col4","col5","col6","col7","col8","col9","IMPORTE","col11","col12","col13","col14","col15","PROVINCIA","col17","col18","col19","col20","col21","col22","col23"]].copy()
print(df_nuevo)

df_nuevo = df.iloc[:, [9, 16]].copy()

suma_deseada = 400000
factor_ajuste = suma_deseada / df_nuevo[9].sum()
df_nuevo[9] = df_nuevo[9] * factor_ajuste

print(df_nuevo)

import pandas as pd

# Lees el archivo CSV
archivo_csv = "subidasr\\PSTD20231215_030514Cabecera.txt"
df = pd.read_table(ruta_archivo, sep=";")

# Inicializas las variables
total_importe = 0
registros_seleccionados = []

# Iteras sobre los registros del DataFrame
for index, row in df.iterrows():
    if total_importe + row['Importe'] <= 40000 and row['provincia'] == 1:
        # Agregas el registro al resultado
        registros_seleccionados.append(row)
        
        # Actualizas el total_importe
        total_importe += row['Importe']

# Creas un nuevo DataFrame con los registros seleccionados
df_resultado = pd.DataFrame(registros_seleccionados)

# Guardas el nuevo DataFrame en un nuevo archivo CSV
archivo_resultado = 'resultado.csv'
df_resultado.to_csv(archivo_resultado, index=False)

print(f"Registros seleccionados guardados en {archivo_resultado}")
