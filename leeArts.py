#----------------------------------------------------------------------------------#
# El txt de SAP debe estar en : Y:\Grupales\InterfacesSAP\VENTASCLI\BACKUP
# DEJARA UN TXT IGUAL A LA ENTRADA SIN CAMPO 'IMPORTADO' 
# Y OTRO CON SOLO EL CODIGO Y EL CAMPO IMPORTADO (SOLO DE LOS REGISTROS QUE LO SEAN)
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
elme=(f'{now.month:02}')
elan=str(now.year)
elamd=elan+elme+eldi
sale=[]

pidoc='09'      # campania del archivo de materiales a "afeitar"

class Aplicacion():
    def __init__(self):
        self.raiz = Tk()
        self.raiz.title("Evaluacion previa de datos")
        # Declara variables de control
        self.esean = IntVar(value=elan)        
        self.eseme = DoubleVar(value=elme)
        self.total = DoubleVar(value=0.0)
        # Carga imagen para asociar a widget Label()
        tren = PhotoImage(file='.\\IMAGEN\\deposito.png')
        self.imagen1 = ttk.Label(self.raiz, image=tren, 
                                 anchor="center")
        #
        self.etiq3 = ttk.Label(self.raiz, text="Año:")
        self.pidoa = ttk.Entry(self.raiz, textvariable=self.esean, width=10)      
        self.etiq4 = ttk.Label(self.raiz, text="Mes:")
        self.pidom = ttk.Entry(self.raiz, textvariable=self.eseme, width=10)    
        #
        self.separ1 = ttk.Separator(self.raiz, orient=HORIZONTAL)
        
        self.boton1 = ttk.Button(self.raiz, text="Procesar", 
                                 command=self.validar)
        self.boton2 = ttk.Button(self.raiz, text="Salir", 
                                 command=quit)                                 
        #
        self.imagen1.pack(side=TOP, fill=BOTH, expand=True, 
                          padx=10, pady=5)                                         
        self.etiq3.pack(side=TOP, fill=BOTH, expand=True, 
                        padx=10, pady=5)
        self.pidoa.pack(side=TOP, fill=X, expand=True, 
                       padx=20, pady=5)
        self.etiq4.pack(side=TOP, fill=BOTH, expand=True, 
                        padx=10, pady=5)
        self.pidom.pack(side=TOP, fill=X, expand=True, 
                        padx=20, pady=5)
        #
        self.separ1.pack(side=TOP, fill=BOTH, expand=True, 
                         padx=5, pady=5)
        self.boton1.pack(side=LEFT, fill=BOTH, expand=True, 
                         padx=10, pady=10)
        self.boton2.pack(side=RIGHT, fill=BOTH, expand=True, 
                         padx=10, pady=10)                
        self.raiz.mainloop()
        
    def validar(self):
        # Función para validar datos
        error_dato = False

        esean = int(self.esean.get())
        eseme = int(self.eseme.get())
        anionu=int(esean)
        mesnu=int(eseme)
        ayer=int(elan)-1
        if not (int(elan)-1 <= esean <= int(elan)):
            MessageBox.showerror("Dato erroneo!", "Año debe ser entre {} y {}".format(ayer,elan)) 
            error_dato = True      
        if not (eseme in range(1,13)):
            MessageBox.showerror("Dato erroneo!", "Mes debe ser entre {} y {}".format(1,12)) 
            error_dato = True      
        
        self.ejecutar(str(anionu),str(mesnu))

    def ejecutar(self, pidoa, pidom):
            pidom=pidom.zfill(2)
            os.chdir('.\\Subidas\\')
            trabajo=os.getcwd()
            arreglo=[[],[]]
            os.chdir('Y:\\InterfacesSAP\\VENTASCLI\\BACKUP\\')
            #-------------------------------------------
            for archi in glob.glob("ARTS_C"+pidoc+"_"+pidoa+pidom+"*"+".txt"):
            
                os.chdir('Y:\\InterfacesSAP\\VENTASCLI\\BACKUP\\')
                df_sumadispo=0
                qfecha6=archi[4:10]
                cadena=archi[10:12]
                cachodia=int(cadena)

                df_cabetxt=pd.read_csv(archi, delimiter = ";",  header=None)
                df_cabetxt.columns = ['acam','codigo','digver','descri','tipo','flia','subflia','grupo','subgru','zalgo','rubro','costo','moneda','nose1','nose2','qseyo','plata','nose3','mersap','importado']
                indexNames = df_cabetxt[ df_cabetxt['codigo'] > 0 ].index 

                df_Nuevo = df_cabetxt[['codigo', 'importado']].copy()
                df_Nuevo = df_Nuevo.drop(df_Nuevo[df_Nuevo['importado']!='I'].index)   
                df_Nuevo['codigo'] = df_Nuevo['codigo'].apply(lambda x: '{0:0>18}'.format(x))
                
                df_sinimpo = df_cabetxt[['acam','codigo','digver','descri','tipo','flia','subflia','grupo','subgru','zalgo','rubro','costo','moneda','nose1','nose2','qseyo','plata','nose3','mersap']].copy()
                df_sinimpo['codigo'] = df_sinimpo['codigo'].apply(lambda x: '{0:0>18}'.format(x))
                df_sinimpo['tipo'] = df_sinimpo['tipo'].apply(lambda x: '{0:0>2}'.format(x))
                df_sinimpo['flia'] = df_sinimpo['flia'].apply(lambda x: '{0:0>3}'.format(x))
                df_sinimpo['subflia'] = df_sinimpo['subflia'].apply(lambda x: '{0:0>3}'.format(x))
                df_sinimpo['grupo'] = df_sinimpo['grupo'].apply(lambda x: '{0:0>3}'.format(x))
                df_sinimpo['subgru'] = df_sinimpo['subgru'].apply(lambda x: '{0:0>4}'.format(x))
                df_sinimpo['rubro'] = df_sinimpo['rubro'].apply(lambda x: '{0:0>4}'.format(x))

            os.chdir(trabajo)    
            df_Nuevo.to_csv(r'soloimpor'+"_C"+pidoc+"_"+qfecha6+".txt", header=None, index=None, sep=';', mode='a')
            df_sinimpo.to_csv(r'sinimpor'+"_C"+pidoc+"_"+qfecha6+".txt", header=None, index=None, sep=';', mode='a')
            MessageBox.showinfo("Fin de Proceso", "Terminado Exitosamente {} - {}".format(pidoa,pidom)) 

def main():
    mi_app = Aplicacion()
    return 0

if __name__ == '__main__':
    main()
#--------------------------------------------------    
