"""Las funciones del notebook que usa el pipeline de preprocesamiento.

joblib guarda de estas funciones sólo el nombre, no el código: para cargar
preprocesamiento.joblib tienen que estar definidas en el programa que lo carga.
Son las mismas del notebook (sección "Codificación de variables categóricas" y
"Escalado de los datos"), con las constantes que usan.
"""

from pathlib import Path

import numpy as np
import pandas as pd

RUMBOS = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
ANGULO = {rumbo: 2 * np.pi * i / 16 for i, rumbo in enumerate(RUMBOS)}
DIRECCIONES = {"WindGustDir": "WindGustSpeed", "WindDir9am": "WindSpeed9am", "WindDir3pm": "WindSpeed3pm"}
COORDENADAS = pd.read_csv(Path(__file__).with_name("coordenadas_ciudades.csv"), index_col="Location", dtype={"estacion_bom": str})


def preparar_variables(X):
    """Transformaciones fijas, sin parámetros aprendidos: seno y coseno de direcciones y mes, log de las colas largas."""
    X = X.copy()
    for direccion, velocidad in DIRECCIONES.items():
        angulo = X[direccion].map(ANGULO)
        calma = X[direccion].isna() & X[velocidad].eq(0)
        X[f"{direccion}_sen"] = np.sin(angulo).mask(calma, 0.0)
        X[f"{direccion}_cos"] = np.cos(angulo).mask(calma, 0.0)
    mes = X["Date"].dt.month
    X["mes_sen"] = np.sin(2 * np.pi * mes / 12)
    X["mes_cos"] = np.cos(2 * np.pi * mes / 12)
    X["Rainfall"] = np.log1p(X["Rainfall"])
    X["Evaporation"] = np.log1p(X["Evaporation"])
    return X.drop(columns=["Date", "RainToday", *DIRECCIONES])


def a_ubicacion(X):
    """Reemplaza la ciudad por la latitud, la longitud, la altura y el logaritmo de la distancia a la costa de su estación."""
    desconocidas = set(X["Location"]) - set(COORDENADAS.index)
    if desconocidas:
        raise ValueError(f"Ciudades sin coordenadas en la tabla: {desconocidas}")
    estacion = COORDENADAS.loc[X["Location"]].set_index(X.index)
    return pd.DataFrame({"latitud": estacion["latitud"], "longitud": estacion["longitud"],
                         "altura": estacion["altura_m"], "distancia_costa": np.log1p(estacion["distancia_costa_km"])})


def con_ubicacion(X):
    """Las columnas numéricas con la ciudad reemplazada por los cuatro datos de su ubicación."""
    return X.drop(columns="Location").join(a_ubicacion(X))


def redondear_nubosidad(X):
    """Lleva la nubosidad imputada al octavo entero más cercano."""
    X = X.copy()
    X[["Cloud9am", "Cloud3pm"]] = X[["Cloud9am", "Cloud3pm"]].round()
    return X
