#----
'''
Rescata una revendedora de los archivos de Interfaces de SAP TXT , traer los 
Archivos Cliente, Cabecera y Detalle de las carpetas en linea y copiarlos en
la carpeta SUBIDASR DEL SITIO
El programa pedirá el numero de revendedora 

'''

#----
import numpy as np
import pandas as pd
import glob, os
from datetime import datetime

import sys
now = datetime.now()
eldi=(f'{now.day:02}')
#eldi='24'      # si proceso al otro dia informar fecha del excel hardcodeando o cambiar nombre a excel
elme=(f'{now.month:02}')
elan=str(now.year)
elamd=elan+elme+eldi
lahor=datetime.now().strftime('%Y-%m-%d %H%M%S')
lahor=lahor[11:20]

if len(sys.argv) == 2:
    # pidoa = sys.argv[1] # Pido año
    # eseme = sys.argv[2] # Pido Mes
    # esedia = sys.argv[3] # Pido día
    revend = sys.argv[1] # Pido revendedora 2055017
    
    os.chdir('Subidasr\\')

    pidoa='2022'
    eseme = 6
    mesnu=int(eseme)

    trabajo=os.getcwd()
    losme=["ENERO","FEBRERO","MARZO","ABRIL","MAYO","JUNIO","JULIO","AGOSTO","SEPTIEMBRE","OCTUBRE","NOVIEMBRE","DICIEMBRE"]
    enletras=losme[mesnu-1]    

    letraanio=enletras+' '+pidoa
    cachocabe = []
    cachodeta = []
    cachoclie = []
    
    trabajo1=os.getcwd()
   
   
    cabecera="PSTD"+"*cabecera.txt"
    for archi in glob.glob(cabecera):
        df_cabetxt=pd.read_csv(archi, delimiter = ";",  dtype=str, header=None)
        df_cabetxt.columns = ['A','cod_cliente','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W']
        qfecha=archi[4:12]
            # abre csv de la zona
        df_mask_cabe=df_cabetxt['cod_cliente']==revend
        df_revend_cabe = df_cabetxt[df_mask_cabe]

        print(df_revend_cabe)
                        
                #--------- trata clientes ------------------------------------
       
    miclie='Cli_fact_*'+'.txt'
    trozos = []
    for hallado in glob.glob(miclie):
        df_clie=pd.read_csv(hallado, delimiter = ";",  dtype=str, header=None)
        df_clie.columns = ['cod_cliente','DV','TIPREV','ZONASEC','T12','NOMBRE','TDOC','NDOC','DIRE','NDIRE',
                    'KK1','KK2','KK3','ECALL',
                    'KK4','CP','CPROV','PROV','KK5','KK6','KK7','EXPLI']
       
        df_mask_clie=df_clie['cod_cliente']==revend
        df_revend_clie = df_clie[df_mask_clie]
                #---------
        print(df_revend_clie)
                #----------- fin clientes a salida -----------------------------------
                #--------------------- obtiene detalles = jamon ----------------
                
        
    mideta="PSTD"+"*posiciones.txt"
    
    for alguno in glob.glob(mideta):
        df_deta=pd.read_csv(alguno, delimiter = ";", dtype=str, header=None)
        df_deta.columns = ['A1','cod_cliente','C1','D1','E1','F1','G1','H1','I1','J1','K1','L1','M1','N1','O1','P1','Q1','R1','S1']
      
        df_mask_deta=df_deta['cod_cliente']==revend
        df_revend_deta = df_deta[df_mask_deta]

        print(df_revend_deta)


    
    
                #---------- fin detalles coincidentes con extraccion ---------------
   
    
    
    df_revend_clie.to_csv(r'RevCli_fact_'+elamd+'.txt', header=None, index=None, sep=';', mode='a')

    df_revend_deta.to_csv(r'RevPSTD'+elamd+'_'+lahor+'Posiciones.txt', header=None, index=None, sep=';', mode='a')
  
    df_revend_cabe.to_csv(r'RevPSTD'+elamd+'_'+lahor+'Cabecera.txt', header=None, index=None, sep=';', mode='a')

else :
    print ("Faltan argumentos")

#----------- clientes a salida -----------------------------------
