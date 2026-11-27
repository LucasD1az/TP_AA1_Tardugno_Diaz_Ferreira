FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY inferencia.py transformaciones.py coordenadas_ciudades.csv preprocesamiento.joblib red.keras umbral.json ./

ENTRYPOINT ["python", "inferencia.py"]
