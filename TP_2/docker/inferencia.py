"""Predice si mañana llueve a partir de las mediciones de un día, con la red neuronal elegida en el TP.

Uso: python inferencia.py entrada.csv salida.csv

La entrada tiene las columnas del dataset (Date, Location, MinTemp, ..., RainToday), una fila por
ciudad y día. La salida es la misma tabla con dos columnas más: la probabilidad de lluvia y el aviso
("Yes" si la probabilidad llega al umbral elegido en validación). No entrena nada: todo lo aprendido
viene en los archivos que guardó el notebook.
"""

import argparse
import json
import os

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")

import joblib
import keras
import numpy as np
import pandas as pd

# El pipeline guardado busca estas funciones por nombre en el programa que lo carga
from transformaciones import con_ubicacion, preparar_variables, redondear_nubosidad  # noqa: F401


def predecir(dias, preprocesamiento, red, umbral):
    """Probabilidad de lluvia y aviso para cada fila, con las columnas que espera el pipeline."""
    faltantes = set(preprocesamiento.feature_names_in_) - set(dias.columns)
    if faltantes:
        raise ValueError(f"Faltan columnas en la entrada: {sorted(faltantes)}")
    entrada = dias[list(preprocesamiento.feature_names_in_)].assign(Date=lambda d: pd.to_datetime(d["Date"]))
    variables = preprocesamiento.transform(entrada)
    probabilidad = red.predict(np.asarray(variables, dtype="float32"), verbose=0).ravel()
    return dias.assign(probabilidad_lluvia=probabilidad.round(4), llueve_manana=np.where(probabilidad >= umbral, "Yes", "No"))


def main():
    parser = argparse.ArgumentParser(description="Predice si mañana llueve en cada ciudad y día de un CSV.")
    parser.add_argument("entrada", help="CSV con las mediciones del día, con las columnas del dataset")
    parser.add_argument("salida", help="CSV donde se escribe la entrada con la probabilidad y el aviso")
    args = parser.parse_args()

    carpeta = os.path.dirname(os.path.abspath(__file__))
    preprocesamiento = joblib.load(os.path.join(carpeta, "preprocesamiento.joblib"))
    red = keras.saving.load_model(os.path.join(carpeta, "red.keras"))
    with open(os.path.join(carpeta, "umbral.json")) as archivo:
        umbral = json.load(archivo)["umbral"]

    dias = pd.read_csv(args.entrada)
    resultado = predecir(dias, preprocesamiento, red, umbral)
    resultado.to_csv(args.salida, index=False)
    print(f"Días: {len(resultado)}  |  Con aviso de lluvia: {(resultado['llueve_manana'] == 'Yes').sum()}  |  "
          f"Umbral: {umbral}  |  Salida: {args.salida}")


if __name__ == "__main__":
    main()
