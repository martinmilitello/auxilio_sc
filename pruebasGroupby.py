import pandas as pd

df_ventas = pd.read_excel("D:\\Excel\\sales_9_2022.xlsx")

suma = df_ventas["Sales"].sum()

print (suma)

df_ventasGroupBy=df_ventas.groupby(['Region']).agg({'Sales': 'sum'})

print(df_ventasGroupBy)

df_VentasDoublecheck = df_ventas.groupby(['Region']).agg({'Sales': 'sum'}).sum()

print(df_VentasDoublecheck)

df_VentasBySegment= df_ventas.groupby(['Region', 'Segment']).agg({'Sales': 'sum'}).sum()

print(df_VentasBySegment)
# candidates_by_month = candidates_df.groupby('month').agg(num_cand_month = ('num_candidates', 'sum'))
