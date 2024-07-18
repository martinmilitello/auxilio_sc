import pandas as pd

# Ejemplo del DataFrame df_detaCSV con la estructura proporcionada
df_detaCSV = pd.DataFrame({
    'orden': [1, 2, 3],
    'n_comp': ['A1', 'A2', 'A3'],
    'renglon': [1, 1, 1],
    'cod_art': ['5/404327-7', '5/404329-3', '5/406401-5'],
    'cantidad': [10, 20, 30],
    'importe_neto': [100.0, 200.0, 300.0],
    'precio_neto': [10.0, 20.0, 30.0],
    'porc_iva': [21.0, 21.0, 21.0],
    'adicional': [0.0, 0.0, 0.0],
    'precio_lista': [12.0, 22.0, 32.0],
    'total_renglon': [120.0, 240.0, 360.0],
    'cuales': ['A', 'B', 'C'],
    'revend': [1, 1, 1],
    'precio_neto_modificado': [11.0, 21.0, 31.0]
})

# DataFrame df_detalle proporcionado
df_detalle = pd.DataFrame({
    'DESCRIPCIO': ['COMPOTERA GLAM AUTUMN 500ML CI', 'COMPOTERA GLAM AUTUMN 500ML RO', 'TARRO NOAH 750 ML COL ROSA PAL', 
                   'TARRO NOAH 750 ML COL VISON', 'TARRO NOAH 750 ML COL BERMELLO'],
    'articulo': ['5/404327-7', '5/404329-3', '5/406401-5', '5/406398-1', '5/406402-7']
})

# Realizar el merge
df_merged = pd.merge(df_detaCSV, df_detalle[['articulo', 'DESCRIPCIO']], left_on='cod_art', right_on='articulo', how='left')

# Reemplazar 'cod_art' por 'DESCRIPCIO'
df_merged['cod_art'] = df_merged['DESCRIPCIO']

# Eliminar columnas no deseadas
df_resultado = df_merged.drop(columns=['articulo', 'DESCRIPCIO'])

# Mostrar el resultado final
print(df_resultado)
