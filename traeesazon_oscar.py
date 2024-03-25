#----------------------------------------------------------------------------------#
# Ejecutar evalua.py
#  (teniendo en Y:\InterfacesSAP\INTPEDIDOS\BACKUP las cabeceras y posiciones )
#  ( de Y:\InterfacesSAP\VENTASCLI\BACKUP los clientes txt)
#  (y en Y:\InterfacesSAP\INTPEDIDOS\PASADO\ENERO 2022, los csv de cabeceras)
#  Finalmente: deja todos los C, D y R (simil txt) en: carpeta de /subidas
#  con 1 archivo txt por dia con las zonas que se eligieron para cada dia
#--------------------------------------------
# Marcar en excel (totalestxtaaaammdd.xlsx) con X los elegidos (en funcion del monto buscado) 
# el excel debe tener fecha de hoy
#--------------------------------------------
# Ejecutar traeesazon.py
#----------------------------------------------------------------------------------#
import numpy as np
import pandas as pd
import glob, os
from datetime import datetime
from tkinter import messagebox as MessageBox
from tkinter import *
from tkinter import ttk
now = datetime.now()
eldi=(f'{now.day:02}')
#eldi='24'      # si proceso al otro dia informar fecha del excel hardcodeando o cambiar nombre a excel
elme=(f'{now.month:02}')
elan=str(now.year)
elamd=elan+elme+eldi
lahor=datetime.now().strftime('%Y-%m-%d %H%M%S')
lahor=lahor[11:20]

#qzoquie='995'   # 10/8  dias 2 
#qzoquie='994'   # 16/7 dias 3 y 4
qzoquie='993'   # 24/8 dias 5 y 6 
#qzoquie='992'   # 14/7 dia 8/7
#qzoquie='991'   # 18/7 dia 9 y 12
#qzoquie='990'   # 22/7 dia 13 y 14
#qzoquie='989'   # 26/7 dia 22 y 23
#qzoquie='987'
#qzoquie='986'
#qzoquie='984'
#qzoquie='980'
#qzoquie='981'

os.chdir('.\subidas\\')
df = pd.read_excel(io = "totales_txt"+str(elamd)+".xlsx", sheet_name="Hoja 1", usecols=["PSTD","zona","laX"]) 

lax = df['laX']
lax = df[lax == "X"]

columnas = lax.columns
columnas = columnas.tolist()
valores = lax.values
variosc = []
variosd = []
variosr = []

pidoa='2022'
eseme = elme   # 6 ojo hardcodear llegado el caso
mesnu=int(eseme)

trabajo=os.getcwd()
losme=["ENERO","FEBRERO","MARZO","ABRIL","MAYO","JUNIO","JULIO","AGOSTO","SEPTIEMBRE","OCTUBRE","NOVIEMBRE","DICIEMBRE"]
enletras=losme[mesnu-1]    
############enletras=losme[mesnu-2]


