import pandas as pd
import glob, os

# Directorio donde se encuentran los archivos Excel
directorio = "C:\\Bancos\\electronico\\"

# Obtener el último componente de la ruta (el nombre del directorio)
nombre_directorio = directorio.split("\\")[2]

# Lista para almacenar los DataFrames de cada archivo
dfs = []

# Nuevos nombres para las columnas (ajusta esto a tus necesidades)
nuevos_nombres = ['N_documento', 'Subtipo', 'Fecha_Contabili', 'Importe_moneda_local', 'Tipo', 'Periodo', 'AnioCampania', 'ZONA']

# Recorrer todos los archivos Excel en el directorio
for archivo in glob.glob(directorio + "*.xlsx"):
    # Leer el archivo Excel y asegurarse de que 'ZONA', 'N_documento' y 'AnioCampania' se lean como texto
    df = pd.read_excel(archivo, dtype={'ZONA': str, 'N_documento': str, 'AnioCampania': str})
    
    # Renombrar las columnas (si es necesario)
    df.columns = nuevos_nombres
    
    # Convertir las columnas 'ZONA', 'N_documento' y 'AnioCampania' a string y asegurarse que tengan el formato adecuado
    df['ZONA'] = df['ZONA'].apply(lambda x: str(x).split('.')[0].zfill(3) if pd.notnull(x) else '')  # Asegura que 'ZONA' tenga 3 dígitos
    df['N_documento'] = df['N_documento'].apply(lambda x: str(x).split('.')[0] if pd.notnull(x) else '')  # Convierte N_documento a texto
    df['AnioCampania'] = df['AnioCampania'].apply(lambda x: str(x).split('.')[0] if pd.notnull(x) else '')  # Convierte AnioCampania a texto

    # Convertir la columna 'Periodo' al formato 'YYYYMM'
    df['Periodo'] = pd.to_datetime(df['Periodo'], errors='coerce').dt.strftime('%Y%m')

    dfs.append(df)

# Concatenar todos los DataFrames en uno solo
df_final = pd.concat(dfs, ignore_index=True)

# Guardar el DataFrame final como un nuevo archivo CSV
os.chdir(directorio)
df_final.to_csv(nombre_directorio + ".csv", index=False)

print("Todos los archivos CSV se han combinado en " + nombre_directorio + ".csv")
