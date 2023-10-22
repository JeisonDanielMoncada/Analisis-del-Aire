import pandas as pd
import requests
import sqlite3



def ej_1_cargar_datos_demograficos() -> pd.DataFrame:
    data = pd.read_csv('us-cities-demographics.csv',sep=';')
    data = pd.DataFrame(data)
    return data

def ej_3_limpiar_data() -> pd.DataFrame:
    data= data.drop(['Race', 'Count', 'Number of Veterans'], axis=1)
    data = data.drop_duplicates()
    data.to_csv('us-cities_limpio.csv', index=False)
    return data

def ej_2_cargar_calidad_aire(data: pd.DataFrame) -> None:
    resultado = []
    overall_aqit = []
    city_list = data['City']
    city_lit=[]
    for city in city_list:
        api_url = f'https://api.api-ninjas.com/v1/airquality?city={city}'
        response = requests.get(api_url, headers={'X-Api-Key': 'tnAXTjhGJUF9FCVvRZqenQ==A8xoElsrHq8rJZ3h'})
        dimenciones = []
        if response.status_code == requests.codes.ok:
            city_res=response.json()
            for clave, valor in city_res.items():
                if clave != "overall_aqi":
                    if clave != "overall_aqi":
                        del valor['aqi']
                        dimenciones.append(valor['concentration'])
            if clave == "overall_aqi":
                overall_aqi= city_res['overall_aqi']
                overall_aqit.append(overall_aqi)
            resultado.append(dimenciones)
            city_lit.append(city)
        else:
            print("Error:", response.status_code, response.text)
    city_lit= pd.DataFrame(city_lit)
    city_lit = city_lit.rename(columns={0:'City'})
    resultado = pd.DataFrame(resultado)
    resultado = resultado.rename(columns={0:'CO', 1:'NO2', 2:'O3', 3:'SO2', 4:'PM2.5', 5:'PM10'})
    overall_aqit = pd.DataFrame(overall_aqit)
    overall_aqit = overall_aqit.rename(columns={0:'overall_aqi'})
    base = pd.concat([city_lit, resultado, overall_aqit], axis=1)
    base.set_index('City', inplace=True)
    base.to_csv('ciudades.csv')
    return base


ciudades = pd.read_csv('ciudades.csv')
poblacion = pd.read_csv('us-cities_limpio.csv')

conn = sqlite3.connect('analisis_de_aire.db')

conn.execute('PRAGMA user_id = "jmoncada"')
conn.execute('PRAGMA password = "Joha0723"')

ciudades.to_sql('ciudades', conn, if_exists='replace', index=False)
poblacion.to_sql('poblacion', conn, if_exists='replace', index=False)

conn.close()




    