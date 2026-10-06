# -*- coding: utf-8 -*-
"""Módulo 03 · NumPy: arrays, indexado, cálculo vectorizado y broadcasting."""

EXERCISES = [
# =========================================================== Crear arrays
dict(id="np01", sec="Crear arrays", title="Tu primer array", level=1,
theory="""**NumPy** (*Numerical Python*) es la librería de cálculo numérico de Python y el **motor que hay debajo de pandas**: cada columna de un DataFrame guarda sus datos en un array de NumPy.

Su estructura básica es el **array** (`ndarray`): una colección de valores **del mismo tipo**, guardados de forma compacta y muy rápidos de operar.

```python
import numpy as np    # "np" es el alias estándar

a = np.array([3, 7, 1])
a * 2          # array([ 6, 14,  2])  <- sin bucles
a.dtype        # dtype('int64')
```

**¿Por qué no usar una lista?** Porque `[3, 7, 1] * 2` en una lista **repite** la lista (`[3, 7, 1, 3, 7, 1]`), mientras que el array **multiplica cada número**. Además, NumPy es entre 10 y 100 veces más rápido.

> 💼 **En el trabajo:** Machine Learning, imágenes, audio y simulaciones funcionan sobre arrays de NumPy.""",
task="Crea un array de NumPy con los valores `5, 10, 15, 20` y guárdalo en `resultado`.",
starter="# numpy ya está importado como np\nresultado = ",
solution="resultado = np.array([5, 10, 15, 20])",
hint="np.array([5, 10, 15, 20])",
),

dict(id="np02", sec="Crear arrays", title="Rangos con arange y linspace", level=1,
theory="""Para no escribir los números a mano, NumPy tiene funciones que **generan secuencias**:

- `np.arange(inicio, fin, paso)`: como `range()`; el **fin no se incluye**.
- `np.linspace(inicio, fin, cantidad)`: *cantidad* números equiespaciados, con el **fin incluido**.
- `np.zeros(n)` / `np.ones(n)`: arrays de ceros o de unos.

```python
np.arange(0, 10, 2)      # [0 2 4 6 8]
np.linspace(0, 1, 5)     # [0.   0.25 0.5  0.75 1.  ]
np.zeros(3)              # [0. 0. 0.]
```

> 💡 `linspace` es muy útil para dibujar curvas: generas, por ejemplo, 100 puntos entre 0 y 10.""",
task="Crea con `np.arange` el array `0, 5, 10, ..., 45` (de 0 a 45, de 5 en 5). Guárdalo en `resultado`.",
starter="resultado = ",
solution="resultado = np.arange(0, 50, 5)",
hint="np.arange(0, 50, 5): el 50 no se incluye",
),

dict(id="np03", sec="Crear arrays", title="Dimensiones y forma", level=1,
theory="""Un array puede tener varias **dimensiones**:
- 1D: un vector, como `temperaturas`;
- 2D: una **matriz** con filas y columnas, como `notas`;
- 3D o más: por ejemplo una imagen a color (alto × ancho × 3 colores).

Atributos clave:
- `a.ndim`: cantidad de dimensiones;
- `a.shape`: tamaño de cada dimensión (`(filas, columnas)` en 2D);
- `a.size`: cantidad total de elementos;
- `a.dtype`: tipo de los datos.

En este módulo tienes cargados `temperaturas` (7 días), `notas` (5 alumnos × 3 exámenes) y `precios` (los precios de `productos`).""",
task="Guarda en `resultado` la **forma** (`shape`) de la matriz `notas`.",
starter="print(notas)\nresultado = ",
solution="resultado = notas.shape",
hint="notas.shape",
),

dict(id="np04", sec="Crear arrays", title="Cambiar de forma", level=2,
theory="""`reshape(filas, columnas)` reorganiza los mismos datos con otra forma. La cantidad total de elementos debe coincidir: 12 elementos pueden ser 3×4, 4×3, 2×6…

```python
np.arange(6).reshape(2, 3)
# [[0 1 2]
#  [3 4 5]]
```

Si pones `-1` en una dimensión, NumPy la **calcula por ti**: `reshape(3, -1)`.

> 💼 **En el trabajo:** scikit-learn exige que las variables de entrada sean 2D. `x.reshape(-1, 1)` convierte un vector en una columna, y lo verás muy a menudo.""",
task="Crea un array con los números del **0 al 11** y dale forma de **3 filas × 4 columnas**.",
starter="resultado = ",
solution="resultado = np.arange(12).reshape(3, 4)",
hint="np.arange(12).reshape(3, 4)",
),

# =========================================================== Indexar
dict(id="np05", sec="Indexar y recortar", title="Acceder a elementos", level=2,
theory="""En un array 2D se indica `[fila, columna]`, empezando en 0:

```python
notas[0, 0]     # primera nota del primer alumno
notas[1]        # toda la fila 1 (segundo alumno)
notas[:, 2]     # toda la columna 2 (tercer examen)
```

Los `:` significan **"todo"** en esa dimensión. Así, `notas[:, 2]` se lee *"todas las filas, columna 2"*.""",
task="Guarda en `resultado` las notas del **segundo examen** (columna 1) de todos los alumnos.",
starter="resultado = ",
solution="resultado = notas[:, 1]",
hint="notas[:, 1]",
),

dict(id="np06", sec="Indexar y recortar", title="Recortar submatrices", level=2,
theory="""Con **rebanadas** (*slicing*) `inicio:fin` puedes recortar trozos de un array. Como en Python, el `fin` no se incluye:

```python
notas[:2]          # primeras 2 filas
notas[1:4, 0:2]    # filas 1 a 3, columnas 0 y 1
notas[-2:]         # últimas 2 filas
```

> ⚠️ Un recorte es una **vista** de los mismos datos: si lo modificas, también cambia el original. Usa `.copy()` si quieres un array independiente.""",
task="Guarda en `resultado` las notas de los **3 primeros alumnos** en los **2 últimos exámenes**.",
starter="resultado = ",
solution="resultado = notas[:3, 1:]",
hint="notas[:3, 1:] o notas[:3, -2:]",
),

dict(id="np07", sec="Indexar y recortar", title="Filtrar con máscaras", level=2,
theory="""Igual que en pandas, una comparación genera un array de **True/False** que sirve para filtrar:

```python
a = np.array([4, 9, 2, 7])
a > 5          # [False  True False  True]
a[a > 5]       # [9 7]
```

Para combinar condiciones se usan `&` (y) y `|` (o), **con paréntesis**: `a[(a > 2) & (a < 8)]`.

> 💡 `(a > 5).sum()` cuenta cuántos valores cumplen la condición.""",
task="Guarda en `resultado` las temperaturas **mayores que 22** grados.",
starter="resultado = ",
solution="resultado = temperaturas[temperaturas > 22]",
hint="temperaturas[temperaturas > 22]",
),

# =========================================================== Vectorizado
dict(id="np08", sec="Cálculo vectorizado", title="Fórmulas sobre arrays", level=1,
theory="""Cualquier fórmula matemática se aplica **elemento a elemento** a todo el array, sin bucles:

```python
km = np.array([5, 10, 21])
millas = km * 0.621        # [ 3.1  6.2 13.0]
```

También funcionan las funciones matemáticas de NumPy: `np.sqrt`, `np.log`, `np.exp`, `np.round`, `np.abs`…

> 💼 **En el trabajo:** convertir unidades, normalizar datos o aplicar fórmulas financieras sobre millones de valores en milisegundos.""",
task="Convierte `temperaturas` de Celsius a **Fahrenheit** con la fórmula `F = C * 9/5 + 32`. Guarda el array.",
starter="resultado = ",
solution="resultado = temperaturas * 9 / 5 + 32",
hint="temperaturas * 9 / 5 + 32",
),

dict(id="np09", sec="Cálculo vectorizado", title="Agregar por filas o columnas", level=3,
theory="""Las funciones de resumen (`sum`, `mean`, `max`, `min`, `std`) aceptan el parámetro **`axis`**:

- sin `axis`: resumen de **todo** el array;
- `axis=0`: **baja por las filas**, es decir, un resultado **por columna**;
- `axis=1`: **recorre las columnas**, es decir, un resultado **por fila**.

```python
m = np.array([[1, 2],
              [3, 4]])
m.sum()          # 10
m.sum(axis=0)    # [4 6]   (por columna)
m.sum(axis=1)    # [3 7]   (por fila)
```

> 💡 Truco para recordarlo: el `axis` que indicas es la dimensión que **desaparece**.""",
task="Calcula el **promedio de cada alumno** (cada fila de `notas`). Guarda el array de 5 promedios.",
starter="resultado = ",
solution="resultado = notas.mean(axis=1)",
hint="notas.mean(axis=1)",
),

dict(id="np10", sec="Cálculo vectorizado", title="Broadcasting", level=3,
theory="""El **broadcasting** permite operar arrays de formas distintas: NumPy "estira" el más pequeño para que encaje con el grande.

```python
notas.shape        # (5, 3)
bonus = np.array([1, 0, 0.5])      # shape (3,)
notas + bonus      # suma el bonus correspondiente a CADA columna
```

El vector `bonus` se aplica a las 5 filas: +1 al primer examen, +0 al segundo y +0.5 al tercero.

Después, `np.minimum(array, 10)` limita los valores para que ninguno pase de 10 (`np.clip(array, 0, 10)` limita por arriba y por abajo).""",
task="Suma a `notas` el bonus `[1, 0, 0.5]` (uno por examen) y limita las notas a un **máximo de 10** con `np.minimum`. Guarda la matriz.",
starter="bonus = np.array([1, 0, 0.5])\nresultado = ",
solution="bonus = np.array([1, 0, 0.5])\nresultado = np.minimum(notas + bonus, 10)",
hint="np.minimum(notas + bonus, 10)",
),

dict(id="np11", sec="Cálculo vectorizado", title="Condicionales con np.where", level=2,
theory="""`np.where(condición, valor_si_true, valor_si_false)` es un **if vectorizado**: evalúa la condición para cada elemento y elige un valor u otro.

```python
edades = np.array([15, 30, 17])
np.where(edades >= 18, "adulto", "menor")
# ['menor' 'adulto' 'menor']
```

Se usa muchísimo para crear columnas en pandas:

```python
df["tipo"] = np.where(df["precio"] > 100, "caro", "barato")
```""",
task="Con el promedio de cada alumno (`promedios`), crea un array que diga **\"aprobado\"** si el promedio es **≥ 7** y **\"recupera\"** si no.",
starter="promedios = notas.mean(axis=1)\nresultado = ",
solution="promedios = notas.mean(axis=1)\nresultado = np.where(promedios >= 7, 'aprobado', 'recupera')",
hint="np.where(promedios >= 7, 'aprobado', 'recupera')",
),

# =========================================================== Práctica
dict(id="np12", sec="NumPy en la práctica", title="Números aleatorios reproducibles", level=2,
theory="""Para simular datos, mezclar filas o separar datos de entrenamiento se necesitan **números aleatorios**. La forma moderna es crear un **generador** con una **semilla** (*seed*):

```python
rng = np.random.default_rng(42)
rng.integers(1, 7, size=5)     # 5 tiradas de dado (el 7 no se incluye)
rng.normal(0, 1, size=3)       # 3 valores de una distribución normal
rng.choice(["a", "b"], size=4) # elecciones al azar
```

Con la **misma semilla** siempre salen **los mismos números**. Eso hace que tus experimentos sean **reproducibles**.

> 💼 **En el trabajo:** en Machine Learning siempre se fija la semilla (`random_state=42`) para que otra persona pueda obtener exactamente tus resultados.""",
task="Crea un generador con semilla **0** y simula **10 tiradas de un dado** (enteros del 1 al 6). Guarda el array.",
starter="rng = \nresultado = ",
solution="rng = np.random.default_rng(0)\nresultado = rng.integers(1, 7, size=10)",
hint="rng = np.random.default_rng(0); rng.integers(1, 7, size=10)",
),

dict(id="np13", sec="NumPy en la práctica", title="Estandarizar datos", level=3,
theory="""Estandarizar (calcular el **z-score**) transforma los datos para que tengan **media 0 y desviación estándar 1**:

```
z = (x - media) / desviación
```

Así ves cuántas desviaciones se aleja cada valor de la media: `z = 2` significa "muy por encima de lo normal".

```python
x = np.array([10, 20, 30])
(x - x.mean()) / x.std()      # [-1.22  0.    1.22]
```

> 💼 **En el trabajo:** muchos modelos de Machine Learning (KNN, regresión logística, redes neuronales) funcionan mucho mejor con los datos estandarizados. Lo verás de nuevo en el último módulo con `StandardScaler`.""",
task="Estandariza `temperaturas`: resta su media y divide por su desviación estándar (`.std()`). Guarda el array.",
starter="resultado = ",
solution="resultado = (temperaturas - temperaturas.mean()) / temperaturas.std()",
hint="(temperaturas - temperaturas.mean()) / temperaturas.std()",
),

dict(id="np14", sec="NumPy en la práctica", title="Percentiles", level=2,
theory="""Un **percentil** indica el valor por debajo del cual queda cierto porcentaje de los datos:

- percentil 50 = **mediana** (la mitad de los datos está por debajo);
- percentil 90 = el 90% de los datos está por debajo.

```python
np.percentile(datos, 50)          # mediana
np.percentile(datos, [25, 75])    # primer y tercer cuartil
```

A diferencia de la media, los percentiles **no se deforman** con valores extremos. Por eso se usan para medir tiempos de respuesta ("el p95 es de 300 ms") o para detectar outliers.

> 💡 Puedes sacar un array de pandas con `df["col"].to_numpy()`, como se hizo con `precios`.""",
task="Calcula el **percentil 75** de `precios` y guárdalo en `resultado`.",
starter="resultado = ",
solution="resultado = np.percentile(precios, 75)",
hint="np.percentile(precios, 75)",
),

dict(id="np15", sec="NumPy en la práctica", title="Álgebra de matrices", level=4,
theory="""El **producto matricial** (`@` o `np.dot`) es la base de la estadística y del Machine Learning: una regresión lineal predice con `X @ coeficientes`.

Para multiplicar `A @ B`, las columnas de A deben coincidir con las filas de B: `(5, 3) @ (3,)` da `(5,)`.

```python
ventas = np.array([[2, 1],
                   [0, 3]])          # 2 clientes x 2 productos (unidades)
precio = np.array([10, 4])          # precio de cada producto
ventas @ precio                      # [24 12]  -> gasto de cada cliente
```

> 💡 No lo confundas con `*`, que multiplica **elemento a elemento**.""",
task="Los exámenes pesan distinto: **30%, 30% y 40%**. Calcula la **nota final ponderada** de cada alumno con el producto matricial `notas @ pesos`.",
starter="pesos = np.array([0.3, 0.3, 0.4])\nresultado = ",
solution="pesos = np.array([0.3, 0.3, 0.4])\nresultado = notas @ pesos",
hint="notas @ pesos",
),
]
