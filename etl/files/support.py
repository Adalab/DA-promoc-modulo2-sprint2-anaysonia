import pandas as pd
import numpy as np
import requests

from IPython.core.interactiveshell import InteractiveShell # Nos permite mostar más de una salida por celda
InteractiveShell.ast_node_interactivity = "all"


class Clima:
    def __init__(self, saludo):
        self.saludo=saludo #creamos el constructor, en este caso no le ponemos ninguna variable global.
    
    def obtener_prediccion(self,dict_countries,product):    #Funcion para obtener datos meteorologicos del tipo
                                                            # product que le indiquemos.
        #El parametro "dict_countries", debe ser un diccionario donde cada key sera un pais y sus values
        #  seran una lista con la latitud y la longitud (en ese orden).
        #El parametro "product" sera a igual a 'civil', 'civillight', 'astro' o 'meteo'.

        df_countries=pd.DataFrame() #creamos un dataframe vacio.

        for key, value in dict_countries.items():   #Hacemos un for loop para obtener los datos meteorologicos
                                                    # de cada pais del diccionario.
            print(key, value)
            url = f'http://www.7timer.info/bin/api.pl?lon={value[1]}&lat={value[0]}&product=meteo&output=json'
            response=requests.get(url=url)
            code=response.status_code
            reason=response.reason
            
            df=pd.DataFrame.from_dict(pd.json_normalize(response.json()['dataseries']))
            df['country']=key
            df_countries=pd.concat([df_countries,df],axis=0,ignore_index=False)
        return df_countries
    
    def obtener_ataques(self,dataframe,lista_paises):
        #Funcion para obtener un dataframe con los ataques ocurridos solo en los paises que aparecen en
        # la lista indicada como parametro "lista_paises". En "dataframe" introduciremos el la variable que
        # almacena el dataframe con los ataque sproducidos en todo el mundo.
        df_ataques_paises=dataframe[dataframe['country'].isin(lista_paises)]
        print('El nuevo dataframe contiene los ataques ocurridos en',df_ataques_paises['country'].unique())
        return df_ataques_paises
    
    def separar_columna_rh(self,dataframe):
        #Funcion para separar una columna que contenga un alista de diccionarios en varias columnas por separado.
        #"dataframe", sera el dataframe donde se encuentra la columna que queremos separar.

        df_rh=dataframe['rh_profile'].apply(pd.Series)

        #Separamos la columna, para ello hacemos un for para iterar por cada una de las columnas del dataframe
        #  generado a partir de la columna que queriamos separar. 
        for i in range(len(df_rh.columns)): 

            #Aplicamos el apply,extraemos el valores de la key "layer" y lo almacenamos en una variable que
            #  convertimos a string.
            nombre = "rh_" + str(df_rh[i].apply(pd.Series)["layer"][0]) 

            #Hacemos lo mismo con una variable que se llame valores para "guardar" los valores de la celda.
            valores = list(df_rh[i].apply(pd.Series)["rh"] )

            #Usamos el método insert de los dataframes para ir añadiendo esta información a el dataframe
            #  con la información del clima. 
            dataframe.insert(i, nombre, valores)
            #dataframe.drop(['rh_profile'],inplace=True,axis=1)
            dataframe=dataframe.reset_index()
            dataframe.drop(['index'],inplace=True,axis=1)
        return dataframe

    def separar_columna_wind(self,dataframe):
        #Funcion para separar una columna que contenga un alista de diccionarios en varias columnas por separado.
        #"dataframe", sera el dataframe donde se encuentra la columna que queremos separar.

        df_wind=dataframe['wind_profile'].apply(pd.Series)

        #Separamos la columna "wind_profile", para ello hacemos un for para iterar por cada una de las columnas. 
        for i in range(len(df_wind.columns)): 

            #Aplicamos el apply,extraemos el valores de la key "layer" y lo almacenamos en una variable
            #  que convertimos a string 
            nombre = "wind_dir_" + str(df_wind[i].apply(pd.Series)["layer"][0]) 
            nombre2 = "wind_spe_" + str(df_wind[i].apply(pd.Series)["layer"][0])

            #Hacemos lo mismo con una variable que se llame valores para "guardar" los valores de la celda.
            direccion = list(df_wind[i].apply(pd.Series)["direction"])

            velocidad= list(df_wind[i].apply(pd.Series)["speed"])

            #Usamos el método insert de los dataframes para ir añadiendo esta información a el dataframe
            #  con la información del clima. 
            dataframe.insert(i, nombre, direccion)
            dataframe.insert(i, nombre2, velocidad)
            #dataframe.drop(['wind_profile'],inplace=True,axis=1)
            dataframe=dataframe.reset_index()
            dataframe.drop(['index'],inplace=True,axis=1)
        return dataframe
    
    def juntar_dataframes(self,dataframe_tiempo,dataframe_ataques):
        #Funcion para juntar dos dataframes, el dataframe que contiene los datos de los ataques y el dataframe
        #  que contiene la informacion climatica.

        #Hacemos el groupby por pais.
        df_agrupado=dataframe_tiempo.groupby('country').mean()
        df_agrupado.reset_index()
        #df_clima3=df_agrupado.drop(['index'],inplace=False,axis=1)
        #df_clima3.reset_index(inplace=True)
        df_agrupado['country']=df_agrupado['country'].str.lower()
        df_mergeado=pd.merge(left=dataframe_ataques,right=df_agrupado,how='left',left_on='country',right_on='country')
        return df_mergeado

    def guardar_dataframe(self,tipo_fichero,dataframe_guardar,direccion_guardado):
        #"tipo_fichero", especificaremos si queremos guardarlo en csv o pickle, debera ir entre comillas.
        #"dataframe_guardar", pondremos la variable que almacena el dataframe que queremos almacenar en un fichero.
        #"direccion_guardado", indicaremos la ruta donde lo vamos a almacenar, debera ir entre comillas.
        if tipo_fichero=='.csv':
            dataframe_guardar.to_csv(direccion_guardado)
            print('Dataframe almacenado como .csv exitosamente en la ubicacion',direccion_guardado)
        elif tipo_fichero=='.pkl':
            dataframe_guardar.to_pickle(direccion_guardado)
            print('Dataframe almacenado como .pkl exitosamente en la ubicacion',direccion_guardado)
        else:
            print('La funcion solo acepta como tipos de fichero ".csv" o ".pkl".')
        return 'Funcion guardar_dataframe finalizada.'








