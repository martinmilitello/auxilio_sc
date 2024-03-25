import os
from pandasql import sqldf
import pandas as pd



rutaPSTD='Y:\\InterfacesSAP\\INTPEDIDOS\\BACKUP\\'
rutaCLIE='Y:\\InterfacesSAP\\VENTASCLI\\BACKUP\\'


archiCabe = rutaPSTD + 'PSTD20230524_030502Cabecera.txt'
archiDeta = rutaPSTD + 'PSTD20230524_030502posiciones.txt'
archiClie = rutaCLIE + 'Cli_fact_20230524_ORIG.txt'

encabezadoCabe =['zonasec','revend','codramo','anio','camp','premeife','cancajas','fecfac','remito','impotot','ivatot1','ivatot2','impsobra','spbonval','nrocbte','prov','caiva','impbon1','impbon5','extracosm','impbon3','gtoadmin','exentos']
encabezadoDeta =['zonasec','revend','digverif','producto','digverpo','tipo','filler','aniocamp','cant','abastesp','iva2','prenp','iva1','descri','tipimpos','montib','a3','bonif','tipprod']
encabezadoClie =['revend','	digverif','	grupcta','zonasec','inhabili','rasoc','tidoc','ndocu','domic','altura','piso','dpto','local','ecall','partido','codpost','prov','provincia','caiva','nucuit','nucuil','barrio','retrapro']


df_cabetxt=pd.read_csv(archiCabe, delimiter = ";",  header=None)
df_cabetxt.columns = encabezadoCabe
df_cabetxt.fillna(0,inplace=True)

df_detatxt=pd.read_csv(archiDeta, delimiter = ";",  header=None)
df_detatxt.columns = encabezadoDeta
df_detatxt.fillna(0,inplace=True)

df_clietxt=pd.read_csv(archiClie, delimiter = ";",  header=None)
df_clietxt.columns = encabezadoClie
df_clietxt.fillna(0,inplace=True)


queryGrandes = """ SELECT SUBSTRING(zonasec,1,3) AS zona, revend,codramo,anio,camp,premeife,cancajas,fecfac,remito,impotot,ivatot1,ivatot2,impsobra,spbonval,nrocbte,prov,caiva,impbon1,impbon5,extracosm,impbon3,gtoadmin,exentos
            FROM df_cabetxt 
            WHERE impotot >= 23000
            """
queryChicas = """ SELECT SUBSTRING(zonasec,1,3) AS zona, revend,codramo,anio,camp,premeife,cancajas,fecfac,remito,impotot,ivatot1,ivatot2,impsobra,spbonval,nrocbte,prov,caiva,impbon1,impbon5,extracosm,impbon3,gtoadmin,exentos
            FROM df_cabetxt 
            WHERE impotot <= 23000
            """

df_CabeSQLgrandes = sqldf(queryGrandes)
df_CabeSQLchicas = sqldf(queryChicas)

print("---"*10)
print(df_CabeSQLgrandes)
print("---"*10)
print(df_CabeSQLchicas)









'''
students= {
    'Students':["Sira","Ibrahim","Moussa","Mamadou","Nabintou"],
    'Gender':['Female','Male','Male', "Male", "Female"],
    'Age':[18, 27, 19, 22, 21],
    'Email': ["sira@info.com", "ib@info.com", "mouss@info.com", 
             "mam@info.com", "nab@info.com"]
          }
students_df = pd.DataFrame(students)





# Create the Teaching Assistant Data Frame

teaching_assistant= {
    'Teacher':["Ibrahim","Nabintou","Mamadou","Fatim","Aziz"],
    'Email':['ib@info.com','nab@info.com','mam@info.com', 
             "fat@info.com", "aziz@info.com"],
    'Degree':["M.S in Data Science", "B.S in Statistics", 
              "B. Comp Sc", "M.S. Architecture", "B.S in Accounting"],
    'Department': ["Business", "Statistics", "Comp Sc", 
             "Engineering", "Business"]
          }
teaching_assistant_df = pd.DataFrame(teaching_assistant)

all_students = sqldf("SELECT * FROM students_df")


print(type(all_students))
print("---"*10)
print(all_students.dtypes)
query = """ SELECT SUBSTRING(Teacher,1,3) AS Teacher_Corto, Email, Degree 
            FROM teaching_assistant_df 
            WHERE Degree LIKE 'M.S%'
            """
ms_students = sqldf(query)
print(ms_students)

'''