import datetime        
from datetime import datetime
from datetime import date
import numpy as np
from numpy import nan
import pandas as pd
import glob, os
from tkinter import messagebox as MessageBox
from tkinter import *
from tkinter import ttk
from pandas import concat
# ----------- coneccion a SQL
import pyodbc
direccion_servidor = 'LT00148'
nombre_bd = 'bodysoul' 
try:
    conexion = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' +
                              direccion_servidor+';DATABASE='+nombre_bd+';Trusted_Connection=yes;')
    print('OK! conexión exitosa')  
except Exception as e:
    # Atrapar error
    print("Ocurrió un error al conectar a SQL Server: ", e)

#query = "select * from objetivos where periodo = (select top 1 max(periodo) from objetivos where montofacturacion > 0)"
#dfobjetivo = pd.read_sql(query, conexion, params=[])
#print(query)    
#===================================================================================================================================================================================#
# Este programa debe implementarse en el disparador de windows, para que lo ejecute 15' antes de la importacion de los archivos planos que deja SAP para ser levantados por el SC   #
# Su funcion es seleccionar de cualquier zona perteneciente a Gran Bs As la cantidad de revendedoras que necesite para cubrir el adicional calculado mediante un algoritmo          #
# Es para usar mientras Body se mantenga en letargo
#===================================================================================================================================================================================#
# Funciones ========================================================
def calcular_zcostot(row):
            if "Gastos Administrativos" in row['DESCRI']: 
                return 0
            else:
                return (row['PRENP'] - (row['PRENP'] * row['BONIF'] / 100)) * row['CANT']
            
def calcular_GRCH(row):
            if row['zcostot'] > limiva:                                           ############### OJO 60000 probar con 4200
                return 'G'
            else:
                return 'C'
            
def calcular_boncosme(row):
            if "ZCOS" in row['GRUPO']: 
                return (row['PRENP'] * row['BONIF'] / 100) * row['CANT']  
            else:
                return 0 
            
def calcular_bonhogar(row):
            if "ZHOG" in row['GRUPO']: 
                return (row['PRENP'] * row['BONIF'] / 100) * row['CANT']  
            else:
                return 0  
            
def calcular_bonotros(row):
            if "ZCOS" not in row['GRUPO'] and "ZHOG" not in row['GRUPO']: 
                return (row['PRENP'] * row['BONIF'] / 100) * row['CANT']  
            else:
                return 0      
              
def leer_ultimos_tres(archivo):
  try:
    datos = np.loadtxt(archivo)
    longitud = datos.shape[0]
    ultimos_tres = datos[longitud-3:longitud]
    return ultimos_tres
  except FileNotFoundError:
    lista = [0, 0, 0]
    datos = np.array(lista)
    np.savetxt(archivo, datos, newline=" ", fmt="%d")
    return lista

def graba_ultimos_tres(archivo, vale1,vale2,vale3):
  try:
    datos = np.loadtxt(archivo)
    
    lista = [vale1,vale2,vale3]
    my_list=np.array(lista)
    lista=np.nan_to_num(my_list)
    
    if datos[0]==0 and datos[1]==0 and datos[2]==0:
      datos = np.array(lista)
      np.savetxt(archivo, datos, newline=" ", fmt="%d")  
    else:
      datos=np.insert(datos, datos.shape[0], np.array(lista), 0)
      a = np.array(datos)                            #
      np.savetxt(archivo, a, newline=" ", fmt="%d")  #
    return
  except FileNotFoundError:
    print('Error')
    return 

def redondear_decimal(df, columna):
    # Verifica
    if columna not in df.columns:
        print(f"La columna '{columna}' no existe en el DataFrame.")
        return df

    # Redondea si la columna es numérica
    if pd.api.types.is_numeric_dtype(df[columna]):
        df.loc[:, columna] = df[columna].round(2)

    # Convierte a string y formatea (si es necesario)
    if not pd.api.types.is_string_dtype(df[columna]):
        try:
            df.loc[:, columna] = df[columna].astype(str).str.format('.2f')
        except AttributeError:
            df.loc[:, columna] = df[columna].astype(float).apply('{:.2f}'.format)

    return df

def eliminar_decimal(df, columna):
    # Verifica
    if columna not in df.columns:
        print(f"La columna '{columna}' no existe en el DataFrame.")
        return df

    # Aplica (Corrección usando .loc)
    df.loc[:, columna] = df[columna].astype(str).str.replace(r'\.0$', '', regex=True)
    return df

def completar_con_ceros(df, columna):
    # Verifico
    if columna not in df.columns:
        print(f"La columna '{columna}' no existe en el DataFrame.")
        return df
    # Aplico
    df[columna] = df[columna].astype(str).str.zfill(10)
    return df

def completar_con_2_ceros(df, columna):
    # Verifico
    if columna not in df.columns:
        print(f"La columna '{columna}' no existe en el DataFrame.")
        return df
    # Aplico
    df[columna] = df[columna].astype(str).str.zfill(2)
    return df
# Fin Funciones ==================================================================

