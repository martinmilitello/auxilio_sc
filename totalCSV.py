#-----------------------------------------------------------------------------------------

# Busca en el directorio indicado solo csv,

# suma 2 columnas y almacena zona y 2 totales en una lista, la agrega a otra lista general

# y al terminar convierte en dataframe y transfiere a un excel

#-----------------------------------------------------------------------------------------

 
# Necesito una funcion que sume dos numeros
import numpy as np

import pandas as pd

import glob, os

from datetime import datetime

 

now = datetime.now()

eldi=(f'{now.day:02}')

elme=(f'{now.month:02}')

elan=str(now.year)

elamd=elan+elme+eldi

 

sale=[]

# os.chdir('Y:\\InterfacesSAP\\INTPEDIDOS\\PASADO\\MARZO 2024\\')

os.chdir('subidasr\\')

for archi in glob.glob("*.csv"):

   for pos,char in enumerate(archi):

      if(ord(char) >= 48 and ord(char) <= 57 and pos == 2 and archi[0]== 'C'):

         #df = pd.read_csv('subidas\\C2021090400703.csv',delimiter = ",")

         df = pd.read_csv(archi,delimiter = ",")

         mizo = df['zona'].max()

         Total = df['importe'].sum()

         Adic = df['bonifivadic'].sum()

         fecha=df['fecha_emision'].max()

         sale.append([mizo,Total,Adic,fecha])

 

dfx = pd.DataFrame(sale, columns=['zona', 'Total','Adic','fecha'])

dfx.to_excel("totales_csv2"+elamd+".xlsx", index=False)