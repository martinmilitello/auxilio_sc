#----------------------------------------------------------------------------------#
# Los txt de SAP deben estar en : Y:\Grupales\InterfacesSAP\INTPEDIDOS\BACKUP
# Los csv deben estar en : Y:\Grupales\InterfacesSAP\INTPEDIDOS\PASADO\ENERO 2022
#
# Procedera a :
#     Recorrer PSTD cabecera del anio/mes solicitado
#           Acceder a todos los CSV que respondan a la fecha de cada TXT
#           Cruzar el TXT leido con todos esos CSV, obteniendo aquellos que solo esten en el TXT
#           Apoyandose en los elegidos, leera el PSTD de posiciones y obtendra los pertinentes detalles 
#           Apoyandose en los elegidos, leera el Cli_fact de esa fecha y obtendra los pertinentes clientes
#     Finalmente debera crear un XLSX con fecha del dia y resumenes
# 
#------------------------------- Proceso ------------------------------------------#
# Ejecutar evaluar.py
#  (teniendo en Y:\InterfacesSAP\INTPEDIDOS\BACKUP las cabeceras y posiciones )
#  ( de Y:\InterfacesSAP\VENTASCLI\BACKUP los clientes txt)
#  (y en Y:\InterfacesSAP\INTPEDIDOS\PASADO\DICIEMBRE 2021, los csv de cabeceras)
#  Finalmente: deja todos los C, D y R (simil txt) en: carpeta de /subidas
#  con 1 archivo txt por dia con las zonas que se eligieron para cada dia
#  
#--------------------------------------------
#  Marcar en excel con X los elegidos (en funcion del monto buscado) 
#  el excel debe tener fecha de hoy
#--------------------------------------------
# Ejecutar traeesazon.py
# que deja en subidasx los txt con las zonas elegidas
# Colocarlos en : Y:\InterfacesSAP\INTPEDIDOS\BACKUP y en Y:\InterfacesSAP\VENTASCLI\BACKUP 
# con fecha de hoy y hora _000001
#----------------------------------------------------------------------------------#
import numpy as np
import pandas as pd
import glob, os
import sys
from datetime import datetime
import openpyxl


now = datetime.now()
eldi=(f'{now.day:02}')
elme=(f'{now.month:02}')
elan=str(now.year)
elamd=elan+elme+eldi
sale=[]

#pidoa='2021'
#pidom='12'                                             # despues ver como pedir
#malfa='DICIEMBRE'
 

diamesanio = datetime.now()

now = diamesanio.date()
diahoy = now.day
meshoy = now.month
aniohoy = now.year



