# Coordenadas de las ciudades

El notebook del TP reemplaza la ciudad (`Location`) por la latitud, la longitud, la altura y la distancia
al mar de su estación meteorológica, que lee de una tabla fija: [`coordenadas_ciudades.csv`](../coordenadas_ciudades.csv).
Esa tabla la arma y la controla [`coordenadas.ipynb`](coordenadas.ipynb), en esta carpeta. Todo lo que
dice este README sale de alguna celda de ese notebook, y al lado de cada afirmación está la sección donde
se puede ver.

## Archivos

| Archivo | Qué es |
|---|---|
| `coordenadas.ipynb` | Baja el listado de estaciones, elige la estación de cada ciudad, escribe la tabla y la controla |
| `estaciones_bom.txt` | Copia del listado de estaciones del Bureau of Meteorology que usa el notebook |
| `costa_ne_10m.geojson` | Copia de la línea de costa de Natural Earth que usa el notebook (y el mapa del notebook del TP) |
| `../coordenadas_ciudades.csv` | La tabla que lee el notebook del TP |

La tabla tiene una fila por cada uno de los 49 valores de `Location`, con estas columnas:

| Columna | Contenido |
|---|---|
| `Location` | Nombre de la ciudad, escrito igual que en el dataset |
| `estacion_bom` | Número de la estación en el listado (seis dígitos, con ceros adelante) |
| `nombre_estacion` | Nombre de la estación en el listado |
| `latitud` | Latitud de la estación, en grados decimales (negativa: hemisferio sur) |
| `longitud` | Longitud de la estación, en grados decimales al este de Greenwich |
| `altura_m` | Altura de la estación sobre el nivel del mar, en metros (columna `Height (m)` del listado) |
| `distancia_costa_km` | Distancia de la estación al punto de costa más cercano, en km |

## Fuente

El listado oficial de estaciones del Bureau of Meteorology, el servicio meteorológico de Australia:

```
ftp://ftp.bom.gov.au/anon2/home/ncc/metadata/sitelists/stations.txt
```

Su encabezado lo identifica como el producto `IDCJMC0014`, generado el 10 de junio de 2015. Tiene 20.105
estaciones, históricas y activas, con el año de apertura y de cierre, las coordenadas, de dónde sale cada
coordenada, la altura del barómetro y el número de la Organización Meteorológica Mundial (OMM)
(*El listado de estaciones*). El notebook lo baja la primera vez y guarda la copia
`estaciones_bom.txt`, para que el resultado no dependa de que el archivo siga igual en el servidor.

## Cómo se eligió la estación de cada ciudad

El dataset no dice de qué estación salen los datos de cada ciudad. La correspondencia la armamos con
requisitos y reglas explícitas, que el notebook aplica sin elecciones a mano.

El único dato del listado que se puede contrastar con lo que mide cada ciudad es el barómetro: una
estación sin barómetro no puede registrar presión. En el dataset hay cuatro ciudades sin ningún dato de
presión: Newcastle, Penrith, MountGinini y SalmonGums. Las otras 45 tienen presión en al menos el 62% de
sus días (*Lo que el dataset dice de cada ciudad*).

### Requisitos

Una estación es candidata para una ciudad si (*Candidatas*):

1. Su nombre contiene el de la ciudad, buscado como comienzo de palabra y separado en palabras
   (`GoldCoast` → `GOLD COAST`).
2. Estuvo abierta en algún momento del período de la ciudad en el dataset.
3. Tiene número OMM. Esto es una suposición nuestra para quedarnos con estaciones de observación
   completas, porque el listado no dice qué variables mide cada estación.
4. Su nombre no dice que sea un radar, un perfilador de viento o un anemómetro.
5. Tiene barómetro si la ciudad tiene datos de presión, y no lo tiene si la ciudad nunca los tuvo.

Si ninguna estación con el nombre de la ciudad cumple todo, se toma la que cumpla los demás requisitos
más cercana a alguna de las que tienen el nombre, a no más de 30 km.

El requisito del barómetro descarta 11 estaciones que cumplían todo lo demás, todas sin barómetro y en
ciudades con presión, entre ellas `ALBANY`, `LAUNCESTON (TI TREE BEND)` y `KATHERINE COUNTRY CLUB`. En las
cuatro ciudades sin presión no descarta ninguna: todas sus estaciones que cumplen lo demás ya eran
estaciones sin barómetro. Eso respalda que la falta de altura de barómetro en el listado signifique que no
hay barómetro.

Tres ciudades se resolvieron por cercanía, porque ninguna estación con su nombre cumplía todo:

| Ciudad | Estación | Por qué no hubo candidata con el nombre | Distancia a la estación con el nombre |
|---|---|---|---|
| `Katherine` | 014932 Tindal RAAF | La única con número OMM no tiene barómetro | 9,9 km |
| `Uluru` | 015635 Yulara Airport | `ULURU RANGERS` no tiene número OMM | 19,5 km |
| `Watsonia` | 086068 Viewbank | `WATSONIA LOYOLA` no estuvo abierta durante el período | 4,7 km |

Con estos requisitos, 36 ciudades quedan con una sola candidata, 11 con dos y 2 con tres.

### Reglas para elegir entre varias candidatas

En este orden (*Elección*):

1. Una estación no puede ser de dos ciudades. Así Perth y Sydney pierden la candidata del aeropuerto,
   que es la única de `PerthAirport` y de `SydneyAirport`.
