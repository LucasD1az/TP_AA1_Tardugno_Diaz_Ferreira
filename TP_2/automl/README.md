# AutoML con PyCaret

El ítem 6 del TP compara la regresión logística con los modelos que prueba PyCaret. La comparación corre
en [`automl_pycaret.ipynb`](automl_pycaret.ipynb), en esta carpeta, y la lectura de los resultados está
en la sección "AutoML con PyCaret" del [notebook del TP](../TP-clasificacion-AA1.ipynb).

Está aparte porque PyCaret 3.3.2, la última versión, sólo funciona con Python 3.9 a 3.11, y baja
scikit-learn a 1.4.2 y pandas a 2.1.4. El notebook del TP usa Python 3.12, scikit-learn 1.9.1 y pandas
3.0.6, y con las versiones viejas deja de correr.

## Archivos

| Archivo | Qué es |
|---|---|
| `automl_pycaret.ipynb` | Arma el experimento de PyCaret con los mismos folds por año y la misma métrica que la búsqueda de hiperparámetros, compara los modelos y guarda los resultados |
| `requirements.txt` | Las bibliotecas del entorno de PyCaret |
| `datos/entrenamiento.csv.gz` | Entrenamiento ya preprocesado, con el año de cada día y `RainTomorrow`. Lo escribe el notebook del TP |
| `datos/validacion.csv.gz` | Validación ya preprocesada, con `RainTomorrow`. Lo escribe el notebook del TP |
| `resultados/comparacion.csv` | Las métricas de cada modelo, promediadas en los cinco folds por año |
| `resultados/recall_por_anio.csv` | El recall con precisión de al menos 0,5 de los tres mejores modelos y de la regresión logística, en cada año |
| `resultados/probabilidades_validacion.csv.gz` | La probabilidad de lluvia que cada uno de esos modelos le asigna a cada día de validación |

Prueba no se exporta: no participa de ninguna decisión.

## Orden de ejecución

1. El notebook del TP, hasta la celda que exporta los datos a `datos/` (sección "AutoML con PyCaret").
2. `automl_pycaret.ipynb`, con el entorno de esta carpeta. Escribe `resultados/`.
3. El resto del notebook del TP, que lee `resultados/`.

Los datos y los resultados están en el repositorio, así que el notebook del TP corre entero sin el
paso 2. Sólo hace falta volver a correr `automl_pycaret.ipynb` si cambia el preprocesamiento.

## Preparar el entorno

Hace falta Python 3.11. Si no está instalado, la forma más simple es con
[uv](https://docs.astral.sh/uv/), que lo baja aparte sin tocar el Python del sistema. Desde la raíz del
repositorio:

```bash
pip install uv                                   # una sola vez, en cualquier entorno
uv python install 3.11
uv venv --python 3.11 .venv-pycaret
uv pip install --python .venv-pycaret -r TP_2/automl/requirements.txt
```

Para usarlo como kernel de Jupyter o de VS Code:

```bash
.venv-pycaret/bin/python -m ipykernel install --user --name aa1-pycaret --display-name "Python 3.11 (PyCaret)"
```

En VS Code, elegir **Python 3.11 (PyCaret)** como kernel de `automl_pycaret.ipynb` (y `.venv` para el
notebook del TP). `.venv-pycaret/` no se versiona, igual que `.venv/`.

`six` está en `requirements.txt` aunque el notebook no la use: PyCaret la necesita al importarse y no
la instala sola.

Una corrida completa de `automl_pycaret.ipynb` tarda unos 5 minutos.