letraanio=enletras+' '+pidoa
cachocabe = []
cachodeta = []
cachoclie = []
sale=[]
os.chdir('Y:\\InterfacesSAP\\INTPEDIDOS\\BACKUP\\')
for i in lax.index: 
    zonaeleg=lax["zona"][i]
    os.chdir('Y:\\InterfacesSAP\\INTPEDIDOS\\BACKUP\\')
    cortado=lax["PSTD"][i][:12] +"*Cabecera.txt"
    mosca=0
    for archi in glob.glob(cortado):
        df_cabetxt=pd.read_csv(archi, delimiter = ";",  header=None)
        df_cabetxt.columns = ['A','cod_cliente','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W']
        indexNames = df_cabetxt[ df_cabetxt['cod_cliente'] > 0 ].index 
        # abre csv de la zona
        qfecha=archi[4:12]
        os.chdir('Y:\\InterfacesSAP\\INTPEDIDOS\\PASADO\\'+letraanio+'\\')
        cacho='C'+str(qfecha)+str(zonaeleg).rjust(5, '0')+'.csv'
        ###for filename in glob.glob('C'+str(qfecha)+str(zonaeleg).rjust(5, '0')+'.csv'):
        for filename in glob.glob(cacho):
            df_cabecsv = pd.read_csv(filename, index_col=None, header=0)
            df_cabecsv=df_cabecsv['cod_cliente'].apply(lambda x: int(x/10))
            df_jamon=(df_cabetxt.merge(df_cabecsv, on='cod_cliente', how='left', indicator=True)                       .query('_merge == "left_only"')
                        .drop('_merge',1)) 
            # elimina por cliente en txt los que si en csv                        
            df_jamon = df_jamon.drop(df_jamon[df_jamon['A'].str[0:3]!=str(zonaeleg).rjust(3, '0')].index)
            # elimina del txt los que no son de la zona en analisis
            indexJam = df_jamon[ df_jamon['cod_cliente'] != ''].index 
            ################df_jamon = df_jamon.drop(df_jamon[df_jamon['L']>0].index)
            # ahora quito las que tienen adicional en df_jamon
            df_jamon = df_jamon.drop(df_jamon[df_jamon['A'].str[0:3] == '999'].index) 
            # quita personales

            plata = df_jamon['J'].sum()
            #plata=df_jamon.iloc[0]['J']
            mosca=mosca+plata
            sale.append([archi,zonaeleg,mosca])

            #--------- trata clientes ------------------------------------
            os.chdir('Y:\\InterfacesSAP\\VENTASCLI\\BACKUP\\')
            miclie='Cli_fact_'+qfecha+'.txt'
            trozos = []
            for hallado in glob.glob(miclie):
                df_clie=pd.read_csv(hallado, delimiter = ";",  header=None)
                df_clie.columns = ['cod_cliente','DV','TIPREV','ZONASEC','T12','NOMBRE','TDOC','NDOC','DIRE','NDIRE',
                'KK1','KK2','KK3','ECALL',
                'KK4','CP','CPROV','PROV','KK5','KK6','KK7','EXPLI','CHOTA']
                indexclie = df_clie[ df_clie['cod_cliente'] > 0 ].index 
                trozos.append(df_clie)    
            clientas = pd.concat(trozos, axis=0, ignore_index=True)
            saleclie = clientas.merge(right=df_jamon[['cod_cliente']], on='cod_cliente')
            #----------- clientes coincidentes con extraccion
            # aqui quitar las que en clientes tienen "9 " en el nombre
            # cruzar saleclie con df_jamon eliminando por condicion 
            #saleclie = saleclie.drop(saleclie[saleclie['NOMBRE']>0].index)
            index997  = saleclie[saleclie['NOMBRE'].str[:2] == '9 ' ].index
            saleclie.drop(index997 , inplace=True)
            df_jamon = df_jamon.merge(right=saleclie[['cod_cliente']], on='cod_cliente')
            #---------------------------------------------------------
            saleclie['cod_cliente'] = saleclie['cod_cliente'].apply(lambda x: '{0:0>10}'.format(x))  
            saleclie['T12'] = saleclie['T12'].apply(lambda x: '{0:0>2}'.format(x))
            saleclie['KK5'] = saleclie['KK5'].apply(lambda x: '{0:0>2}'.format(x))  
            zonsec=qzoquie+'00A' 
            saleclie['ZONASEC']=saleclie['ZONASEC'].map(zonsec.format)
            cachoclie.append(saleclie)
            #---------
            os.chdir(trabajo)
            #----------- fin clientes a salida -----------------------------------
            #--------------------- obtiene detalles = jamon ----------------
            
            os.chdir('Y:\\InterfacesSAP\\INTPEDIDOS\\BACKUP\\')
            mideta='PSTD'+qfecha+'_*posiciones.txt'
            sodapes = []
            for alguno in glob.glob(mideta):
                        df_deta=pd.read_csv(alguno, delimiter = ";",  header=None)
                        df_deta.columns = ['A1','cod_cliente','C1','D1','E1','F1','G1','H1','I1','J1','K1','L1','M1','N1','O1','P1','Q1','R1','S1']
                        indexdeta = df_deta[ df_deta['cod_cliente'] > 0 ].index 
                        sodapes.append(df_deta)
            detalles = pd.concat(sodapes, axis=0, ignore_index=True)
            saledet = detalles.merge(right=df_jamon[['cod_cliente']], on='cod_cliente')
            #---------- fin detalles coincidentes con extraccion ---------------
            saledet['cod_cliente'] = saledet['cod_cliente'].apply(lambda x: '{0:0>10}'.format(x))  
            saledet['D1'] = saledet['D1'].apply(lambda x: '{0:0>18}'.format(x))
            saledet['F1'] = saledet['F1'].apply(lambda x: '{0:0>2}'.format(x))   
            saledet['O1'] = saledet['O1'].apply(lambda x: '{0:0>1}'.format(x))   
            saledet['A1']=saledet['A1'].map(zonsec.format)
            os.chdir(trabajo)
            cachodeta.append(saledet)
            #----------- fin detalles a salida ---------------------------

            #----------- trata cabeceras --------------------------
            os.chdir(trabajo)
            df_jamon['cod_cliente'] = df_jamon['cod_cliente'].apply(lambda x: '{0:0>10}'.format(x))
            df_jamon['O'] = df_jamon['O'].apply(lambda x: '{0:0>10}'.format(x))
            df_jamon['P'] = df_jamon['P'].apply(lambda x: '{0:0>2}'.format(x)) 
            df_jamon['Q'] = df_jamon['Q'].apply(lambda x: '{0:0>2}'.format(x)) 
            df_jamon['E'] = df_jamon['E'].apply(lambda x: '{0:0>2}'.format(x))
            df_jamon['A']=df_jamon['A'].map(zonsec.format)

            cachocabe.append(df_jamon)
            #----------- fin cabeceras a salida -------------------
            #print (zonaeleg,plata)

