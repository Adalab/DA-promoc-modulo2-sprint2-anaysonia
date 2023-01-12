import files.support as sp
import pandas as pd

#llamamos a la clase:
nube=sp.Clima('hola')

dict_usa={'USA':[39.7837304,-100.445882]}
df_usa_clima=nube.obtener_prediccion(dict_usa,'meteo')
print(df_usa_clima.head(3))
print(df_usa_clima.columns)

df_ataques=pd.read_pickle('files/df_ataques_paises.pkl')
lista_paises=['usa']
df_ataques_usa=nube.obtener_ataques(df_ataques,lista_paises)

df_usa_clima_rh=nube.separar_columna_rh(df_usa_clima)

df_usa_clima_rh_wind=nube.separar_columna_wind(df_usa_clima_rh) 

df_unido=nube.juntar_dataframes(df_usa_clima_rh_wind,df_ataques_usa)

print(df_unido.head(3))

print(nube.guardar_dataframe('.pkl',df_unido,'files/prueba_main1.pkl'))