2. Si las candidatas están a más de 100 km entre sí, se elige la más cercana a la estación de la ciudad
   cuya lluvia diaria más se parece. Sólo pasa con Richmond: dos candidatas están en Queensland y una en
   Nueva Gales del Sur. Su lluvia se parece sobre todo a la de Penrith (correlación 0,84), y Richmond RAAF,
   la de Nueva Gales del Sur, está a 16 km de la estación de Penrith; las de Queensland, a más de 1.600.
3. La que estuvo abierta más años del período de la ciudad.
4. La que no es de aeropuerto. El dataset trata a los aeropuertos como ciudades aparte (`SydneyAirport`,
   `PerthAirport`, `MelbourneAirport`), así que suponemos que una ciudad sin "Airport" en el nombre no es
   la del aeropuerto.
5. La que abrió primero.

Las reglas 3 a 5 son convenciones nuestras. Deciden 10 ciudades, y lo que costaría haber elegido mal es
la distancia a la alternativa:

| Ciudad | Estación elegida | Regla | Alternativa | Distancia |
|---|---|---|---|---|
| `Albany` | 009741 Albany Airport Comparison | 3 | 009999 Albany Airport | 1,2 km |
| `CoffsHarbour` | 059040 Coffs Harbour MO | 3 | 059151 Coffs Harbour Airport | 0,9 km |
| `Melbourne` | 086071 Melbourne Regional Office | 3 | 086338 Melbourne (Olympic Park) | 2,2 km |
| `Adelaide` | 023090 Adelaide (Kent Town) | 4 | 023034 Adelaide Airport | 9,9 km |
| `Brisbane` | 040913 Brisbane | 4 | 040842 Brisbane Aero | 13,3 km |
| `Cobar` | 048027 Cobar MO | 4 | 048237 Cobar Airport AWS | 6,8 km |
| `Darwin` | 014072 Darwin NTC AWS | 4 | 014015 Darwin Airport | 7,4 km |
| `Hobart` | 094029 Hobart (Ellerslie Road) | 4 | 094008 Hobart Airport | 15,6 km |
| `Portland` | 090192 Portland NTC AWS | 4 | 090171 Portland (Cashmore Airport) | 12,9 km |
| `Newcastle` | 061055 Newcastle Nobbys Signal Station AWS | 5 | 061390 Newcastle University | 9,1 km |

La mayor es 15,6 km, del orden de la distancia entre las dos ciudades más cercanas del dataset (Perth y
PerthAirport, 9,8 km) y chica frente a los 4.984 km que separan a las dos más lejanas (*Controles*).

De las 49 coordenadas elegidas, 45 están relevadas con GPS, 3 con un relevamiento (`SURVEY`) y una, la de
Darwin NTC AWS, sale de un mapa en escala 1:250.000 (*La tabla*).

## Distancia a la costa

La línea de costa sale de Natural Earth, un conjunto de datos geográficos de uso libre, en su escala más
detallada (1:10.000.000) y en la versión 5.1.2, fijada para que la descarga dé siempre el mismo archivo:

```
https://raw.githubusercontent.com/nvkelso/natural-earth-vector/v5.1.2/geojson/ne_10m_coastline.geojson
```

La costa viene como tramos de puntos. Entre cada par de puntos consecutivos intercalamos puntos hasta que
no queden a más de 0,01 grados ni en latitud ni en longitud, y medimos la distancia de cada estación al
punto más cercano. Así dos puntos consecutivos quedan a menos de 1,6 km, y la distancia calculada exagera
la real en menos de 0,8 km (*Distancia a la costa*).

31 de las 49 ciudades están a menos de 50 km del mar, y la mitad a menos de 26 km. NorfolkIsland queda a
1,9 km, así que su isla está incluida en la línea de costa. Las del interior quedan a cientos de
kilómetros: Cobar a 555, Uluru a 699 y AliceSprings a 895.

La altura está en el listado para las 49 estaciones. La mitad está a menos de 63 m; la más alta es
MountGinini, a 1.760 m (*La tabla*).

En el notebook del TP, la distancia se correlaciona -0,75 (en logaritmo) con la proporción de días con
lluvia de cada ciudad, y a igual distancia las estaciones más altas llueven algo más. Las dos entran al
modelo y al imputador junto con la latitud y la longitud.

## Controles

Los dos controles están en la sección *Controles* del notebook.

El primero es dibujar las 49 estaciones según la tabla sobre la línea de costa (Figura 1). Cada estación
cae dentro de Australia y en su lugar: las ciudades costeras sobre la costa; AliceSprings, Uluru, Woomera,
Cobar y Moree en el interior; Hobart y Launceston en Tasmania; y NorfolkIsland sobre su isla, al este del
continente.

El segundo compara la lluvia con la cercanía. Para cada ciudad se busca la otra cuya lluvia diaria se le
parece más, y se mira en qué puesto queda al ordenar las demás por distancia según la tabla. La lluvia
sólo se usó para elegir la estación de Richmond, así que para las otras 48 ciudades es un control
independiente. En 36 de las 49, la ciudad de lluvia más parecida es la más cercana, y en 44 es una de las
tres más cercanas. Las cinco que quedan afuera (NorfolkIsland, Moree, Nhil, Mildura y Woomera) no tienen
ninguna ciudad de lluvia parecida: la más parecida está a más de 240 km y la correlación no pasa de 0,55.

## Cómo volver a generar la tabla

Desde esta carpeta, con el entorno del repositorio activado:

```bash
jupyter nbconvert --to notebook --execute --inplace coordenadas.ipynb
```

Si `estaciones_bom.txt` o `costa_ne_10m.geojson` no están, el notebook los baja. Con los mismos
archivos, reescribe `../coordenadas_ciudades.csv` exactamente igual.