#--------------------------------
os.chdir(trabajo)  

dfx = pd.DataFrame(sale, columns=['PSTD','zona','Plata'])
#dfx['disponible'] = dfx['Txt'] - dfx['CSV'] 
(max_row, max_col) = dfx.shape  # siempre, para disponer de esos datos
last_row=['Totales : ']+list(dfx.count())[1:2]+list(dfx.sum())[2:3]
dfx2 = pd.DataFrame(data=[last_row], columns=dfx.columns)
dff = dfx.append(dfx2, ignore_index=True)
writer = pd.ExcelWriter(r"genero_"+elamd+".xlsx")
dff.to_excel(writer,'Hoja 1', index=False, freeze_panes=(1,1))
workbook  = writer.book
worksheet = writer.sheets['Hoja 1']
format1 = workbook.add_format({'num_format': '0.00'})
worksheet.set_column(2, 2, None, format1) 
worksheet.set_column(0, max_col, 30)    # PSTD
worksheet.set_column(1, max_col, 4)     # zona
worksheet.set_column(2, max_col, 17)    # suma X
dff.to_excel(writer,'Hoja 1', index=False, freeze_panes=(1,1))
writer.save()
#--------------------------------
#os.chdir(trabajo)
df_cachoclie = pd.concat(cachoclie, axis=0, ignore_index=True)
df_cachoclie.to_csv(r'Cli_fact_'+elamd+'.txt', header=None, index=None, sep=';', mode='a')

df_cachodeta = pd.concat(cachodeta, axis=0, ignore_index=True)
df_cachodeta.to_csv(r'PSTD'+elamd+'_'+lahor+'posiciones.txt', header=None, index=None, sep=';', mode='a')

df_cachocabe = pd.concat(cachocabe, axis=0, ignore_index=True)
df_cachocabe.to_csv(r'PSTD'+elamd+'_'+lahor+'Cabecera.txt', header=None, index=None, sep=';', mode='a')

#----------- clientes a salida -----------------------------------
