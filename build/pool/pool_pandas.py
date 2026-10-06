# -*- coding: utf-8 -*-
"""Módulo 01 · Pandas: Series, operaciones y primer contacto con tablas."""

EXERCISES = [
# =========================================================== Series
dict(id="pd01", sec="Series: la pieza básica", title="Hola, pandas 👋", level=1,
theory="""**pandas** es la librería de Python para trabajar con datos en forma de tabla. Es la herramienta número uno de analistas, científicos e ingenieros de datos: con ella se leen archivos, se limpian datos, se calculan métricas y se preparan datos para modelos de Machine Learning.

Todo en pandas se construye con dos piezas:
- **Series**: una columna de datos con etiquetas.
- **DataFrame**: una tabla, que en el fondo es un conjunto de Series que comparten las mismas etiquetas.

Una Series tiene **valores** y un **índice** (las etiquetas de cada valor). Si no indicas el índice, pandas usa 0, 1, 2…

```python
import pandas as pd   # "pd" es el alias estándar que usa todo el mundo

temperaturas = pd.Series([22, 25, 19], index=["lun", "mar", "mié"])
print(temperaturas)
# lun    22
# mar    25
# mié    19
# dtype: int64
```
El `dtype` final indica el **tipo de dato** de los valores (int64 = números enteros).

> 💼 **En el trabajo:** cada columna que leas de un Excel, un CSV o una base de datos llega a pandas como una Series.""",
task="Crea una Series con los valores `10, 20, 30` y el índice `'a', 'b', 'c'`. Guárdala en la variable `resultado`.",
starter="# pandas ya está importado como pd\n# Escribe tu código aquí 👇\nresultado = ",
solution="resultado = pd.Series([10, 20, 30], index=['a', 'b', 'c'])",
hint="pd.Series([10, 20, 30], index=['a', 'b', 'c'])",
sql="-- En SQL no hay Series: equivale a una sola columna\nSELECT valor FROM tabla;"),

dict(id="pd02", sec="Series: la pieza básica", title="Series desde un diccionario", level=1,
theory="""Muchas veces los datos ya vienen como **diccionario** de Python: pares `clave: valor`. Si le pasas un diccionario a `pd.Series`, las **claves pasan a ser el índice** y los **valores**, los datos.

```python
poblacion = pd.Series({"Madrid": 3.3, "Lima": 10.0, "Bogotá": 7.9})
# Madrid     3.3
# Lima      10.0
# Bogotá     7.9
# dtype: float64
```

Esto es muy útil porque el índice deja de ser un número sin significado y pasa a describir cada dato.

> 💡 El orden se respeta: pandas usa el mismo orden en que escribiste las claves.""",
task="Crea una Series a partir del diccionario `{'Lun': 120, 'Mar': 95, 'Mié': 143}`, que representa las ventas de tres días. Guárdala en `resultado`.",
starter="ventas = {'Lun': 120, 'Mar': 95, 'Mié': 143}\nresultado = ",
solution="ventas = {'Lun': 120, 'Mar': 95, 'Mié': 143}\nresultado = pd.Series(ventas)",
hint="pd.Series(ventas)",
sql="SELECT dia, ventas FROM ventas_semana;"),

dict(id="pd03", sec="Series: la pieza básica", title="Etiqueta o posición", level=2,
theory="""Hay dos formas de sacar un valor de una Series, y conviene distinguirlas bien desde el principio:

- `.loc[etiqueta]`: busca por la **etiqueta** del índice.
- `.iloc[posición]`: busca por la **posición** (0 es el primero y -1 el último, como en las listas de Python).

```python
s = pd.Series([22, 25, 19], index=["lun", "mar", "mié"])
s.loc["mar"]   # 25  -> por etiqueta
s.iloc[0]      # 22  -> primera posición
s.iloc[-1]     # 19  -> última posición
```

También puedes escribir `s["mar"]`, pero usar `loc` e `iloc` deja clarísimo qué quieres decir.

> ⚠️ **Error común:** usar `iloc` con una etiqueta (`s.iloc["mar"]`) da error, porque `iloc` solo acepta números de posición.""",
task="Con la Series `ventas`, guarda en `resultado` una **lista** con dos valores: las ventas del **Mié** (por etiqueta, con `loc`) y las ventas del **primer día** (por posición, con `iloc`).",
starter="ventas = pd.Series({'Lun': 120, 'Mar': 95, 'Mié': 143, 'Jue': 88, 'Vie': 170})\nresultado = [ , ]",
solution="ventas = pd.Series({'Lun': 120, 'Mar': 95, 'Mié': 143, 'Jue': 88, 'Vie': 170})\nresultado = [ventas.loc['Mié'], ventas.iloc[0]]",
hint="[ventas.loc['Mié'], ventas.iloc[0]]",
sql="SELECT ventas FROM ventas_semana WHERE dia = 'Mié';"),

# =========================================================== Operaciones
dict(id="pd04", sec="Operaciones con Series", title="Cálculos sin bucles", level=1,
theory="""La gran ventaja de pandas son las **operaciones vectorizadas**: escribes la operación una vez y se aplica a **todos los valores a la vez**, sin bucles `for`. Además de más cómodo, es muchísimo más rápido.

```python
precios = pd.Series([100, 200], index=["A", "B"])
precios * 2        # A 200, B 400
precios + 10       # A 110, B 210
precios / 100      # A 1.0, B 2.0
```

El índice se conserva, así que cada resultado sigue sabiendo a qué producto pertenece.

> 💼 **En el trabajo:** aplicar impuestos, convertir monedas o pasar de gramos a kilos se hace con una sola línea como esta.""",
task="Los precios de la Series `precios` no incluyen el IVA. Calcula el precio **con un IVA del 21%** (multiplica por `1.21`) y guarda la Series en `resultado`.",
starter="precios = pd.Series([100, 250, 80, 40], index=['Mouse', 'Teclado', 'Webcam', 'Cable'])\nresultado = ",
solution="precios = pd.Series([100, 250, 80, 40], index=['Mouse', 'Teclado', 'Webcam', 'Cable'])\nresultado = precios * 1.21",
hint="precios * 1.21",
sql="SELECT producto, precio * 1.21 FROM productos;"),

dict(id="pd05", sec="Operaciones con Series", title="Filtrar valores", level=2,
theory="""Cuando comparas una Series con un valor (`precios > 90`), obtienes otra Series de **True/False**, llamada **máscara booleana**. Si la pones entre corchetes, pandas **se queda solo con los valores True**:

```python
edades = pd.Series([15, 32, 17, 45])
edades > 18            # False, True, False, True
edades[edades > 18]    # 32, 45
```

Operadores de comparación: `>`, `<`, `>=`, `<=`, `==` (igual) y `!=` (distinto).

> 💡 Piénsalo en dos pasos: primero **preguntas** (la máscara) y después **filtras** con esa respuesta.""",
task="De la Series `precios`, quédate solo con los productos que cuestan **más de 90**. Guarda el resultado en `resultado`.",
starter="precios = pd.Series([100, 250, 80, 40], index=['Mouse', 'Teclado', 'Webcam', 'Cable'])\nresultado = ",
solution="precios = pd.Series([100, 250, 80, 40], index=['Mouse', 'Teclado', 'Webcam', 'Cable'])\nresultado = precios[precios > 90]",
hint="precios[precios > 90]",
sql="SELECT * FROM productos WHERE precio > 90;"),

dict(id="pd06", sec="Operaciones con Series", title="Estadística exprés", level=1,
theory="""Las Series traen métodos para resumir datos en un solo número:

| Método | Qué calcula |
|---|---|
| `.sum()` | suma |
| `.mean()` | media (promedio) |
| `.median()` | mediana (el valor del medio) |
| `.min()` / `.max()` | mínimo / máximo |
| `.std()` | desviación estándar (cuánto se dispersan los datos) |
| `.count()` | cantidad de valores no nulos |

```python
notas = pd.Series([6, 8, 10])
notas.mean()   # 8.0
notas.max()    # 10
```

> 💼 **En el trabajo:** "¿cuál es el ticket medio?", "¿cuál fue la venta máxima?"… son preguntas que se responden con estos métodos.""",
task="Calcula la **nota media** de la Series `notas` y guárdala en `resultado`.",
starter="notas = pd.Series([7, 9, 6, 8, 10, 5], index=['Ana', 'Bruno', 'Carla', 'Diego', 'Elena', 'Facu'])\nresultado = ",
solution="notas = pd.Series([7, 9, 6, 8, 10, 5], index=['Ana', 'Bruno', 'Carla', 'Diego', 'Elena', 'Facu'])\nresultado = notas.mean()",
hint="notas.mean()",
sql="SELECT AVG(nota) FROM notas;"),

dict(id="pd07", sec="Operaciones con Series", title="Ordenar un ranking", level=1,
theory="""`sort_values()` ordena los **valores** de menor a mayor. Con `ascending=False` se ordenan de mayor a menor, que es lo que normalmente quieres para un ranking. Cada valor conserva su etiqueta.

```python
goles = pd.Series({"Ana": 3, "Luis": 7, "Eva": 5})
goles.sort_values(ascending=False)
# Luis    7
# Eva     5
# Ana     3
```

Existe también `sort_index()`, que ordena por las **etiquetas** (alfabéticamente, por ejemplo).""",
task="Ordena la Series `notas` de la **nota más alta a la más baja** y guarda el resultado.",
starter="notas = pd.Series([7, 9, 6, 8, 10, 5], index=['Ana', 'Bruno', 'Carla', 'Diego', 'Elena', 'Facu'])\nresultado = ",
solution="notas = pd.Series([7, 9, 6, 8, 10, 5], index=['Ana', 'Bruno', 'Carla', 'Diego', 'Elena', 'Facu'])\nresultado = notas.sort_values(ascending=False)",
hint="notas.sort_values(ascending=False)",
sql="SELECT * FROM notas ORDER BY nota DESC;"),

dict(id="pd08", sec="Operaciones con Series", title="Datos que faltan", level=2,
theory="""En los datos reales casi siempre **faltan valores**. pandas los representa como `NaN` (*Not a Number*). Para detectarlos:

- `.isna()` devuelve True donde falta el dato.
- `.notna()` devuelve lo contrario.

Como True cuenta como 1 y False como 0, `.isna().sum()` te dice **cuántos datos faltan**:

```python
s = pd.Series([1, None, 3, None])
s.isna()         # False, True, False, True
s.isna().sum()   # 2
```

> ⚠️ **Error común:** comparar con `== None` o `== np.nan` **no funciona**. Usa siempre `isna()`.

> 💼 **En el trabajo:** lo primero que se hace con un dataset nuevo es contar los nulos de cada columna.""",
task="La Series `temperaturas` tiene lecturas faltantes. Cuenta **cuántos valores faltan** y guarda ese número en `resultado`.",
starter="temperaturas = pd.Series([21.5, None, 19.8, 25.1, None, 22.4, None])\nresultado = ",
solution="temperaturas = pd.Series([21.5, None, 19.8, 25.1, None, 22.4, None])\nresultado = temperaturas.isna().sum()",
hint="temperaturas.isna().sum()",
sql="SELECT COUNT(*) FROM lecturas WHERE temperatura IS NULL;"),

dict(id="pd09", sec="Operaciones con Series", title="Traducir valores con map", level=2,
theory="""`.map(diccionario)` reemplaza cada valor por el que le corresponde en el diccionario. Es perfecto para **traducir códigos** a textos legibles, o al revés.

```python
estado = pd.Series(["A", "C", "A"])
estado.map({"A": "Activo", "C": "Cancelado"})
# Activo, Cancelado, Activo
```

> ⚠️ Si un valor no está en el diccionario, el resultado es `NaN`. Revisa siempre que el diccionario cubra todos los casos.""",
task="Traduce los talles de la Series `talles`: `S` → `Chico`, `M` → `Mediano`, `L` → `Grande`. Guarda la Series traducida en `resultado`.",
starter="talles = pd.Series(['S', 'M', 'L', 'M', 'S'])\nresultado = ",
solution="talles = pd.Series(['S', 'M', 'L', 'M', 'S'])\nresultado = talles.map({'S': 'Chico', 'M': 'Mediano', 'L': 'Grande'})",
hint="talles.map({'S': 'Chico', 'M': 'Mediano', 'L': 'Grande'})",
sql="SELECT CASE talle WHEN 'S' THEN 'Chico' WHEN 'M' THEN 'Mediano' ELSE 'Grande' END FROM ropa;"),

dict(id="pd10", sec="Operaciones con Series", title="Tu propia función con apply", level=3,
theory="""Cuando la lógica es más compleja que una simple operación, puedes escribir **tu propia función** y aplicarla a cada valor con `.apply(funcion)`:

```python
def clasificar(nota):
    if nota >= 6:
        return "aprobado"
    return "desaprobado"

notas.apply(clasificar)
```

También puedes usar una función anónima en una línea, con `lambda`:

```python
notas.apply(lambda n: "aprobado" if n >= 6 else "desaprobado")
```

> 💡 `apply` es flexible pero más lento que las operaciones vectorizadas. Úsalo cuando no haya una alternativa directa.""",
task="""Escribe una función que clasifique cada temperatura de `temperaturas`:
- **"frío"** si es menor que 20,
- **"templado"** si está entre 20 y 25 (ambos incluidos),
- **"calor"** si es mayor que 25.

Aplícala con `apply` y guarda la Series resultante en `resultado`.""",
starter="temperaturas = pd.Series([18.5, 22.0, 26.3, 20.0, 25.0, 31.2])\n\ndef clasificar(t):\n    # completa aquí\n    pass\n\nresultado = temperaturas.apply(clasificar)",
solution="temperaturas = pd.Series([18.5, 22.0, 26.3, 20.0, 25.0, 31.2])\n\ndef clasificar(t):\n    if t < 20:\n        return 'frío'\n    if t <= 25:\n        return 'templado'\n    return 'calor'\n\nresultado = temperaturas.apply(clasificar)",
hint="if t < 20: return 'frío' / if t <= 25: return 'templado' / return 'calor'",
sql="SELECT CASE WHEN t < 20 THEN 'frío' WHEN t <= 25 THEN 'templado' ELSE 'calor' END FROM lecturas;"),

dict(id="pd11", sec="Operaciones con Series", title="Limpiar texto con .str", level=2,
theory="""Las Series de texto tienen el accesor **`.str`**, con los métodos de texto de Python pero **vectorizados** (se aplican a todos los valores a la vez):

```python
s.str.strip()       # quita los espacios del principio y del final
s.str.lower()       # minúsculas
s.str.upper()       # MAYÚSCULAS
s.str.title()       # Primera Letra En Mayúscula
s.str.len()         # largo de cada texto
s.str.contains("x") # True si contiene "x"
```

Se pueden **encadenar** uno detrás de otro: `s.str.strip().str.lower()`.

> 💼 **En el trabajo:** los nombres escritos a mano por personas llegan con espacios de más y mayúsculas mezcladas. Normalizarlos es tarea de todos los días.""",
task="Limpia la Series `nombres`: quita los espacios sobrantes y déjalos en formato Título (`Ana`, `Bruno`...). Guarda el resultado.",
starter="nombres = pd.Series(['  ana ', 'BRUNO', 'carla  ', 'dIEGO'])\nresultado = ",
solution="nombres = pd.Series(['  ana ', 'BRUNO', 'carla  ', 'dIEGO'])\nresultado = nombres.str.strip().str.title()",
hint="nombres.str.strip().str.title()",
sql="SELECT INITCAP(TRIM(nombre)) FROM personas;"),

# =========================================================== DataFrame
dict(id="pd12", sec="Del Series al DataFrame", title="Tu primer DataFrame", level=1,
theory="""Un **DataFrame** es una tabla: filas y columnas, como una hoja de Excel. Cada columna es una Series y todas comparten el mismo índice (las etiquetas de las filas).

La forma más habitual de crear uno a mano es con un **diccionario de listas**: cada clave es el nombre de una columna y cada lista, sus valores.

```python
df = pd.DataFrame({
    "fruta": ["pera", "uva", "kiwi"],
    "kilos": [3, 5, 2],
})
#   fruta  kilos
# 0  pera      3
# 1   uva      5
# 2  kiwi      2
```

> ⚠️ Todas las listas deben tener **el mismo largo**; si no, pandas da error.""",
task="Crea un DataFrame con la columna `jugador` = `Messi, Ronaldo, Mbappé` y la columna `goles` = `30, 25, 28`, en ese orden. Guárdalo en `resultado`.",
starter="resultado = pd.DataFrame({\n    # 'columna': [valores],\n})",
solution="resultado = pd.DataFrame({'jugador': ['Messi', 'Ronaldo', 'Mbappé'], 'goles': [30, 25, 28]})",
hint="{'jugador': ['Messi', 'Ronaldo', 'Mbappé'], 'goles': [30, 25, 28]}",
sql="CREATE TABLE jugadores (jugador TEXT, goles INT);\nINSERT INTO jugadores VALUES ('Messi',30),('Ronaldo',25),('Mbappé',28);"),

dict(id="pd13", sec="Del Series al DataFrame", title="Conoce tus tablas", level=1,
theory="""A partir de aquí tienes cargadas las tablas de una tienda online: `clientes`, `productos`, `pedidos`, `empleados`, `ventas_diarias` y `sucio` (datos desordenados para limpiar). Puedes verlas cuando quieras con el botón **📋 Tablas**.

Lo primero con cualquier tabla es saber **cuánto mide**:
- `df.shape` devuelve una tupla `(filas, columnas)`.
- `len(df)` devuelve solo la cantidad de filas.

```python
productos.shape   # (10, 5) -> 10 filas y 5 columnas
```

> ⚠️ `shape` es un **atributo**, no un método: se escribe sin paréntesis.""",
task="Guarda en `resultado` la forma (`shape`) de la tabla `clientes`.",
starter="resultado = ",
solution="resultado = clientes.shape",
hint="clientes.shape (sin paréntesis)",
sql="SELECT COUNT(*) FROM clientes;  -- filas"),

dict(id="pd14", sec="Del Series al DataFrame", title="Un vistazo rápido", level=1,
theory="""Con tablas de miles o millones de filas no puedes mirarlo todo. Por eso existen:

- `df.head(n)`: las primeras *n* filas (5 si no indicas nada).
- `df.tail(n)`: las últimas *n* filas.
- `df.sample(n)`: *n* filas al azar.

```python
pedidos.head(3)
```

> 💼 **En el trabajo:** `head()` es lo primero que se ejecuta con cualquier archivo nuevo, para ver qué columnas trae y cómo lucen los datos.""",
task="Guarda en `resultado` las **3 primeras filas** de `productos`.",
starter="resultado = ",
solution="resultado = productos.head(3)",
hint="productos.head(3)",
sql="SELECT * FROM productos LIMIT 3;"),

dict(id="pd15", sec="Del Series al DataFrame", title="Inventario de columnas", level=1,
theory="""Dos atributos que usarás a diario:

- `df.columns`: los nombres de las columnas. Con `list(df.columns)` se convierten en una lista normal.
- `df.dtypes`: el **tipo de dato** de cada columna:
  - `int64`: enteros; `float64`: decimales;
  - `object` o `str`: texto;
  - `datetime64`: fechas; `bool`: verdadero/falso.

```python
list(productos.columns)
# ['producto_id', 'producto', 'categoria', 'precio', 'stock']
```

> 💡 `df.info()` muestra todo junto: columnas, tipos y cantidad de valores no nulos.""",
task="Guarda en `resultado` una **lista** con los nombres de las columnas de `pedidos`.",
starter="resultado = ",
solution="resultado = list(pedidos.columns)",
hint="list(pedidos.columns)",
sql="SELECT column_name FROM information_schema.columns WHERE table_name = 'pedidos';"),

dict(id="pd16", sec="Del Series al DataFrame", title="Resumen estadístico", level=1,
theory="""`df.describe()` calcula de golpe las estadísticas principales de **todas las columnas numéricas**:

- `count`: cuántos valores hay;
- `mean` y `std`: media y desviación estándar;
- `min` y `max`;
- `25%`, `50%`, `75%`: percentiles (el 50% es la mediana).

Es la forma más rápida de detectar cosas raras: un precio negativo, una edad de 300 años, un stock en cero…

> 💼 **En el trabajo:** `describe()` es parte del **EDA** (*Exploratory Data Analysis*), el análisis exploratorio que se hace antes de cualquier trabajo serio.""",
task="Guarda en `resultado` el resumen estadístico de `productos`.",
starter="resultado = ",
solution="resultado = productos.describe()",
hint="productos.describe()",
sql="SELECT COUNT(precio), AVG(precio), MIN(precio), MAX(precio) FROM productos;"),

dict(id="pd17", sec="Del Series al DataFrame", title="¿Cuántos de cada uno?", level=1,
theory="""`value_counts()` cuenta **cuántas veces aparece cada valor** de una columna, ordenado de mayor a menor. Es probablemente el método más usado en análisis exploratorio.

```python
pedidos["estado"].value_counts()
# entregado    15
# enviado       5
# ...
```

Variantes útiles:
- `value_counts(normalize=True)`: proporciones en lugar de conteos;
- `.nunique()`: cuántos valores **distintos** hay;
- `.unique()`: cuáles son.""",
task="Cuenta cuántos clientes hay de cada `pais` y guarda la Series en `resultado`.",
starter="resultado = ",
solution="resultado = clientes['pais'].value_counts()",
hint="clientes['pais'].value_counts()",
sql="SELECT pais, COUNT(*) FROM clientes GROUP BY pais ORDER BY 2 DESC;",
check={"ordered": False}),

# =========================================================== Leer y guardar
dict(id="pd18", sec="Leer y guardar datos", title="Leer un CSV", level=2,
theory="""El **CSV** (valores separados por comas) es el formato de datos más común del mundo. pandas lo lee con `pd.read_csv()`:

```python
df = pd.read_csv("ventas.csv")                 # archivo local
df = pd.read_csv("https://.../datos.csv")      # desde una URL
df = pd.read_csv("datos.csv", sep=";")         # separado por punto y coma
```

En **Google Colab** puedes subir un archivo desde el panel de la izquierda (📁) o leerlo directamente desde Google Drive.

Aquí vamos a leer un CSV que está guardado en un **texto**. Para que pandas lo trate como un archivo se usa `io.StringIO(texto)`.

> 💡 Otros lectores: `pd.read_excel()`, `pd.read_json()`, `pd.read_parquet()` y `pd.read_sql()` (este último lo verás en el módulo de DataFrames).""",
task="Lee el texto `csv` con `pd.read_csv` (envuelto en `io.StringIO`) y guarda el DataFrame en `resultado`.",
starter="import io\n\ncsv = '''ciudad,habitantes,pais\nMadrid,3300000,España\nLima,10000000,Perú\nBogotá,7900000,Colombia'''\n\nresultado = ",
solution="import io\n\ncsv = '''ciudad,habitantes,pais\nMadrid,3300000,España\nLima,10000000,Perú\nBogotá,7900000,Colombia'''\n\nresultado = pd.read_csv(io.StringIO(csv))",
hint="pd.read_csv(io.StringIO(csv))",
sql="COPY ciudades FROM 'ciudades.csv' CSV HEADER;  -- PostgreSQL"),

dict(id="pd19", sec="Leer y guardar datos", title="Exportar resultados", level=2,
theory="""Cuando terminas un análisis hay que **compartirlo**. Los métodos `to_...` guardan un DataFrame:

```python
df.to_csv("resultado.csv", index=False)    # index=False: no guarda el índice
df.to_excel("reporte.xlsx", index=False)
df.to_json("datos.json")
```

Si no indicas el archivo, `to_csv()` **devuelve el texto** del CSV, lo que viene bien para verlo o enviarlo.

> ⚠️ **Error común:** olvidar `index=False` y acabar con una columna extra `Unnamed: 0` al volver a leer el archivo.""",
task="Convierte `productos` a texto CSV **sin el índice** y guarda ese texto en `resultado`.",
starter="resultado = ",
solution="resultado = productos.to_csv(index=False)",
hint="productos.to_csv(index=False)",
sql="COPY productos TO 'productos.csv' CSV HEADER;  -- PostgreSQL"),
]
