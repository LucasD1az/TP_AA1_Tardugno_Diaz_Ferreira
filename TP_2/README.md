# TP 2 — Clasificación: predicción de lluvia en Australia

Segundo trabajo práctico de **Aprendizaje Automático 1**. Los integrantes y las instrucciones para armar el entorno están en el [README del repositorio](../README.md).

## Problema

Predecir, a las 23:59 de cada día, si al día siguiente va a llover en una ciudad de Australia (`RainTomorrow`, `Yes` / `No`), a partir de las observaciones meteorológicas de ese día: temperaturas, lluvia, sol, nubosidad, viento, humedad y presión, junto con la ciudad y la fecha.

Como la variable a predecir es una de dos categorías, es un problema de clasificación binaria. El enunciado pide resolverlo con regresión logística y con una red neuronal, compararlos, y poner el modelo elegido en producción con Docker.

## Archivos

| Archivo | Descripción |
|---|---|
| `TP-clasificacion-AA1.ipynb` | **Notebook con el desarrollo.** Es la entrega |
| `weatherAUS_2026C2.csv` | Dataset: 145.412 filas y 25 columnas, 49 ciudades entre 2007 y 2017 |
| `coordenadas_ciudades.csv` | Latitud, longitud, altura y distancia a la costa de la estación meteorológica de cada ciudad. La lee el notebook |
| `coordenadas/` | El notebook que arma y controla la tabla de coordenadas (`coordenadas.ipynb`), las copias del listado de estaciones y de la línea de costa que usa, y un [README](coordenadas/README.md) con el resumen de cómo se eligió cada estación |
| `TrabajoPrácticoClasificacionAA1_2026C2.pdf` | Consigna de la cátedra |

Las definiciones de las variables son las de la [descripción del dataset en Kaggle](https://www.kaggle.com/datasets/arunavakrchakraborty/australia-weather-data/data).

## Cómo correrlo

Con el entorno activado (ver el [README del repositorio](../README.md)):

```bash
jupyter notebook TP-clasificacion-AA1.ipynb
```

El notebook lee el dataset y la tabla de coordenadas desde esta misma carpeta y se ejecuta de principio a fin en orden, sin pasos manuales intermedios. La semilla está fijada, así que los números son los mismos en cada corrida. Casi todo el tiempo de una corrida se va en la imputación por regresión, que se ajusta dos veces: una en la comparación de métodos y otra en el preprocesamiento final.

## Cómo está organizado el notebook

### Análisis descriptivo y preprocesamiento

Recorrido de las variables, chequeos de consistencia, análisis de faltantes, balance de clases, división en entrenamiento / validación / prueba, visualizaciones, transformación logarítmica, codificación, imputación, matriz de correlación y escalado.

Las decisiones que más pesan en el resultado, todas justificadas en el notebook:

- Se descarta `RainfallTomorrow`: `RainTomorrow` es exactamente esa columna cortada en 1 mm, así que es la respuesta. También `RainToday`, que es `Rainfall` cortada en 1 mm y no agrega información.
- Se eliminan las 3.259 filas sin `RainTomorrow` y las 2.085 con la mitad o más de las variables vacías: el 3,68% del archivo.
- La división es por fecha (70% / 10% / 20%), no al azar: el modelo siempre predice el futuro, y las ciudades vecinas coinciden en la lluvia el mismo día. Prueba va de noviembre de 2015 a junio de 2017.
- Los faltantes son en su mayoría estructurales (estaciones que nunca miden una variable). Se imputan con regresión a partir de las otras variables del mismo día y de la ubicación de la estación (`IterativeImputer`), elegida comparando contra la mediana global y la mediana por ciudad y mes sobre valores ocultos a propósito.
- Las direcciones de viento y el mes se codifican con seno y coseno. Los momentos de calma, que no tienen dirección, van al centro del círculo.
- La ciudad se reemplaza por cuatro datos de su estación meteorológica: latitud, longitud, altura y distancia a la costa (en logaritmo). Salen del listado oficial de estaciones del Bureau of Meteorology y de la línea de costa de Natural Earth (detalle en [`coordenadas/README.md`](coordenadas/README.md)). Así las ciudades cercanas, como Sydney y SydneyAirport, quedan con valores cercanos, que one-hot no puede representar porque trata a cada ciudad como independiente. Entre ciudades, la distancia a la costa se correlaciona -0,75 con la proporción de días con lluvia, y a igual distancia las estaciones más altas llueven algo más. Las cuatro columnas entran al modelo y también al imputador.

Todo el preprocesamiento está en un único `Pipeline` de scikit-learn, ajustado sólo con entrenamiento. Quedan 98.004 / 14.016 / 28.048 filas con 28 columnas.

### Regresión logística

La clase positiva es la lluvia, y un falso negativo (no avisar y que llueva) se considera peor que una falsa alarma. Por eso el criterio, fijado antes de ver resultados, es maximizar el recall de la lluvia con una precisión de al menos 0,5.

- Se comparan dos modelos, sin balanceo y con `class_weight="balanced"`. Tienen prácticamente el mismo AUC (0,872 y 0,873) y, cada uno con su umbral, los mismos errores: balancear equivale a bajar el umbral, y además infla las probabilidades. Se elige el modelo sin balanceo.
- El umbral se elige en validación: 0,19, no 0,5. El umbral más cercano a la esquina de la curva ROC, usado como control, cae cerca (0,212), un poco más arriba porque pesa igual los dos errores.
- No hay sobreajuste (entrenamiento y validación dan casi igual), y con menos regularización el modelo no se ajusta mejor: el límite es la frontera lineal.
- En prueba detecta el 81,1% de los días de lluvia, con una precisión de 0,484, apenas por debajo del piso, y un AUC de 0,864.

### Modelo base

Siempre "No" (accuracy 0,776, no detecta ninguna lluvia), aleatorio con la proporción de lluvia de entrenamiento (recall 0,225, sobre la diagonal de la curva ROC) y persistencia: mañana llueve si hoy llovió más de 1 mm (recall 0,443). Con la misma tasa de falsas alarmas que la persistencia, la regresión logística detecta el 71,1% de las lluvias contra el 44,3%. Su log loss (0,359) es un tercio menor que la de darle a todos los días la proporción de lluvia de entrenamiento (0,532).

## Estado

| Ítem de la consigna | Estado |
|---|---|
| 1. Análisis descriptivo y preprocesamiento | Completo |
| 2. Regresión logística | Completo |
| 3. Modelo base | Completo |
| 4. Optimización de hiperparámetros | Pendiente |
| 5. Explicabilidad | Pendiente |
| 6. AutoML con PyCaret | Pendiente |
| 7. Red neuronal | Pendiente |
| 8. Comparación de modelos | Pendiente |
| 9. MLOps | Pendiente |
| 10. Conclusión | Pendiente |

Entregas parciales: ítems 1 a 3 hasta el 30/10, 4 a 6 hasta el 13/11, y 7 a 10 hasta el 27/11.