now = datetime.now()
eldi=(f'{now.day:02}')
elme=(f'{now.month:02}')
elan=str(now.year)
elamd=elan+elme+eldi
lahor=datetime.now().strftime('%Y-%m-%d %H%M%S')
lahor=lahor[11:20]
#===================================================================== LOG
milog="guarda_log.txt"
ultimos_tres = leer_ultimos_tres(milog)
qdiaes = ultimos_tres[0]
yahice = ultimos_tres[1]
ivahastahoy = ultimos_tres[2]
datos = np.loadtxt(milog)
#============================================= leer SQL objetivos =======================================================
#now = datetime.now()
#qfecha = now.strftime("%Y-%m-%d")
#qfecha='20231218'
#query = "SELECT * FROM objetivos WHERE vigenciahasta >= ? AND vigenciadesde <= ?"
#dfobjetivo = pd.read_sql(query, conexion, params=[qfecha, qfecha]) 
       
query = "select * from objetivos where periodo = (select top 1 max(periodo) from objetivos where montofacturacion > 0)"
dfobjetivo = pd.read_sql(query, conexion, params=[])
#--------------------------------------------------- rescata datos y calcula dias de actividad en el mes: diashd
porgtos=float(dfobjetivo.PORC_GTOS_ADMIN/100)
fe_obje_de=dfobjetivo.VigenciaDesde
fe_obje_de = datetime.strftime(fe_obje_de[0], '%Y-%m-%d')

fe_obje_ha=dfobjetivo.VigenciaHasta
fe_obje_ha = datetime.strftime(fe_obje_ha[0], '%Y-%m-%d')

fechaAMD = datetime.strptime(fe_obje_de, "%Y-%m-%d")
afede = str(fechaAMD.year)
maskcal=np.busdaycalendar(holidays=[afede+'-01-01',afede+'-02-12',afede+'-02-13',afede+'-03-24',afede+'-03-29',afede+'-04-02',
    afede+'-05-01',afede+'-05-25',afede+'-06-20',afede+'-07-09',afede+'-12-08',afede+'-12-25'])
diashd=np.busday_count(
      fe_obje_de, fe_obje_ha, 
      busdaycal=maskcal)
#----------------------------------------------------que dia es hoy
hoyes = date.today()
qdiaes=int(format(hoyes.day))
#----------------------------------------------------Monto
Montoobje=float(dfobjetivo.MontoFacturacion)
pordia=Montoobje/diashd           
yahice=float(dfobjetivo.ACUMULADO)     

faltamon=Montoobje-yahice         
cubridias=round(yahice/pordia,0)      
faldia=diashd-cubridias                                                               
if faltamon==0 and faldia==0:
    quieromon=0
else:    
    quieromon=float(faltamon/faldia)         
if quieromon> faltamon:
    quieromon=faltamon
#--------------------------------------------------- Tasas de IVA 
unatasa = 1+(dfobjetivo.IVA/100)
iva2pura = dfobjetivo.IVAADIC
sumatasas = (1+(dfobjetivo.IVA/100))*(1+(dfobjetivo.IVAADIC/100))
tasa21= dfobjetivo.IVA/100
tasa10=dfobjetivo.IVAADIC /100
#--------------------------------------------------- IVA Adic-------------------------------------------------------------
limiva=float(dfobjetivo.MONTOIVA)              
adiclimiva=float(limiva-((limiva/sumatasas)*unatasa))   
objeperc=float(dfobjetivo.MontoIVAPercepcion)   
#objeperc=dfobjetivo.MontoIVAPercepcion[0]    
pordiaiva=objeperc/diashd        
ivahastahoy=float(dfobjetivo.ACUMULADOIVA)        
falivaun=float(objeperc-ivahastahoy)                
cubridiasiva=round(ivahastahoy/pordiaiva,0)       
faldiaiva=diashd-cubridiasiva                   
falivadi=float(round(falivaun/faldiaiva,0))
#===================================================================== 
if falivadi < adiclimiva:                         
    if objeperc-ivahastahoy<adiclimiva:
        pordiaiva=0
    else:
        if  ivahastahoy>0:
            cadactosdias=round((diashd/(objeperc/adiclimiva)),0)       
            if round(cubridiasiva/cadactosdias,0)==round(qdiaes/cadactosdias,0) and qdiaes>=cubridiasiva:    
                pordiaiva=adiclimiva
            else:
                pordiaiva=0
        else:
            if objeperc>0 and qdiaes> 1 and round(diashd/(objeperc/adiclimiva),0)>=qdiaes :
                pordiaiva=adiclimiva
            else:
                pordiaiva=0
else:                                                         
    pordiaiva=falivadi
#====================================================================== 
montopadic=float(pordiaiva*iva2pura)      
if limiva>montopadic and montopadic>0:
    montopadic=limiva
    print(6)
if montopadic>quieromon:            
    if quieromon==faltamon:          
        quieromon=0
    else:                              
        if quieromon>0:           
            quieromon=quieromon/3 
else:
    if quieromon>montopadic and montopadic>0:            
        quieromon=quieromon/3     
quieromon=quieromon+montopadic    
#===============================================================LOG
yahice=yahice+quieromon
ivahastahoy=ivahastahoy+pordiaiva
lollama = graba_ultimos_tres(milog, qdiaes, yahice, ivahastahoy)
     
print('# Hoy: ', qdiaes, ' Obj.mont.hoy: ',int(quieromon), ' Ya hice mon: ', yahice, ' Adic p/hoy: ',int(pordiaiva),'Mont.iva bus : ',int(montopadic),' Ya hice IVA: ',ivahastahoy,' Dias cubiertos IVA: ', round(cubridiasiva,2), 
     ' Dias faltan IVA: ', round(faldiaiva,2)) 
