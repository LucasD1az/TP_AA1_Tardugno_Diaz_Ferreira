# AA1-TUIA-Diaz-Tardugno-Ferreira

Trabajos prácticos de **Aprendizaje Automático 1**, Tecnicatura en Inteligencia
Artificial, FCEIA, UNR. Cuatrimestre 2, 2026.

## Integrantes

- Amanda Tardugno
- Lucas Díaz
- Facundo Ferreira

## Contenido del repositorio

| Carpeta | Descripción |
|---|---|
| [`TP_1/`](TP_1/) | TP de regresión: predicción de precios de casas |
| [`TP_2/`](TP_2/) | TP de clasificación: predicción de lluvia en Australia |

Cada carpeta tiene su propio `README.md` con la consigna, los archivos y cómo
correr el notebook. Las instrucciones de entorno de acá abajo valen para todas.

## Preparar el entorno

Requiere **Python 3.12**. Las dependencias se instalan en un entorno virtual
(`.venv/`), que no se versiona: cada uno lo crea en su máquina.

### Crearlo (una sola vez)

Desde la raíz del repositorio:

```bash
python -m venv .venv
```

Activarlo:

```bash
source .venv/bin/activate      # Linux y macOS
.venv\Scripts\activate         # Windows
```

E instalar las bibliotecas:

```bash
pip install -r requirements.txt
```

### Activarlo (cada vez)

Una vez creado, en cada sesión nueva de terminal alcanza con activarlo:

```bash
source .venv/bin/activate      # Linux y macOS
.venv\Scripts\activate         # Windows
```

Se sabe que está activo porque el prompt pasa a mostrar `(.venv)` adelante. Para
salir, `deactivate`.

### Abrir un notebook

Con el entorno activo, desde la raíz del repositorio:

```bash
jupyter notebook TP_1/TP-regresion-AA1.ipynb
jupyter notebook TP_2/TP-clasificacion-AA1.ipynb
```

> **Si usás VS Code** en lugar de Jupyter, elegí `.venv` como kernel
> (**Select Kernel**, arriba a la derecha). Si no, el notebook corre con el
> Python del sistema, que no tiene las bibliotecas instaladas.

## Dependencias

`requirements.txt` fija las versiones exactas de las bibliotecas que usamos de
forma directa, no sus dependencias internas:

```
ipykernel      jupyter        matplotlib
numpy          pandas         scikit-learn      seaborn
shap
```

PyCaret, que usa el ítem 6 del TP 2, no entra en este entorno: necesita Python
3.11 y versiones viejas de scikit-learn y pandas. Corre en un entorno aparte,
`.venv-pycaret/`, con sus propias instrucciones en
[`TP_2/automl/README.md`](TP_2/automl/README.md).

Si se suma una biblioteca nueva, se la agrega a mano al archivo con la versión
que quedó instalada. Para averiguarla:

```bash
pip show <biblioteca> | grep -i version
```

La razón de fijar versiones es que los resultados de los notebooks se puedan
reproducir tal cual: algunas funciones de scikit-learn cambiaron de firma entre
versiones y los números no darían iguales.