if len(sys.argv) == 3:
    pidoa = sys.argv[1] # Año de los Archivos CSV  2022
    pidom = sys.argv[2] # Mes de los archivos CSV  12
    
    esean = int(pidoa)
    eseme = int(pidom)
    anionu=int(esean)

    mesperiodo = 10 # para poder traer planilla de meses anteriores
    
    if mesperiodo != eseme:
         mesnu=int(eseme-1)
    else :
         mesnu=int(eseme)

    ayer=int(elan)-1
    
    losme=["ENERO","FEBRERO","MARZO","ABRIL","MAYO","JUNIO","JULIO","AGOSTO","SEPTIEMBRE","OCTUBRE","NOVIEMBRE","DICIEMBRE"]
    enletras=losme[mesnu-1]    
    letraanio=enletras+' '+pidoa
    #print('kk')
    pidom=pidom.zfill(2)
    
   # print (os.getcwd())
    # os.chdir('subidasx')
    os.chdir('subidasx\\')  #para ejecutar Fuera del WEB quitar el #
    trabajo=os.getcwd()
    #print (trabajo)
  
    os.chdir(r'\\ms10004.vfc.com.ar\\fileserver\\grupales\\InterfacesSAP\\INTPEDIDOS\\BACKUP\\')  # Debe estar iniciada la sesión con Violetta
    mitrabajo=os.getcwd()
    listado = os.walk(mitrabajo)
    # print(mitrabajo)
            #-------------------------------------------

    mitrabajo=os.getcwd()
    # print (mitrabajo)

    for archi in glob.glob("PSTD"+pidoa+pidom+"*"+"cabecera.txt"):
        os.chdir(r'\\ms10004.vfc.com.ar\\fileserver\\grupales\\InterfacesSAP\\INTPEDIDOS\\BACKUP\\')
        df_sumadispo=0
        qfecha6=archi[4:10]
        cadena=archi[10:12]
        cachodia=int(cadena)

        df_cabetxt=pd.read_csv(archi, delimiter = ";",  header=None)
        df_cabetxt.columns = ['A','cod_cliente','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W']
        indexNames = df_cabetxt[ df_cabetxt['cod_cliente'] > 0 ].index 
        df_Nuevo = df_cabetxt[['A', 'J']].copy()
        df_Nuevo['zona'] = df_Nuevo["A"].str[0:3] 
        df_Nuevo.drop(['A'], axis=1, inplace=True)
        df_pivotcabe = pd.pivot_table(df_Nuevo, index= "zona", aggfunc= {"J": "sum"}, margins= True)
                                        #columns= "zona", 

                                       
                                       
        df_pivotcabe["esazona"] = df_pivotcabe.index     
        df_pivotcabe["montocsv"] = 0
                # aqui hacer array con zonas
                # iterar en puzo y leer cada csv

        dfNuevo = df_cabetxt[['A', 'J']].copy()
        dfNuevo.round({"J":2})
        dfNuevo['zona'] = dfNuevo["A"].str[0:3] 
        miarray = dfNuevo.groupby('zona').agg(totzona = ('J', 'sum'), zonas = ('zona','max'))
        otroarray=miarray[['totzona','zonas']].copy()
        sumacsvorig=0
        for i in otroarray.index:
            puzo=otroarray["zonas"][i]
            os.chdir(r'\\ms10004.vfc.com.ar\\fileserver\\grupales\\InterfacesSAP\\INTPEDIDOS\\PASADO\\'+letraanio+'\\')
                        # dentro del anio/mes busco ESA zona (podria venir el dia 3 y en dia 24)

            for archi1 in glob.glob('C'+str(qfecha6)+'*'+str(puzo).rjust(3, '0')+'.csv'):
                if archi1 and len(archi1)>0:
                    varios = []
                    lista=[]
                    sumacsvorig=0
                    estedia=int(archi1[7:9])
                    if estedia in range (cachodia-3,cachodia+3):
                        df_cabetxt1 = pd.read_csv(archi1, index_col=None, header=0)
                        indexNames1 = df_cabetxt1[ df_cabetxt1['zona'] > 0 ].index 
                        df_Nuevo1 = df_cabetxt1[['importe','zona']].copy()
                        df_pivotcabe1 = pd.pivot_table(df_Nuevo1,index= "zona",aggfunc= {"importe": "sum"},margins= True) 
                        df_iva2 =  df_cabetxt1['bonifivadic'].sum()                                              
                        df_pivotcabe1["zonacsv"] = df_pivotcabe1.index                           
                        hard=str(df_pivotcabe1.iloc[0]['zonacsv']).rjust(3, '0')
                        plata=df_pivotcabe1.iloc[0]['importe']
                        df_pivotcabe1 = pd.pivot_table(df_Nuevo1, 
                                                                        index= "zona", 
                                                                        aggfunc= {"importe": "sum"}, 
                                                                        margins= True)

                        sumacsvorig=plata

                                                #------------por cada zona del txt --------------------------------
                        putot=otroarray["totzona"][i]
                        lax= ' '
                        lasuma=' '
                        fecharchi=int(archi[4:12])
                        porce= sumacsvorig/putot*100
                        sale.append([archi,puzo,putot,sumacsvorig,df_iva2,lax,lasuma, fecharchi,porce])

    os.chdir(trabajo)  

    dfx = pd.DataFrame(sale, columns=['PSTD','zona','Txt','CSV','IVA2','laX','lasuma','fecha','porce'])
    # dfx['IVA2'] = dfx['Txt'] - dfx['CSV'] 

    df_mask=dfx['porce']<=200
    
    dfx= dfx[df_mask]# filtro para que no df los porcentajes negativos
    dfx.to_csv(r'prueba_negativos'+elamd+'.txt', index=None, sep=';', mode='a')
    (max_row, max_col) = dfx.shape  # siempre, para disponer de esos datos

    last_row=['Totales : ']+list(dfx.count())[1:2]+list(dfx.sum())[2:5]+[' ']+list(dfx.sum())[5:6]+[' ']+[' ']
    dfx2 = pd.DataFrame(data=[last_row], columns=dfx.columns)
    dff = pd.concat([dfx, dfx2], ignore_index=True)
            
    writer = pd.ExcelWriter(r"totales_txt_Prueba"+elamd+".xlsx")

    dff.to_excel(writer,'Hoja 1', index=False, freeze_panes=(1,1))
    workbook  = writer.book
    worksheet = writer.sheets['Hoja 1']

    for row in range(2,dff.shape[0]+2):
        #formula = f'=C{row}-D{row}'
        formula = f'=IF(F{row}="X",E{row},0)'
                # OJO poner IF (ingles) y coma (std ingles) (a pesar de que mi excel es SI y ;)
        worksheet.write_formula(f"G{row}", formula)

    format1 = workbook.add_format({'num_format': '0.00'})
    format2 = workbook.add_format({'num_format': '0.000'})
    worksheet.set_column(2, 4, None, format1) 
    worksheet.set_column(6, 6, None, format1) 
    worksheet.set_column(8, 8, None, format2) 
            #(max_row, max_col) = dff.shape
    worksheet.set_column(0, max_col, 30)    # PSTD
    worksheet.set_column(1, max_col, 4)     # zona
    worksheet.set_column(2, max_col, 17)    # sap
    worksheet.set_column(3, max_col, 17)    # tango
    worksheet.set_column(4, max_col, 17)    # resta
    worksheet.set_column(5, max_col, 3)     # X
    worksheet.set_column(6, max_col, 17)    # suma X
    worksheet.set_column(7, max_col, 8)     # fechas
    worksheet.set_column(8, max_col, 10)    # porcentual

    cell_formatv = workbook.add_format({'bold': True, 'font_color': 'green'})
    cell_formatr = workbook.add_format({'bold': True, 'font_color': 'red'})
    worksheet.conditional_format('E1:E'+str(max_row), {'type':     'cell',
                                        'criteria': 'greater than',
                                        'value':    '0',
                                        'format':   cell_formatv})

    worksheet.conditional_format('E1:E'+str(max_row), {'type':     'cell',
                                        'criteria': 'less than',
                                        'value':    '0',
                                        'format':   cell_formatr})

    header_format = workbook.add_format({
                'bold': True,
                'text_wrap': True,
                'valign': 'top',
                'fg_color': '#D7E4BC',
                'border': 1})
    for col_num, value in enumerate(dff.columns.values):
                worksheet.write(0, col_num , value, header_format)  # col_num + 1 corre los titulos

            #worksheet.conditional_format(max_col-2, max_col-1, max_row, max_col-1,
    worksheet.conditional_format(1, 7, max_row, 7,
                             {'type': '3_color_scale'})

            # Green fill with dark green text.
    formatvv = workbook.add_format({'bg_color':   '#C6EFCE',
                                        'font_color': '#006100'})
            # Light yellow fill with dark yellow text.
    formataa = workbook.add_format({'bg_color':   '#FFEB9C',
                               'font_color': '#9C6500'})

            #worksheet.conditional_format('B1:B'+str(max_row), {'type':     'cell',
    worksheet.conditional_format('B1:B'+str(max_row), {'type':      '3_color_scale',
                                        'min_color': '#C5D9F1',
                                        'max_color': '#538ED5'})

            #                           'criteria': 'color_cells',
            #                           'value':   '$H$1:$H$'+str(max_row),
            #                           'format':   formatvv})


    worksheet.conditional_format('I1:I'+str(max_row), {'type':     'cell',
                                       'criteria': 'between',
                                       'minimum':  99,
                                       'maximum':  101,
                                       'format':   formatvv})

    worksheet.conditional_format('I1:I'+str(max_row), {'type':     'cell',
                                       'criteria': 'between',
                                       'minimum':  65,
                                       'maximum':  98.99,
                                       'format':   cell_formatv})
            
    worksheet.conditional_format('I1:I'+str(max_row), {'type':     'cell',
                                    'criteria': '>',
                                    'value':   101,
                                    'format':   cell_formatr})

    worksheet.conditional_format('I1:I'+str(max_row), {'type':     'cell',
                                    'criteria': '<',
                                    'value':   65,
                                    'format':   formataa})

    worksheet.write(max_row+1, max_col-3, '=SUM(G2:G'+str(max_row)+')') 

#percent_format = workbook.add_format({'num_format': '0%'})
# Apply the number format to Grade column.
#worksheet.set_column(2, 2, None, percent_format)

    workbook.close()
else :
    print ("Faltan argumentos")

    # print(cabe_df)