#---------------------------------------------
##os.chdir('Y:\\INTPEDIDOS\\BKVJO\\')   ##sin acceso desde mi equipo
#os.chdir('entradas\\')
os.chdir('C:\\C#\\VENTASCLI\\')
trabajo=os.getcwd()
for archi in glob.glob("PSTD"+"*Cabecera.txt"):
    df_cabetxt=pd.read_csv(archi, delimiter = ";",  header=None)
    df_cabetxt.columns = ['ZONASEC','cod_cliente','C','D','E','F','G','H','I','apagar','iva','adic','M','N','O','CPROV','Q','boncos','bonres','T','U','V','W']
    
    indexNames = df_cabetxt[ df_cabetxt['cod_cliente'] > 0 ].index 
    qfecha=archi[4:12]
    qhora=archi[12:19]
    
    # Lectura del excel para recabar provincias a incluir---------------#
    dfpxlsx = pd.read_excel(io = "parametros"+".xlsx", sheet_name="Hoja1", usecols=["provincias","tomar_prov"]) 
    tomar_prov = dfpxlsx['tomar_prov']
    tomar_prov = dfpxlsx[tomar_prov == "X"]
    columnas = tomar_prov.columns
    columnas = columnas.tolist()
    valores = tomar_prov.values
    provx = []
    for i in tomar_prov.index: 
        proveleg=tomar_prov["provincias"][i]
        provx.extend([proveleg])               
    #-------------------------------------------------------------------#
    # 1=Gran Bs As   # 0=Capital Federal   
    filtered_df_esas = df_cabetxt.where(df_cabetxt['CPROV'].isin(provx))    
    filtered_df_esas['Zonas'] = filtered_df_esas['ZONASEC'].str[0:3]   
    df_cabes_esa_prov = filtered_df_esas.dropna(how='all')
    if df_cabes_esa_prov.empty:
        df_zona_cant=df_cabes_esa_prov
        print('Sin datos para Body')
    else:        
        df_zona_cant = df_cabes_esa_prov.groupby(['Zonas']).size().reset_index(name='cant')
        # en df_zona_cant tengo resumen por zona (de esas provincias) habiendo leido cabeceras del dia
        # debo obtener clientes en otro df de la extraccion (00 y 01) Ej: 168 son 14 rev
        #-------------------------------------------------------------
    df_clietxt=pd.read_csv("Cli_fact_"+qfecha+'.txt', delimiter = ";",  header=None)
    df_clietxt.columns = ['cod_cliente','DV','TIPREV','ZONASEC','T12','NOMBRE','TDOC','NDOC','DIRE','NDIRE',
    'KK1','KK2','KK3','ECALL','KK4','CP','CPROV','PROV','KK5','KK6','KK7','EXPLI', 'QSEYO']
    indexNames = df_clietxt[ df_clietxt['cod_cliente'] > 0 ].index 
    #-------------------------------------------------------------
    # ahora leo detalles (del mismo juego) y entrando por cada zona 
    for archid in glob.glob("PSTD"+qfecha+qhora+"posiciones.txt"):
        df_detatxt=pd.read_csv(archid, delimiter = ";",  header=None)
        df_detatxt.columns = ['ZONASEC','cod_cliente','DV','ARTICULO','DVPROD','TIPO','AC','AC1','CANT','NOSE1','ADIC','PRENP','IVA','DESCRI','NOSE2','NOSE3','NOSE4','BONIF','GRUPO']
        indexNamesd = df_detatxt[ df_detatxt['cod_cliente'] > 0 ].index 
                
        prime=0 
        if df_cabes_esa_prov.empty:
            print("No se encontraron datos para el cliente:")
            filtered_df_esasd = df_detatxt.fillna('No se encontraron datos')
            df_detas_esa_prov=filtered_df_esasd
            sras='0'
        else:            
            for i in range(len(df_cabes_esa_prov)):
                sras = df_cabes_esa_prov.iloc[i]['cod_cliente']
                filtered_df_esasd = df_detatxt.where(df_detatxt['cod_cliente'].isin([sras]))
                if prime == 0:
                    prime=1
                    df_detas_esa_prov = filtered_df_esasd.dropna(how='all')
                else:
                    df_detas_esa_prov = concat([df_detas_esa_prov, filtered_df_esasd.dropna(how='all')], ignore_index=True)            
                        
        # dejar solo detas cosme
        esegru='ZCOS'  

        filtered_df_esegru = df_detas_esa_prov.where(df_detas_esa_prov['GRUPO'].isin([esegru]))   
        df_detas_esa_prov = filtered_df_esegru.dropna(how='all')   

        # Obtener de registros de detalle la cantidad de articulos por cod_cliente
        df_detas_esa_prov_grp = df_detas_esa_prov.groupby('cod_cliente').size().reset_index(name='cant_detas')

        # Filtrar df_cabes_esa_prov por aquellos `cod_cliente` que tengan al menos 4 registros de detalle
        df_cabes_esa_prov_flt = df_cabes_esa_prov.merge(df_detas_esa_prov_grp, how='inner', left_on='cod_cliente', right_on='cod_cliente')
        df_cabes_esa_prov_flt = df_cabes_esa_prov_flt[df_cabes_esa_prov_flt['cant_detas'] >= 4]

        # ANECDOTICO:
        # mostrar cant de cabeceras ya depuradas por zona
        #df_zona_cant_flt = df_cabes_esa_prov_flt.groupby(['Zonas']).size().reset_index(name='kant')
        ###print(df_zona_cant_flt)

        # detalles correspondientes a cabes filtradas
        df_detas_esa_prov_flt = df_detas_esa_prov.merge(df_cabes_esa_prov_flt, how='inner', left_on='cod_cliente', right_on='cod_cliente')
        #print (df_detas_esa_prov_flt)
        
        # calcular plata por clientes desde detas sumados
        df_detas_esa_prov_flt['neto'] = df_detas_esa_prov_flt.apply(lambda row: row['PRENP'] - (row['PRENP'] * row['BONIF'] / 100), axis=1)

        # ANECDOTICO:
        #df_detas_esa_prov_flt.sort_values('Zonas','neto', inplace=True)  # sobre si mismo
        ###print (df_detas_esa_prov_flt)

        # Agrupa detalles con suma de netos
        df_detas_esa_prov_flt_plata = df_detas_esa_prov_flt.groupby('cod_cliente').agg({'neto': 'sum'}).reset_index()         
           
        #============================================= Inicio tratamiento =======================================================

        # Persigo adicional  
        # Ordena por neto descendente los detalles sumados por monto
        
        df_detas_esa_prov_flt_plata.sort_values(by = ['neto','cod_cliente'], axis=0, ascending = [False, True], inplace=True, ignore_index=True, key=None)

        conseguia=0     
        lista_sw = []

        for i in range(len(df_detas_esa_prov_flt_plata)):
            if df_detas_esa_prov_flt_plata.loc[i, 'neto'] >= limiva:
                if df_detas_esa_prov_flt_plata.loc[i, 'neto'] + conseguia <= montopadic * 1.1:
                    conseguia = conseguia + df_detas_esa_prov_flt_plata.loc[i, 'neto']
                    lista_sw.extend([df_detas_esa_prov_flt_plata['cod_cliente'][i], df_detas_esa_prov_flt_plata['neto'][i]])
        print(lista_sw)   # 
        
        # Ordena por neto ascendente los detalles sumados por monto
        df_detas_esa_prov_flt_plata.sort_values(by = ['neto','cod_cliente'], axis=0, ascending = [True, True], inplace=True, ignore_index=True, key=None)

        conseguim=conseguia
        quieromon=quieromon + montopadic
        for i in range(len(df_detas_esa_prov_flt_plata)):
            if df_detas_esa_prov_flt_plata.loc[i,'neto'] + conseguim <= quieromon:
                conseguim=conseguim + df_detas_esa_prov_flt_plata.loc[i,'neto']  
                lista_sw.extend([df_detas_esa_prov_flt_plata['cod_cliente'][i], df_detas_esa_prov_flt_plata['neto'][i]])
        print(lista_sw)   # OK: lista de 10 sras con 4 o + arts, de cualquier zona y todas llegan a 90000 $
        #-----------------------------------------------------
        ##os.chdir('Y:\\INTPEDIDOS\\BODY\\')
        #os.chdir('..\\salidas\\')
        os.chdir('C:\\C#\\VENTASCLI\\body_soul\\')
        # generar lote cli, cabe, deta para body de solo esas   
        filtered_df_esas = df_clietxt.where(df_clietxt['cod_cliente'].isin(lista_sw))
        df_sin_nan_esas = filtered_df_esas.dropna(how='all')  
        
        df_sin_nan_esas_copia = df_sin_nan_esas.copy()
        eliminar_decimal(df_sin_nan_esas_copia,'cod_cliente')       
        completar_con_ceros(df_sin_nan_esas_copia,'cod_cliente')        
        eliminar_decimal(df_sin_nan_esas_copia,'DV')
        eliminar_decimal(df_sin_nan_esas_copia,'T12')
        eliminar_decimal(df_sin_nan_esas_copia,'TDOC')
        eliminar_decimal(df_sin_nan_esas_copia,'NDOC')
        eliminar_decimal(df_sin_nan_esas_copia,'NDIRE')
        eliminar_decimal(df_sin_nan_esas_copia,'CP')
        eliminar_decimal(df_sin_nan_esas_copia,'CPROV')
        eliminar_decimal(df_sin_nan_esas_copia,'KK5')
        #====================================================Clientes Body a CSV ===========================================================
        df_sin_nan_esas_copia.to_csv("Cli_fact_"+qfecha+'.txt', header=None, index=None, sep=';', mode='w')
        # OK clientes body
        
        filtered_df_detas_esas = df_detatxt.where(df_detatxt['cod_cliente'].isin(lista_sw))
        df_body_esasd = filtered_df_detas_esas.dropna(how='all')
        df_body_esasd_copia = df_body_esasd.copy()
        # 
        df_body_esasdcos = df_body_esasd_copia.query('GRUPO == "ZCOS" | DESCRI.str.contains("Gastos Administrativos")')
        df_body_esasdcosnan = df_body_esasdcos.dropna(how='all')
        #=============================================================================
        if  df_body_esasdcosnan.empty:
            #====================================================Detalles Body a CSV ===========================================================
            df_body_esasdcosnan.to_csv(archid, header=None, index=None, sep=';', mode='w')
            # OK posiciones body (vacias)
            print('Sin datos')
        else:
            # Calcula apagar (neto) de cada renglon    
            df_body_esasdcosnan['zcostot'] = df_body_esasdcosnan.apply(calcular_zcostot, axis=1)      # OJO aqui zcostot falta gastos---------------------------------------------------
        
            # Calcula 2 bonif separadas
            df_body_esasdcosnan['boncosme'] = df_body_esasdcosnan.apply(calcular_boncosme, axis=1) 
            df_body_esasdcosnan['bonhogar'] = df_body_esasdcosnan.apply(calcular_bonhogar, axis=1) 
            df_body_esasdcosnan['bonotros'] = df_body_esasdcosnan.apply(calcular_bonotros, axis=1) 
            
            # Lo torna flotante para que sea igual formato que el divisor mas adelante
            df_body_esasdcosnan['zcostot'] = df_body_esasdcosnan['zcostot'].astype('float') 
            df_body_esasdcosnan['boncosme'] = df_body_esasdcosnan['boncosme'].astype('float') 
            df_body_esasdcosnan['bonhogar'] = df_body_esasdcosnan['bonhogar'].astype('float') 
            df_body_esasdcosnan['bonotros'] = df_body_esasdcosnan['bonotros'].astype('float') 
            
            # Hace un resumen sumando por cod_cliente
            df_grouped = df_body_esasdcosnan.groupby('cod_cliente')[['zcostot', 'boncosme', 'bonhogar', 'bonotros']].sum().reset_index()    
            df_grouped['migastoadmin'] = df_grouped['zcostot']
            
            # En resumen documenta G=grandes/C=chicas
            df_grouped['GRCH'] = df_grouped.apply(calcular_GRCH, axis=1)  
            
            # Reemplaza en migastoadmin el neto por los gastos obtenidos desde neto
            df_grouped = df_grouped.assign(migastoadmin=df_grouped['migastoadmin'] * porgtos)
            
            # Cambia el tipo de cod_cliente para que lo soporte la igualdad al cruzar con detalles
            df_grouped['cod_cliente'] = df_grouped['cod_cliente'].astype('int64') 
            
            # Dejo 2 decimales
            df_grouped['migastoadmin']=df_grouped['migastoadmin'].round(2)         
            df_grouped['zcostot']=df_grouped['zcostot'].round(2)         
            df_grouped['boncosme']=df_grouped['boncosme'].round(2)   
            df_grouped['bonhogar']=df_grouped['bonhogar'].round(2)         
            df_grouped['bonotros']=df_grouped['bonotros'].round(2)   
                    
            # Cambia el tipo de cod_cliente para que lo soporte la igualdad al cruzar con agrupado 
            df_body_esasdcosnan['cod_cliente'] = df_body_esasdcosnan['cod_cliente'].astype('int64') 
            
            # Corrige PRENP de los registros 'Gastos Administrativos' (se asume que el resto de los detalles esta bien)
            df_body_esasdcosnan["PRENP"] = df_body_esasdcosnan.apply(lambda x: df_grouped[df_grouped['cod_cliente'] ==
                    x["cod_cliente"]]['migastoadmin'].values[0] if x["DESCRI"] == 'Gastos Administrativos' 
                    and x["cod_cliente"] in df_grouped['cod_cliente'].values else x["PRENP"], axis=1)
                
            # Cruzo ambos duplicando _x y _y algunos campos
            resultado = df_body_esasdcosnan.merge(df_grouped, on=['cod_cliente'], how='left')
            
            # elimino la columna redundante y renombro otras
            resultado = resultado.drop(['zcostot_y'], axis=1)
            resultado = resultado.rename(columns={'GRCH_y': 'GRCH'})
            df_body_esasdcosnan = resultado.rename(columns={'zcostot_x': 'zcostot'})

            # calcula el 21% del migastoadmin para aquellos que cumplen las condiciones G/C respectivamente
            df_body_esasdcosnan["IVA"] = df_body_esasdcosnan.apply(lambda x: round(float(tasa21 * x["migastoadmin"]/sumatasas),2)
                        if x["GRCH"] == 'G' and 
                        x["DESCRI"] == 'Gastos Administrativos' and
                        x["cod_cliente"] in df_grouped['cod_cliente'].values else x["IVA"], axis=1)    
            df_body_esasdcosnan["IVA"] = df_body_esasdcosnan.apply(lambda x: round(float(tasa21 * x["migastoadmin"]/unatasa),2)
                        if x["GRCH"] == 'C' and 
                        x["DESCRI"] == 'Gastos Administrativos' and
                        x["cod_cliente"] in df_grouped['cod_cliente'].values else x["IVA"], axis=1)    
            
            # calcula el 10.5 del migastoadmin para aquellos que cumplen las condiciones G/C respectivamente
            df_body_esasdcosnan["ADIC"] = df_body_esasdcosnan.apply(lambda x: round(float((unatasa * x["migastoadmin"]/sumatasas) * iva2pura/100),2)
                        if x["GRCH"] == 'G' and 
                        x["DESCRI"] == 'Gastos Administrativos' and                   
                        x["cod_cliente"] in df_grouped['cod_cliente'].values else x["ADIC"], axis=1)    
            df_body_esasdcosnan["ADIC"] = df_body_esasdcosnan.apply(lambda x: round(float(0),2)
                        if x["GRCH"] == 'C' and 
                        x["DESCRI"] == 'Gastos Administrativos' and
                        x["cod_cliente"] in df_grouped['cod_cliente'].values else x["ADIC"], axis=1)    

            #------------------------------------------------------------------------------- Ahora IVA y ADIC de los no gastos
            # calcula el 21% del zcostot para aquellos que cumplen las condiciones G/C respectivamente
            df_body_esasdcosnan["IVA"] = df_body_esasdcosnan.apply(lambda x: round(float(tasa21 * x["zcostot"]/sumatasas),2)
                        if x["GRCH"] == 'G' and 
                        x["DESCRI"] != 'Gastos Administrativos' and
                        x["cod_cliente"] in df_grouped['cod_cliente'].values else x["IVA"], axis=1)    
            df_body_esasdcosnan["IVA"] = df_body_esasdcosnan.apply(lambda x: round(float(tasa21 * x["zcostot"]/unatasa),2)
                        if x["GRCH"] == 'C' and 
                        x["DESCRI"] != 'Gastos Administrativos' and
                        x["cod_cliente"] in df_grouped['cod_cliente'].values else x["IVA"], axis=1)    
            
            # calcula el 10.5 del zcostot para aquellos que cumplen las condiciones G/C respectivamente
            df_body_esasdcosnan["ADIC"] = df_body_esasdcosnan.apply(lambda x: round(float((unatasa * x["zcostot"]/sumatasas) * iva2pura/100),2)
                        if x["GRCH"] == 'G' and 
                        x["DESCRI"] != 'Gastos Administrativos' and                   
                        x["cod_cliente"] in df_grouped['cod_cliente'].values else x["ADIC"], axis=1)    
            df_body_esasdcosnan["ADIC"] = df_body_esasdcosnan.apply(lambda x: round(float(0),2)
                        if x["GRCH"] == 'C' and 
                        x["DESCRI"] != 'Gastos Administrativos' and
                        x["cod_cliente"] in df_grouped['cod_cliente'].values else x["ADIC"], axis=1)    
                    
            # Realizar la fusión de los dos DataFrames en base a 'cod_cliente'
            df_merged = pd.merge(df_grouped, df_body_esasdcosnan, on='cod_cliente', how='left')

            # Agregar las columnas con las sumas de 'IVA' y 'ADIC'
            df_merged['suma_IVA'] = df_merged.groupby('cod_cliente')['IVA'].transform('sum')
            df_merged['suma_ADIC'] = df_merged.groupby('cod_cliente')['ADIC'].transform('sum')

            df_merged['suma_boncos'] = df_merged.groupby('cod_cliente')['boncosme_x'].transform('sum')     
            df_merged['suma_bonhog'] = df_merged.groupby('cod_cliente')['bonhogar_x'].transform('sum')     
            df_merged['suma_bonres'] = df_merged.groupby('cod_cliente')['bonotros_x'].transform('sum')      
            
            # Eliminar las columnas duplicadas después de la fusión
            df_merged = df_merged.drop(['IVA', 'ADIC'], axis=1)
        
            # borrar columna zcostot y otras
            df_body_esasdcosnan=df_body_esasdcosnan.drop(['zcostot'], axis=1)
            df_body_esasdcosnan=df_body_esasdcosnan.drop(['GRCH'], axis=1)
            df_body_esasdcosnan=df_body_esasdcosnan.drop(['migastoadmin'], axis=1)
            df_body_esasdcosnan=df_body_esasdcosnan.drop(['boncosme_x'], axis=1)
            df_body_esasdcosnan=df_body_esasdcosnan.drop(['boncosme_y'], axis=1)
            df_body_esasdcosnan=df_body_esasdcosnan.drop(['bonhogar_x'], axis=1)
            df_body_esasdcosnan=df_body_esasdcosnan.drop(['bonhogar_y'], axis=1)
            df_body_esasdcosnan=df_body_esasdcosnan.drop(['bonotros_x'], axis=1)
            df_body_esasdcosnan=df_body_esasdcosnan.drop(['bonotros_y'], axis=1)
      
            #=============================================================================
            eliminar_decimal(df_body_esasdcosnan,'cod_cliente')
            completar_con_ceros(df_body_esasdcosnan,'cod_cliente')
            eliminar_decimal(df_body_esasdcosnan,'DV')
            eliminar_decimal(df_body_esasdcosnan,'ARTICULO')
            completar_con_ceros(df_body_esasdcosnan,'ARTICULO')
            eliminar_decimal(df_body_esasdcosnan,'DVPROD')
            eliminar_decimal(df_body_esasdcosnan,'TIPO')
            completar_con_2_ceros(df_body_esasdcosnan,'TIPO')      # recien arreglado
            eliminar_decimal(df_body_esasdcosnan,'AC')
            eliminar_decimal(df_body_esasdcosnan,'AC1')
            eliminar_decimal(df_body_esasdcosnan,'CANT')
            eliminar_decimal(df_body_esasdcosnan,'NOSE3')
            eliminar_decimal(df_body_esasdcosnan,'BONIF')
            #====================================================Detalles Body a CSV ===========================================================
            df_body_esasdcosnan.to_csv(archid, header=None, index=None, sep=';', mode='w')
            # OK posiciones body
        
        filtered_df_cabe_esas = df_cabetxt.where(df_cabetxt['cod_cliente'].isin(lista_sw))
        df_body_esas = filtered_df_cabe_esas.dropna(how='all')
        df_body_esas_copia = df_body_esas.copy()
        if df_body_esas_copia.empty:
            #====================================================Cabeceras Body a CSV ===========================================================
            df_body_esas_copia.to_csv(archi, header=None, index=None, sep=';', mode='w')
            # OK cabeceras body
            print('Cabeceras vacias para Body')
        else:
            df_body_esas_copia["apagar"]  = df_body_esas_copia.apply(lambda x: df_merged[df_merged['cod_cliente'] ==
                    x["cod_cliente"]]['zcostot_x'].values[0] 
                    if x["cod_cliente"] in df_merged['cod_cliente'].values else x["apagar"], axis=1)  
            
            df_body_esas_copia["boncos"]  = df_body_esas_copia.apply(lambda x: df_merged[df_merged['cod_cliente'] ==
                    x["cod_cliente"]]['suma_boncos'].values[0] 
                    if x["cod_cliente"] in df_merged['cod_cliente'].values else x["boncos"], axis=1)  
            
            df_body_esas_copia["bonhog"]  = df_body_esas_copia.apply(lambda x: df_merged[df_merged['cod_cliente'] ==
                    x["cod_cliente"]]['suma_bonhog'].values[0] 
                    if x["cod_cliente"] in df_merged['cod_cliente'].values else x["bonhog"], axis=1)  
            
            df_body_esas_copia["bonres"]  = df_body_esas_copia.apply(lambda x: df_merged[df_merged['cod_cliente'] ==
                    x["cod_cliente"]]['suma_bonres'].values[0] 
                    if x["cod_cliente"] in df_merged['cod_cliente'].values else x["bonres"], axis=1)  
            
            df_body_esas_copia["iva"]  = df_body_esas_copia.apply(lambda x: df_merged[df_merged['cod_cliente'] ==
                    x["cod_cliente"]]['suma_IVA'].values[0] 
                    if x["cod_cliente"] in df_merged['cod_cliente'].values else x["iva"], axis=1)  
            
            df_body_esas_copia["adic"]  = df_body_esas_copia.apply(lambda x: df_merged[df_merged['cod_cliente'] ==
                    x["cod_cliente"]]['suma_ADIC'].values[0] 
                    if x["cod_cliente"] in df_merged['cod_cliente'].values else x["adic"], axis=1)  
              
            eliminar_decimal(df_body_esas_copia,'cod_cliente')
            completar_con_ceros(df_body_esas_copia,'cod_cliente')
            completar_con_ceros(df_body_esas_copia,'I')
            eliminar_decimal(df_body_esas_copia,'C')
            eliminar_decimal(df_body_esas_copia,'D')
            eliminar_decimal(df_body_esas_copia,'E')
            completar_con_2_ceros(df_body_esas_copia,'E')           # formateado ok
            eliminar_decimal(df_body_esas_copia,'G')
            eliminar_decimal(df_body_esas_copia,'H')
            eliminar_decimal(df_body_esas_copia,'apagar')
            redondear_decimal(df_body_esas_copia,'iva')
            redondear_decimal(df_body_esas_copia,'adic')
            eliminar_decimal(df_body_esas_copia,'O')
            eliminar_decimal(df_body_esas_copia,'CPROV')
            eliminar_decimal(df_body_esas_copia,'Q')
            redondear_decimal(df_body_esas_copia,'boncos')
            redondear_decimal(df_body_esas_copia,'bonhog')
            redondear_decimal(df_body_esas_copia,'bonres')
            eliminar_decimal(df_body_esas_copia,'U')
            eliminar_decimal(df_body_esas_copia,'V')
            eliminar_decimal(df_body_esas_copia,'W')   # aqui cabeceras body
            
            # Filtrar df_body_esasdcosnan por DESCRI
            gastos_administrativos = df_body_esasdcosnan[df_body_esasdcosnan["DESCRI"] == "Gastos Administrativos"]

            # Actualizar la columna "apagar" usando loc y lambda    
            df_body_esas_copia.loc[df_body_esas_copia["cod_cliente"].isin(gastos_administrativos["cod_cliente"]),
                        "apagar"] = df_body_esas_copia.loc[df_body_esas_copia["cod_cliente"].isin(gastos_administrativos["cod_cliente"])].apply(
                            lambda x: f"{round(float(x['apagar']) + gastos_administrativos[gastos_administrativos['cod_cliente'] == x['cod_cliente']]['PRENP'].sum(), 2)}", axis=1)
            df_body_esas_copia = df_body_esas_copia.drop(['bonhog'], axis=1)
            #====================================================Cabeceras Body a CSV ===========================================================
            df_body_esas_copia.to_csv(archi, header=None, index=None, sep=';', mode='w')
            # OK cabeceras body
        
        #-----------------------------------------------------    REGRABAR Lady -------------------------------------------------------------          
        # ahora regrabar cli, cabe y deta sin esas minas para lady
        ##os.chdir('Y:\\INTPEDIDOS\\BODY\\')  
        #os.chdir('..\\Entradas\\')
        os.chdir('C:\\C#\\VENTASCLI\\')
        # 'cod_cliente','DV','TIPREV','ZONASEC','T12','NOMBRE','TDOC','NDOC','DIRE','NDIRE',
        #'KK1','KK2','KK3','ECALL','KK4','CP','CPROV','PROV','KK5','KK6','KK7','EXPLI', 'QSEYO'
        filtered_df_esasl = df_clietxt.where(~df_clietxt['cod_cliente'].isin(lista_sw))
        df_sin_nan_esasl = filtered_df_esasl.dropna(how='all')
        df_sin_nan_esasl_copia = df_sin_nan_esasl.copy()
        
        eliminar_decimal(df_sin_nan_esasl_copia,'cod_cliente')
        completar_con_ceros(df_sin_nan_esasl_copia,'cod_cliente')
        eliminar_decimal(df_sin_nan_esasl_copia,'DV')
        eliminar_decimal(df_sin_nan_esasl_copia,'T12')
        eliminar_decimal(df_sin_nan_esasl_copia,'TDOC')
        eliminar_decimal(df_sin_nan_esasl_copia,'NDOC')
        eliminar_decimal(df_sin_nan_esasl_copia,'NDIRE')
        eliminar_decimal(df_sin_nan_esasl_copia,'CP')
        eliminar_decimal(df_sin_nan_esasl_copia,'CPROV')
        eliminar_decimal(df_sin_nan_esasl_copia,'KK5')
        #====================================================Clientes Lady a CSV ===========================================================
        df_sin_nan_esasl_copia.to_csv("Cli_fact_"+qfecha+'.txt', header=None, index=None, sep=';', mode='w')       
        # OK clientes lady

        #'ZONASEC','cod_cliente','C','D','E','F','G','H','I','J','K','L','M','N','O','CPROV','Q','R','S','T','U','V','W']
        filtered_df_cabe_esasl = df_cabetxt.where(~df_cabetxt['cod_cliente'].isin(lista_sw))
        df_lady_esas = filtered_df_cabe_esasl.dropna(how='all')
        df_lady_esas_copia = df_lady_esas.copy()
        
        eliminar_decimal(df_lady_esas_copia,'cod_cliente')
        completar_con_ceros(df_lady_esas_copia,'cod_cliente')
        eliminar_decimal(df_lady_esas_copia,'C')
        eliminar_decimal(df_lady_esas_copia,'D')
        eliminar_decimal(df_lady_esas_copia,'E')
        completar_con_2_ceros(df_lady_esas_copia,'E')           # formateado
        eliminar_decimal(df_lady_esas_copia,'G')
        eliminar_decimal(df_lady_esas_copia,'H')
        eliminar_decimal(df_lady_esas_copia,'M')
        eliminar_decimal(df_lady_esas_copia,'N')
        eliminar_decimal(df_lady_esas_copia,'O')
        eliminar_decimal(df_lady_esas_copia,'CPROV')
        eliminar_decimal(df_lady_esas_copia,'Q')
        eliminar_decimal(df_lady_esas_copia,'T')
        eliminar_decimal(df_lady_esas_copia,'U')
        eliminar_decimal(df_lady_esas_copia,'V')
        eliminar_decimal(df_lady_esas_copia,'W')
        #====================================================Cabeceras Lady a CSV ===========================================================
        df_lady_esas_copia.to_csv(archi, header=None, index=None, sep=';', mode='w')
        # OK cabeceras lady

        # 'ZONASEC','cod_cliente','DV','ARTICULO','DVPROD','TIPO','AC','AC1','CANT','NOSE1','ADIC','PRENP',
        # 'IVA','DESCRI','NOSE2','NOSE3','NOSE4','BONIF','GRUPO']
        filtered_df_detas_esasl = df_detatxt.where(~df_detatxt['cod_cliente'].isin(lista_sw))
        df_lady_esasd = filtered_df_detas_esasl.dropna(how='all')
        df_lady_esasd_copia = df_lady_esasd.copy()
        
        eliminar_decimal(df_lady_esasd_copia,'cod_cliente')
        completar_con_ceros(df_lady_esasd_copia,'cod_cliente')
        eliminar_decimal(df_lady_esasd_copia,'DV')
        eliminar_decimal(df_lady_esasd_copia,'ARTICULO')
        completar_con_ceros(df_lady_esasd_copia,'ARTICULO')
        eliminar_decimal(df_lady_esasd_copia,'DVPROD')
        eliminar_decimal(df_lady_esasd_copia,'TIPO')
        completar_con_2_ceros(df_lady_esasd_copia,'TIPO')      # recien arreglado
        eliminar_decimal(df_lady_esasd_copia,'AC')
        eliminar_decimal(df_lady_esasd_copia,'AC1')
        eliminar_decimal(df_lady_esasd_copia,'CANT')
        eliminar_decimal(df_lady_esasd_copia,'NOSE3')
        eliminar_decimal(df_lady_esasd_copia,'BONIF')
        #====================================================Detalles Lady a CSV ===========================================================
        df_lady_esasd_copia.to_csv(archid, header=None, index=None, sep=';', mode='w')
        # OK posiciones lady
        #================================================================================== FIN ============================================