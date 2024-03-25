import numpy as np
import pandas as pd
import glob, os
from datetime import datetime

pidoa = "2022" # Año de los Archivos CSV
pidom = "11" # Mes de los archivos CSV
diresalida = '\\salidas'
now = datetime.now()

trabajo=os.getcwd()

now = datetime.now()
eldi=(f'{now.day:02}')
elme=(f'{now.month:02}')
elan=str(now.year)
elamd=elan+elme+eldi
 
losme=["ENERO","FEBRERO","MARZO","ABRIL","MAYO","JUNIO","JULIO","AGOSTO","SEPTIEMBRE","OCTUBRE","NOVIEMBRE","DICIEMBRE"]
enletras=losme[int(pidom)-1]    
letraanio=enletras+' '+pidoa


os.chdir(r'\\ms10004.vfc.com.ar\\fileserver\\grupales\\InterfacesSAP\\INTPEDIDOS\\PASADO\\'+letraanio+'\\')


sale=[]

for archi in glob.glob("*.csv"):

   for pos,char in enumerate(archi):

      if(ord(char) >= 48 and ord(char) <= 57 and pos == 2 and archi[0]== 'C'):

         #df = pd.read_csv('subidas\\C2021090400703.csv',delimiter = ",")
         
         os.chdir(r'\\ms10004.vfc.com.ar\\fileserver\\grupales\\InterfacesSAP\\INTPEDIDOS\\BACKUP\\')
         fechacsv = archi[1:9]
         cabesap = 'PSTD'+fechacsv+'_030515posiciones'
         detasap = 'PSTD'+fechacsv+'*Cabecera'
         df_cabetxt=pd.read_csv(archi, delimiter = ";",  header=None)

         df = pd.read_csv(archi,delimiter = ",")

         mizo = df['zona'].max()

         Total = df['importe'].sum()

         Adic = df['bonifivadic'].sum()

         fecha=df['fecha_emision'].max()

         sale.append([mizo,Total,Adic,fecha])




os.chdir(trabajo+diresalida)
dfx = pd.DataFrame(sale, columns=['zona', 'Total','Adic','fecha'])

dfx.to_excel("totales_csv2"+elamd+".xlsx", index=False)