class Carga_sql:

    def __init__(self,host,user,password,nombre_bbdd):#creamos el constructor con sus variables globales.
        self.host=host
        self.user=user
        self.password=password
        self.nombre_bbdd=nombre_bbdd

    
    def crear_database(self): #creamos la funcion para crear la base de datos.
        try:
            cnx = mysql.connector.connect(user=self.user, password=self.password, host=self.host)
            print('te has conectado')
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR or err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Hay un error con tus datos de acceso")
            else:
                print(err)
        mycursor=cnx.cursor()
        try:
            mycursor.execute(f'CREATE DATABASE IF NOT EXISTS {self.nombre_bbdd};')
            print(mycursor)
        except mysql.connector.Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)

        cnx.close()



    def crear_tabla_ataques(self):
        try:
            cnx = mysql.connector.connect(user=self.user, password=self.password, host=self.host,database=self.nombre_bbdd)
            print('te has conectado')
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR or err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Hay un error con tus datos de acceso")
            else:
                print(err)
        mycursor=cnx.cursor()
        try:
            mycursor.execute("""CREATE TABLE IF NOT EXISTS `tabla_ataques` (
                                    `reg_number` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                    `year` INT NOT NULL,
                                    `type` VARCHAR(200) NOT NULL,
                                    `country` VARCHAR(200) NOT NULL,
                                    `age` INT NOT NULL,
                                    `species_` VARCHAR(200) NOT NULL,
                                    `fecha_limpia` VARCHAR(200) NOT NULL,
                                    `fatal` VARCHAR(200) NOT NULL,
                                    `sex` VARCHAR(200) NOT NULL,
                                    `latitud` DECIMAL NOT NULL,
                                    `longitud` DECIMAL NOT NULL,
                                    `country2` VARCHAR(200) NOT NULL,
                                    `fatal_N` INT NOT NULL,
                                    `fatal_Unknown` INT NOT NULL,
                                    `fatal_Y` INT NOT NULL,
                                    `fatal_N.1` INT NOT NULL,
                                    `fatal_Unknown.1` INT NOT NULL,
                                    `fatal_Y.1` INT NOT NULL,
                                    `species_.1` INT NOT NULL,
                                    `fecha_limpia.1` INT NOT NULL,
                                    `type.1` INT NOT NULL,
                                    `age_NORM` DECIMAL NOT NULL)
                                    ;""")
            
            print(mycursor)
        except mysql.connector.Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)

        cnx.close()



    def crear_tabla_clima(self):
        try:
            cnx = mysql.connector.connect(user=self.user, password=self.password, host=self.host,database=self.nombre_bbdd)
            print('te has conectado')
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR or err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Hay un error con tus datos de acceso")
            else:
                print(err)
        mycursor=cnx.cursor()
        try:
            mycursor.execute("""CREATE TABLE IF NOT EXISTS `tabla_clima` (
                                    `country` VARCHAR(200) NOT NULL PRIMARY KEY,
                                    `wind_spe_950mb/n` DECIMAL NOT NULL,
                                    `wind_spe_900mb/n` DECIMAL NOT NULL,
                                    `wind_spe_850mb/n` DECIMAL NOT NULL,
                                    `wind_spe_800mb/n` DECIMAL NOT NULL,
                                    `wind_spe_750mb/n` DECIMAL NOT NULL,
                                    `wind_spe_700mb/n` DECIMAL NOT NULL,
                                    `wind_spe_650mb/n` DECIMAL NOT NULL,
                                    `wind_spe_600mb/n` DECIMAL NOT NULL,
                                    `wind_spe_550mb/n` DECIMAL NOT NULL,
                                    `wind_spe_500mb/n` DECIMAL NOT NULL,
                                    `wind_spe_450mb/n` DECIMAL NOT NULL,
                                    `wind_spe_400mb/n` DECIMAL NOT NULL,
                                    `wind_spe_350mb/n` DECIMAL NOT NULL,
                                    `wind_spe_300mb/n` DECIMAL NOT NULL,
                                    `wind_spe_250mb/n` DECIMAL NOT NULL,
                                    `wind_spe_200mb/n` DECIMAL NOT NULL,
                                    `wind_dir_200mb/n` DECIMAL NOT NULL,
                                    `wind_dir_250mb/n` DECIMAL NOT NULL,
                                    `wind_dir_300mb/n` DECIMAL NOT NULL,
                                    `wind_dir_350mb/n` DECIMAL NOT NULL,
                                    `wind_dir_400mb/n` DECIMAL NOT NULL,
                                    `wind_dir_450mb/n` DECIMAL NOT NULL,
                                    `wind_dir_500mb/n` DECIMAL NOT NULL,
                                    `wind_dir_550mb/n` DECIMAL NOT NULL,
                                    `wind_dir_600mb/n` DECIMAL NOT NULL,
                                    `wind_dir_650mb/n` DECIMAL NOT NULL,
                                    `wind_dir_700mb/n` DECIMAL NOT NULL,
                                    `wind_dir_750mb/n` DECIMAL NOT NULL,
                                    `wind_dir_800mb/n` DECIMAL NOT NULL,
                                    `wind_dir_850mb/n` DECIMAL NOT NULL,
                                    `wind_dir_900mb/n` DECIMAL NOT NULL,
                                    `wind_dir_950mb/n` DECIMAL NOT NULL,
                                    `rh_950mb/n` DECIMAL NOT NULL,
                                    `rh_900mb/n` DECIMAL NOT NULL,
                                    `rh_850mb/n` DECIMAL NOT NULL,
                                    `rh_800mb/n` DECIMAL NOT NULL,
                                    `rh_750mb/n` DECIMAL NOT NULL,
                                    `rh_700mb/n` DECIMAL NOT NULL,
                                    `rh_650mb/n` DECIMAL NOT NULL,
                                    `rh_600mb/n` DECIMAL NOT NULL,
                                    `rh_550mb/n` DECIMAL NOT NULL,
                                    `rh_500mb/n` DECIMAL NOT NULL,
                                    `rh_450mb/n` DECIMAL NOT NULL,
                                    `rh_400mb/n` DECIMAL NOT NULL,
                                    `rh_350mb/n` DECIMAL NOT NULL,
                                    `rh_300mb/n` DECIMAL NOT NULL,
                                    `rh_250mb/n` DECIMAL NOT NULL,
                                    `rh_200mb/n` DECIMAL NOT NULL,
                                    `timepoint` DECIMAL NOT NULL,
                                    `cloudcover` DECIMAL NOT NULL,
                                    `highcloud` DECIMAL NOT NULL,
                                    `midcloud` DECIMAL NOT NULL,
                                    `lowcloud` DECIMAL NOT NULL,
                                    `temp2m` DECIMAL NOT NULL,
                                    `lifted_index` DECIMAL NOT NULL,
                                    `rh2m` DECIMAL NOT NULL,
                                    `msl_pressure` DECIMAL NOT NULL,
                                    `prec_amount` DECIMAL NOT NULL,
                                    `snow_depth` DECIMAL NOT NULL,
                                    `wind10m.speed` DECIMAL NOT NULL)
                                    ;""")
            print(mycursor)
        except mysql.connector.Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)

        cnx.close()



    def insertar_datos_ataques(self,dataframe_ataques): #Creamos una funcion para insertar los datos del dataframe_ataques en la tabla_ataques de MySQL.
        #dataframe_ataques, sera un dataframe con los datos de los ataques
        try:
            cnx = mysql.connector.connect(user=self.user, password=self.password, host=self.host,database=self.nombre_bbdd)
            print('te has conectado')
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR or err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Hay un error con tus datos de acceso")
            else:
                print(err)
        mycursor=cnx.cursor()

        for i, row in dataframe_ataques.iterrows():
            query=f""" INSERT INTO `tabla_ataques` (`year`,`type`,`country`,`age`,`species_`,`fecha_limpia`,`fatal`,`sex`,`latitud`,`longitud`,`country2`,`fatal_N`,`fatal_Unknown`,`fatal_Y`,`fatal_N.1`,`fatal_Unknown.1`,`fatal_Y.1`,`species_.1`,`fecha_limpia.1`,`type.1`,`age_NORM`)
                        VALUES ('{row['year']}','{row['type']}','{row['country']}','{row['age']}','{row['species_']}','{row['fecha_limpia']}','{row['fatal']}','{row['sex']}','{row['latitud']}','{row['longitud']}','{row['country2']}','{row['fatal_N']}','{row['fatal_Unknown']}','{row['fatal_Y']}','{row['fatal_N.1']}','{row['fatal_Unknown.1']}','{row['fatal_Y.1']}','{row['species_.1']}','{row['fecha_limpia.1']}','{row['type.1']}','{row['age_NORM']}')
                        ;"""
            try:
                mycursor.execute(query)
                cnx.commit()
                print(mycursor)
            except mysql.connector.Error as err:
                print(err)
                print("Error Code:", err.errno)
                print("SQLSTATE", err.sqlstate)
                print("Message", err.msg)

        cnx.close()



    def insertar_datos_clima(self,dataframe_ataques): #Creamos una funcion para insertar los datos del dataframe_ataques en la tabla_ataques de MySQL.
        #dataframe_ataques, sera un dataframe con los datos de los ataques
        try:
            cnx = mysql.connector.connect(user=self.user, password=self.password, host=self.host,database=self.nombre_bbdd)
            print('te has conectado')
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR or err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Hay un error con tus datos de acceso")
            else:
                print(err)
        mycursor=cnx.cursor()

        for i, row in dataframe_ataques.iterrows():
            query=f""" INSERT INTO `tabla_clima` (`country`,`wind_spe_950mb/n`,`wind_spe_900mb/n`,`wind_spe_850mb/n`,`wind_spe_800mb/n`,`wind_spe_750mb/n`,`wind_spe_700mb/n`,`wind_spe_650mb/n`,`wind_spe_600mb/n`,`wind_spe_550mb/n`,`wind_spe_500mb/n`,`wind_spe_450mb/n`,`wind_spe_400mb/n`, `wind_spe_350mb/n`,`wind_spe_300mb/n`, `wind_spe_250mb/n`, `wind_spe_200mb/n`,`wind_dir_200mb/n`, `wind_dir_250mb/n`, `wind_dir_300mb/n`, `wind_dir_350mb/n`, `wind_dir_400mb/n`, `wind_dir_450mb/n`,`wind_dir_500mb/n`, `wind_dir_550mb/n`, `wind_dir_600mb/n`,`wind_dir_650mb/n`, `wind_dir_700mb/n`, `wind_dir_750mb/n`,`wind_dir_800mb/n`, `wind_dir_850mb/n`, `wind_dir_900mb/n`, `wind_dir_950mb/n`, `rh_950mb/n`, `rh_900mb/n`, `rh_850mb/n`,`rh_800mb/n`, `rh_750mb/n`, `rh_700mb/n`, `rh_650mb/n`, `rh_600mb/n`, `rh_550mb/n`, `rh_500mb/n`, `rh_450mb/n`, `rh_400mb/n`, `rh_350mb/n`,`rh_300mb/n`, `rh_250mb/n`, `rh_200mb/n`, `timepoint`, `cloudcover`,`highcloud`, `midcloud`, `lowcloud`, `temp2m`, `lifted_index`, `rh2m`,`msl_pressure`, `prec_amount`, `snow_depth`, `wind10m.speed`)
                VALUES ('{row['country']}','{row['wind_spe_950mb/n']}','{row['wind_spe_900mb/n']}','{row['wind_spe_850mb/n']}','{row['wind_spe_800mb/n']}','{row['wind_spe_750mb/n']}','{row['wind_spe_700mb/n']}','{row['wind_spe_650mb/n']}','{row['wind_spe_600mb/n']}','{row['wind_spe_550mb/n']}','{row['wind_spe_500mb/n']}','{row['wind_spe_450mb/n']}','{row['wind_spe_400mb/n']}','{row['wind_spe_350mb/n']}','{row['wind_spe_300mb/n']}','{row['wind_spe_250mb/n']}','{row['wind_spe_200mb/n']}','{row['wind_dir_200mb/n']}','{row['wind_dir_250mb/n']}','{row['wind_dir_300mb/n']}','{row['wind_dir_350mb/n']}','{row['wind_dir_400mb/n']}','{row['wind_dir_450mb/n']}','{row['wind_dir_500mb/n']}','{row['wind_dir_550mb/n']}','{row['wind_dir_600mb/n']}','{row['wind_dir_650mb/n']}','{row['wind_dir_700mb/n']}','{row['wind_dir_750mb/n']}','{row['wind_dir_800mb/n']}','{row['wind_dir_850mb/n']}','{row['wind_dir_900mb/n']}','{row['wind_dir_950mb/n']}','{row['rh_950mb/n']}','{row['rh_900mb/n']}','{row['rh_850mb/n']}','{row['rh_800mb/n']}','{row['rh_750mb/n']}','{row['rh_700mb/n']}','{row['rh_650mb/n']}','{row['rh_600mb/n']}','{row['rh_550mb/n']}','{row['rh_500mb/n']}','{row['rh_450mb/n']}','{row['rh_400mb/n']}','{row['rh_350mb/n']}','{row['rh_300mb/n']}','{row['rh_250mb/n']}','{row['rh_200mb/n']}','{row['timepoint']}','{row['cloudcover']}','{row['highcloud']}','{row['midcloud']}','{row['lowcloud']}','{row['temp2m']}','{row['lifted_index']}','{row['rh2m']}','{row['msl_pressure']}','{row['prec_amount']}','{row['snow_depth']}','{row['wind10m.speed']}')
                ;"""
            try:
                mycursor.execute(query)
                cnx.commit()
                print(mycursor)
            except mysql.connector.Error as err:
                print(err)
                print("Error Code:", err.errno)
                print("SQLSTATE", err.sqlstate)
                print("Message", err.msg)
                pass

        cnx.close()
    










