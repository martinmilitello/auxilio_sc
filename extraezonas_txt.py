import numpy as np
import pandas as pd
import glob, os
from datetime import datetime


os.chdir('salidas\\')
for archivo in os.listdir():  
            # Eliminar los archivos
    os.remove(archivo)


os.chdir('..\\subidasz\\')
trabajo=os.getcwd()

df_totalCabe = pd.DataFrame()
df_totalCabe['TotalImporte'] = None
df_totalCabe['TotalIVA1'] = None
df_totalCabe['TotalIVA2'] = None
df_totalCabe['Zona'] = None

df_totalCabe = df_totalCabe.assign(TotalImporte=145.23)
df_totalCabe = df_totalCabe.assign(TotalIVA1=345.56)
df_totalCabe = df_totalCabe.assign(TotalIVA2=987.15)
df_totalCabe = df_totalCabe.assign(Zona='023')

gastoadmi=2.9
topeIva2 = 95000


#-------------------------------------------
for archi in glob.glob("PSTD"+"*"+"cabecera.txt"):
    df_cabetxt=pd.read_csv(archi, delimiter = ";",  header=None)
    df_cabetxt.columns = ['A','cod_cliente','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W']
    indexNames = df_cabetxt[ df_cabetxt['cod_cliente'] > 0 ].index 
    qfecha=archi[4:12]
    
    #--------------- hasta  aqui PSTD cabecera txt 
    separado = df_cabetxt["A"].str[0:3] 
    dfzonas=df_cabetxt.assign(grupzonas=separado)
    dfzonas = dfzonas.groupby("grupzonas")
    dfzonas = dfzonas.agg({"cod_cliente": "nunique"})
    #--------------- hasta archivo de zonas agrupadas

    
    for estazona in dfzonas.index:
        os.chdir('salidas\\')
        

        trabajo=os.getcwd()
        #--------------------- extrae cabeceras ok
        df_mascara=df_cabetxt["A"].str[0:3] ==estazona
        filtered_df = df_cabetxt[df_mascara]
        filtered_df['cod_cliente'] = filtered_df['cod_cliente'].apply(lambda x: '{0:0>10}'.format(x))
        filtered_df['O'] = filtered_df['O'].apply(lambda x: '{0:0>10}'.format(x))
        filtered_df['P'] = filtered_df['P'].apply(lambda x: '{0:0>2}'.format(x)) 
        filtered_df['Q'] = filtered_df['Q'].apply(lambda x: '{0:0>2}'.format(x)) 
        filtered_df['E'] = filtered_df['E'].apply(lambda x: '{0:0>2}'.format(x))

        vTotalImporte=filtered_df['J'].sum()
        vTotalIVA1=filtered_df['K'].sum()
       # vTotalIVA2=filtered_df['L'].sum()

        vTotalIVA2 = filtered_df.loc[filtered_df['J'] > topeIva2, 'L'].sum()

        filtered_df.to_csv(r'Cabe'+str(qfecha)+str(estazona)+'SAP.txt', header=None, index=None, sep=';', mode='a')

        nueva_fila = { 'TotalImporte': vTotalImporte,'TotalIVA1': vTotalIVA1, 'TotalIVA2': vTotalIVA2, 'Zona':str(estazona)}
        # df_totalCabe = df_totalCabe.append(nueva_fila, ignore_index=True)
        df_totalCabe = pd.concat([df_totalCabe, pd.DataFrame([nueva_fila])], ignore_index=True)
        print(df_cabetxt)
        #--------------------- clientes ok
        trabajo=os.getcwd()
        os.chdir('..\\..\\subidasz\\')
        trabajo=os.getcwd()
        for archi in glob.glob("Cli_fact"+"*.txt"):
            df_clietxt=pd.read_csv(archi, delimiter = ";",  header=None, index_col=None)
            print(df_clietxt)
            df_clietxt.columns = ['cod_cliente','DV','TIPREV','ZONASEC','T12','NOMBRE','TDOC','NDOC','DIRE','NDIRE','KK1','KK2','KK3','ECALL','KK4','CP','CPROV','PROV','KK5','KK6','KK7','EXPLI','23']
            indexNames = df_clietxt[ df_clietxt['cod_cliente'] > 0 ].index 
            #
            os.chdir('salidas\\')
            trabajo=os.getcwd()
            #
            df_mascara=df_clietxt["ZONASEC"].str[0:3] ==estazona
            filtered_df = df_clietxt[df_mascara]
            filtered_df['cod_cliente'] = filtered_df['cod_cliente'].apply(lambda x: '{0:0>10}'.format(x))
            filtered_df['T12'] = filtered_df['T12'].apply(lambda x: '{0:0>2}'.format(x))
            filtered_df['KK5'] = filtered_df['KK5'].apply(lambda x: '{0:0>2}'.format(x))  
            filtered_df['CPROV'] = filtered_df['CPROV'].astype(str)
            filtered_df['CPROV'] = filtered_df['CPROV'].apply(lambda x: '{0:0>2}'.format(x)) 

            filtered_df.to_csv(r'Clie'+str(qfecha)+str(estazona)+'SAP.txt', header=None, index=None, sep=';', mode='a')

        #--------------------- detalles
        os.chdir('..\\..\\subidasz\\')
        trabajo=os.getcwd()
        for archi in glob.glob("PSTD"+"*"+"posiciones.txt"):
            df_detatxt=pd.read_csv(archi, delimiter = ";",  header=None)
            df_detatxt.columns =   ['A1','cod_cliente','C1','D1','E1','F1','G1','H1','I1','J1','K1','L1','M1','N1','O1','P1','Q1','R1','S1']
            indexNames = df_detatxt[ df_detatxt['cod_cliente'] > 0 ].index 
            #
            os.chdir('salidas\\')
            trabajo=os.getcwd()
            #
            df_mascara=df_detatxt["A1"].str[0:3] ==estazona
            filtered_df = df_detatxt[df_mascara]
            filtered_df['cod_cliente'] = filtered_df['cod_cliente'].apply(lambda x: '{0:0>10}'.format(x))
            filtered_df['D1'] = filtered_df['D1'].apply(lambda x: '{0:0>18}'.format(x))
            filtered_df['F1'] = filtered_df['F1'].apply(lambda x: '{0:0>2}'.format(x))   
            filtered_df['O1'] = filtered_df['O1'].apply(lambda x: '{0:0>1}'.format(x))   

            filtered_df.to_csv(r'Deta'+str(qfecha)+str(estazona)+'SAP.txt', header=None, index=None, sep=';', mode='a')
            os.chdir('..\\..\\subidasz\\')


trabajo=os.getcwd()
 
'''
writer = pd.ExcelWriter(r"totales_txt_TopeIVA2"+str(qfecha)+".xlsx")
df_totalCabe.to_excel(writer,'Hoja 1', index=False)
writer.save()
writer.close()
'''

writer = pd.ExcelWriter(r"totales_txt_TopeIVA2"+str(qfecha)+".xlsx", mode='w')
df_totalCabe.to_excel(writer,'Hoja 1', index=False)

# Cierra el escritor para guardar el archivo Excel
writer.close()  # Ya no es necesario usar writer.save()

# print(df_totalCabe)
