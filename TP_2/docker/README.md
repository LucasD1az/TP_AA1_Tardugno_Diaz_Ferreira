# Predicción de lluvia con Docker

Imagen que predice, a partir de las mediciones de un día, si al día siguiente llueve en cada ciudad. Usa
el modelo elegido en el [notebook del TP](../TP-clasificacion-AA1.ipynb): la red neuronal optimizada, con
el umbral elegido en validación. La sección "MLOps" del notebook guarda los archivos del modelo en esta
carpeta y verifica que `inferencia.py` reproduce sus predicciones.

## Archivos

| Archivo | Qué es |
|---|---|
| `inferencia.py` | Carga el modelo y predice. No entrena nada |
| `transformaciones.py` | Las funciones del notebook que usa el preprocesamiento: joblib guarda sólo su nombre, y tienen que existir para cargarlo |
| `preprocesamiento.joblib` | El `Pipeline` de scikit-learn ajustado con entrenamiento: transformaciones fijas, ubicación de la ciudad, imputación y escalado |
| `red.keras` | La red neuronal entrenada |
| `umbral.json` | El umbral de probabilidad a partir del cual se avisa lluvia |
| `coordenadas_ciudades.csv` | Latitud, longitud, altura y distancia a la costa de la estación de cada ciudad, que usa el preprocesamiento |
| `requirements.txt` | Las bibliotecas de la inferencia, con las versiones con las que se entrenó |
| `Dockerfile` | La receta de la imagen |
| `ejemplo_entrada.csv` | Un día para probar: el último del conjunto de prueba, con todas las ciudades que midieron ese día |

## Entrada y salida

La entrada es un CSV con las columnas del dataset, una fila por ciudad y día: `Date`, `Location`,
`MinTemp`, `MaxTemp`, `Rainfall`, `Evaporation`, `Sunshine`, `WindGustDir`, `WindGustSpeed`, `WindDir9am`,
`WindDir3pm`, `WindSpeed9am`, `WindSpeed3pm`, `Humidity9am`, `Humidity3pm`, `Pressure9am`, `Pressure3pm`,
`Cloud9am`, `Cloud3pm`, `Temp9am`, `Temp3pm` y `RainToday`. Los valores faltantes se dejan vacíos: el
preprocesamiento los imputa. Si hay columnas de más (por ejemplo `RainTomorrow`), se ignoran; si falta
alguna, el script avisa cuál. La ciudad tiene que ser una de las 49 de `coordenadas_ciudades.csv`.

La salida es la misma tabla con dos columnas más: `probabilidad_lluvia` y `llueve_manana` (`Yes` si la
probabilidad llega al umbral, `No` si no).

## Armar la imagen

Una sola vez, desde esta carpeta (`TP_2/docker/`):

```bash
docker build -t prediccion-lluvia .
```

Tarda unos minutos la primera vez, casi todo en instalar TensorFlow. La imagen pesa unos 2 GB.

## Correr el contenedor

Desde esta misma carpeta, con el día de ejemplo:

```bash
docker run --rm -v "$(pwd)":/datos prediccion-lluvia /datos/ejemplo_entrada.csv /datos/ejemplo_salida.csv
```

- `--rm` borra el contenedor al terminar.
- `-v "$(pwd)":/datos` hace que la carpeta actual se vea dentro del contenedor como `/datos`: de ahí lee la
  entrada y ahí escribe la salida.
- `prediccion-lluvia` es la imagen que se armó en el paso anterior.
- Los dos últimos argumentos son el CSV de entrada y el de salida, con la ruta que tienen dentro del
  contenedor.

Para predecir otros días, se pone el CSV en la carpeta que se monta y se cambian los nombres:

```bash
docker run --rm -v "$(pwd)":/datos prediccion-lluvia /datos/mis_dias.csv /datos/mis_predicciones.csv
```

En Windows (PowerShell), `"$(pwd)"` se reemplaza por `"${PWD}"`.

Si el contenedor dice que no encuentra el archivo de entrada aunque esté en la carpeta, es probable que
Docker no tenga acceso a esa carpeta. Pasa, por ejemplo, con Docker instalado como snap en Ubuntu, que
sólo puede leer carpetas dentro de `/home`: hay que correrlo desde una carpeta ahí adentro.
