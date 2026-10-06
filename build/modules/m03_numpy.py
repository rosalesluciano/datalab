# -*- coding: utf-8 -*-
"""Módulo 03 · NumPy: cálculo numérico vectorizado, desde el punto de vista práctico."""
from datasets import NUMPY_SETUP, SETUP
from framework import A, B, C, D, E, F, G, P, Q, ask, concept, field, module, project

S1, S2, S3, S4 = "¿Cuándo necesito NumPy?", "Arrays: forma, dimensiones y tipo", "Indexar, recortar y filtrar", "Cálculo vectorizado y broadcasting"
S5, S6 = "Estadística y ejes", "NumPy en la práctica (y su relación con pandas)"
SP = "Proyecto: estadísticas de una red de sensores"

CONCEPTS = [
concept("np-porque", "¿Por qué NumPy y no Python puro?", "arrays vectorizados · velocidad · base de pandas y ML",
    problem="Hacer cálculos numéricos sobre **muchos valores a la vez**, rápido y con código corto. NumPy es el motor numérico debajo de pandas, matplotlib y scikit-learn.",
    when="Tenés muchos números del mismo tipo (mediciones, matrices, imágenes) y querés operar sobre todos, o una librería te pide/devuelve arrays.",
    signals=["Loops que hacen la misma cuenta sobre cada número", "Datos en forma de matriz (filas × columnas numéricas)", "Un modelo o librería que devuelve `ndarray`"],
    can=["Operar arrays enteros sin loops: `a * 9/5 + 32`", "Trabajar con matrices de N dimensiones", "Estadística, álgebra lineal y aleatoriedad"],
    cant=["Tener columnas con nombre ni tipos mezclados (para eso: pandas)", "Tener elementos de distinto tipo sin convertir todo a un tipo común"],
    nomemo="Recordá cuándo conviene: **muchos números, mismas operaciones**. La sintaxis se parece mucho a pandas.",
    ai="«Tengo una lista de Python con 1 millón de temperaturas y las convierto con un for. ¿Cómo sería con NumPy y por qué es más rápido?»",
    verify="Compará el resultado vectorizado con el de un loop en un caso chico.",
    example="""import numpy as np
celsius = np.array([21.5, 23.0, 19.8])
celsius * 9 / 5 + 32       # todo el array a la vez
[1, 2] * 2                 # lista: [1, 2, 1, 2] (repite)
np.array([1, 2]) * 2       # array: [2, 4] (multiplica)""",
    check=("¿Qué da `np.array([1, 2, 3]) * 2`?", [
        ("`array([2, 4, 6])`", True, "La operación se aplica a cada elemento."),
        ("`[1, 2, 3, 1, 2, 3]`", False, "Eso pasa con una lista de Python."),
        ("Un error", False, "Es válido."),
    ])),

concept("np-array", "Arrays: shape, dimensiones y dtype", "np.array · arange · linspace · shape · ndim · dtype · reshape",
    problem="Crear arrays y entender su **forma** (cuántas filas/columnas/dimensiones) y su **tipo** (todos los elementos comparten uno).",
    when="Al crear datos, al leer el resultado de una operación y cuando aparece un error de forma.",
    signals=["Errores 'shapes … could not be broadcast'", "Un array de números que se comporta como texto", "'convertí a matriz de 3×4'"],
    can=["Crear: `np.array`, `np.arange`, `np.linspace`, `np.zeros`", "Inspeccionar: `.shape`, `.ndim`, `.dtype`", "Cambiar forma: `.reshape(3, 4)`", "Convertir tipo: `.astype(float)`"],
    cant=["Mezclar tipos: si hay un texto, **todo** el array pasa a texto", "Hacer reshape a una forma con distinta cantidad de elementos"],
    nomemo="shape = (filas, columnas) en 2D. Si un cálculo falla, lo primero es mirar shape y dtype.",
    ai="«Tengo un array con shape (5, 3). ¿Qué representa cada número y cómo lo interpreto si son 5 alumnos y 3 exámenes?»",
    verify="Imprimí `a.shape` y `a.dtype` después de crear o transformar.",
    example="""notas = np.array([[7, 8, 6], [9, 5, 8]])
notas.shape    # (2, 3): 2 filas, 3 columnas
notas.dtype    # int64
np.arange(12).reshape(3, 4)""",
    check=("¿Qué dtype tiene `np.array([1, 2, '3'])`?", [
        ("Texto (str/unicode): todo se convierte a texto", True, "Un array tiene un solo tipo."),
        ("int", False, "El '3' fuerza a texto."),
        ("Mixto", False, "Los arrays no son mixtos."),
    ])),

concept("np-index", "Indexar, recortar y filtrar", "a[i] · a[fila, col] · a[:, 1] · a[a > x]",
    problem="Extraer partes de un array: un elemento, una fila, una columna, un bloque o los elementos que cumplen una condición.",
    when="'la columna del segundo examen', 'los primeros 3 alumnos', 'las temperaturas mayores a 22'.",
    signals=["Se nombran filas/columnas por posición", "Una condición sobre los valores"],
    can=["Elemento: `a[1, 2]`", "Columna completa: `a[:, 1]`", "Bloque: `a[:3, 1:]`", "Filtrar con máscara: `a[a > 22]`", "Encontrar posiciones: `np.argwhere(cond)`"],
    cant=["Usar etiquetas o nombres (solo posiciones)"],
    nomemo="`[filas, columnas]` y `:` = 'todo'. Igual que listas, pero con una coma por dimensión.",
    ai="«En una matriz de notas (alumnos × exámenes), ¿cómo selecciono las notas del último examen de los alumnos 2 a 4?»",
    verify="Mirá el shape del recorte: ¿coincide con lo que pediste?",
    example="""notas[:, 1]        # columna 1 (segundo examen)
notas[:3, 1:]      # 3 primeras filas, desde la columna 1
temperaturas[temperaturas > 22]""",
    check=("En una matriz de alumnos × exámenes, ¿qué selecciona `notas[:, 0]`?", [
        ("La nota del primer examen de todos los alumnos", True, "Todas las filas, columna 0."),
        ("Todas las notas del primer alumno", False, "Eso es notas[0, :]."),
        ("Un solo número", False, "Es una columna completa."),
    ])),

concept("np-vector", "Operaciones vectorizadas", "+ - * / ** · np.sqrt · np.minimum · np.round",
    problem="Aplicar fórmulas a todos los elementos de una vez: conversiones, normalizaciones, impuestos.",
    when="Una fórmula se aplica igual a cada valor.",
    signals=["'convertí todos', 'aplicá la fórmula a cada…'", "Un for que solo hace una cuenta"],
    can=["Aritmética entre arrays y escalares", "Funciones universales: `np.sqrt`, `np.log`, `np.abs`, `np.round`", "Mínimos/máximos elemento a elemento: `np.minimum(a, 10)`"],
    cant=["Operar arrays de formas incompatibles"],
    nomemo="Si la escribirías igual para un número, escribila igual para el array.",
    ai="«Quiero limitar todas las notas a un máximo de 10 después de sumar un bonus. ¿Qué función de NumPy compara elemento a elemento?»",
    verify="Calculá a mano uno o dos elementos y compará.",
    example="""fahrenheit = temperaturas * 9 / 5 + 32
np.minimum(notas + 1, 10)    # tope en 10""",
    check=("`np.minimum(np.array([8, 11, 9]), 10)` da…", [
        ("`array([8, 10, 9])`", True, "Compara cada elemento con 10 y se queda con el menor."),
        ("`8`", False, "Eso sería el mínimo del array (a.min())."),
        ("`10`", False, "No."),
    ])),

concept("np-broadcast", "Broadcasting", "operar arrays de formas distintas compatibles",
    problem="Combinar arrays de distinta forma sin copiar datos: sumar un bonus por examen a toda la matriz, restar la media de cada columna.",
    when="Un array 'pequeño' (por columna o por fila) se aplica sobre uno grande.",
    signals=["'un valor distinto por columna'", "Error 'operands could not be broadcast together'"],
    can=["Matriz (5, 3) + vector (3,): se aplica a cada fila", "Matriz (5, 3) + columna (5, 1): se aplica a cada columna", "Agregar una dimensión: `v.reshape(5, 1)` o `v[:, None]`"],
    cant=["Combinar (5, 3) con (5,) directamente (las formas se alinean por la derecha)"],
    nomemo="Regla práctica: las formas se comparan desde la derecha; cada dimensión debe ser igual o 1.",
    ai="«Tengo una matriz de notas (5 alumnos × 3 exámenes) y un bonus por alumno de largo 5. ¿Por qué falla la suma y cómo lo arreglo?»",
    verify="Mirá los shapes de ambos operandos antes de operar.",
    example="""notas + np.array([1, 0, 0.5])        # (5,3) + (3,) → por examen
notas + bonus_alumno.reshape(5, 1)    # (5,3) + (5,1) → por alumno""",
    check=("¿Funciona `np.ones((5, 3)) + np.array([1, 2, 3])`?", [
        ("Sí: el vector (3,) se suma a cada una de las 5 filas", True, "Las formas son compatibles desde la derecha."),
        ("No: las formas son distintas", False, "Broadcasting lo permite."),
        ("Solo si se usa un for", False, "No hace falta."),
    ])),

concept("np-stats", "Estadística y ejes", "mean · std · percentile · sum · axis",
    problem="Resumir datos numéricos: promedios, dispersión, percentiles, por fila o por columna.",
    when="'promedio de cada alumno', 'percentil 75 de precios', 'desvío de las temperaturas'.",
    signals=["'de cada fila/columna'", "Medidas de posición o dispersión"],
    can=["Global: `a.mean()`, `a.std()`, `np.percentile(a, 75)`", "Por columna: `axis=0`; por fila: `axis=1`", "Estandarizar: `(a - a.mean()) / a.std()`"],
    cant=["Elegir la medida por vos (media vs mediana con outliers)"],
    nomemo="axis=0 → un resultado por columna; axis=1 → uno por fila. Igual que en pandas.",
    ai="«Con una matriz alumnos × exámenes, ¿qué axis uso para el promedio de cada alumno? Explicámelo con la forma del resultado.»",
    verify="El largo del resultado debe coincidir con la cantidad de filas o columnas.",
    example="""notas.mean(axis=1)       # promedio de cada alumno (fila)
notas.mean(axis=0)       # promedio de cada examen (columna)
np.percentile(precios, 75)""",
    check=("Matriz de 5 alumnos × 3 exámenes. ¿Qué shape tiene `notas.mean(axis=0)`?", [
        ("(3,): un promedio por examen", True, "axis=0 colapsa las filas."),
        ("(5,)", False, "Eso es axis=1."),
        ("Un escalar", False, "Eso es sin axis."),
    ])),

concept("np-where", "Condicionales vectorizados", "np.where · np.select",
    problem="Elegir un valor u otro según una condición, para todos los elementos a la vez.",
    when="'aprobado si ≥ 7, si no recupera', 'marcar como anomalía si…'.",
    signals=["Un if/else que se aplicaría a cada elemento"],
    can=["Dos opciones: `np.where(cond, si, no)`", "Varias: `np.select([c1, c2], [v1, v2], default)`"],
    cant=["Reemplazar lógica muy compleja sin perder legibilidad"],
    nomemo="np.where es el if/else de los arrays.",
    ai="«¿Cómo marco con 'alto' los precios mayores a 200 y 'normal' el resto, sin un for?»",
    verify="Contá cuántos 'alto' salieron y compará con `(cond).sum()`.",
    example="""np.where(promedios >= 7, "aprobado", "recupera")""",
    check=("¿Qué hace `np.where(a > 0, a, 0)`?", [
        ("Reemplaza los negativos (y ceros) por 0 y deja los positivos", True, "Elige elemento a elemento."),
        ("Devuelve las posiciones positivas", False, "Con un solo argumento devolvería posiciones."),
        ("Filtra el array", False, "No cambia el largo."),
    ])),

concept("np-random", "Aleatoriedad reproducible", "np.random.default_rng(semilla)",
    problem="Generar datos aleatorios (simulaciones, muestras, datos de prueba) que se puedan **reproducir**.",
    when="Simular escenarios, crear datos de prueba, dividir datos al azar (en ML).",
    signals=["'simulá', 'al azar', 'muestra aleatoria'", "Resultados que cambian en cada ejecución"],
    can=["Generador con semilla: `rng = np.random.default_rng(0)`", "Enteros, decimales, normales: `rng.integers`, `rng.uniform`, `rng.normal`", "Elegir al azar: `rng.choice`"],
    cant=["Reproducir resultados si no fijás la semilla"],
    nomemo="Siempre con semilla si querés que otra persona (o vos mañana) obtenga lo mismo.",
    ai="«Quiero simular 1000 tiradas de dos dados y que el resultado sea reproducible. ¿Cómo uso default_rng?»",
    verify="Ejecutá dos veces: con la misma semilla debe dar lo mismo.",
    example="""rng = np.random.default_rng(42)
rng.integers(1, 7, size=10)      # 10 tiradas de dado""",
    check=("¿Para qué sirve fijar una semilla?", [
        ("Para que los números 'aleatorios' sean reproducibles", True, "Misma semilla → misma secuencia."),
        ("Para que sean más aleatorios", False, "No."),
        ("Para que sean enteros", False, "No."),
    ])),

concept("np-pandas", "NumPy y pandas", "to_numpy · Series sobre arrays · np.funciones sobre columnas",
    problem="Entender que cada columna de pandas guarda sus datos en un array de NumPy, y pasar de uno a otro cuando hace falta.",
    when="Una librería pide arrays (scikit-learn, cálculos matriciales) o querés usar una función de NumPy sobre columnas.",
    signals=["Un modelo devuelve un ndarray", "Necesitás `np.corrcoef`, `np.percentile`… sobre una columna"],
    can=["Columna → array: `df['precio'].to_numpy()`", "Funciones de NumPy directo sobre Series: `np.log(df['precio'])`", "Array → Series/DataFrame: `pd.Series(arr, index=...)`"],
    cant=["Conservar nombres de columna e índice al pasar a array"],
    nomemo="pandas = NumPy + etiquetas. Cuando no necesitás etiquetas, el array alcanza.",
    ai="«scikit-learn me devolvió un ndarray de predicciones. ¿Cómo lo agrego como columna a mi DataFrame y qué tengo que cuidar del orden?»",
    verify="Largo y orden del array deben coincidir con las filas del DataFrame.",
    example="""precios = productos["precio"].to_numpy()
np.corrcoef(df["visitas"], df["ventas"])[0, 1]""",
    check=("¿Qué se pierde al hacer `df['precio'].to_numpy()`?", [
        ("El índice y el nombre de la columna", True, "Queda solo el array de valores."),
        ("Los valores", False, "Se conservan."),
        ("Los decimales", False, "No."),
    ])),
]

EXERCISES = [
# ======================================================================== S1
A("np-a01", S1, "¿Cuándo NumPy?", 1, ["np-porque"],
  "Tenés **1 millón de lecturas** de temperatura en °C y querés convertirlas todas a °F. ¿Qué enfoque conviene?",
  [("Un array de NumPy y la fórmula aplicada al array completo", True, "Vectorizado: rápido y en una línea."),
   ("Un for sobre una lista de Python", False, "Funciona pero es mucho más lento."),
   ("Un diccionario", False, "No aporta nada para una fórmula."),
   ("Matplotlib", False, "Es para graficar.")]),

B("np-b01", S1, "Listas vs arrays", 2, ["np-porque"],
  "Un compañero dice: *'¿Para qué NumPy si puedo usar listas?'*. **Explicale dos diferencias importantes con un ejemplo de datos**, y cuándo seguiría usando listas.",
  model="1) **Operaciones**: con un array, `precios * 1.21` multiplica cada elemento; con una lista, `* 2` **repite** la lista y `* 1.21` da error. 2) **Velocidad y memoria**: los arrays guardan números de un único tipo en bloque y operan en código compilado, así que con millones de datos son mucho más rápidos. Además traen estadística, álgebra lineal y son la base de pandas y scikit-learn. Seguiría usando listas para colecciones chicas o de tipos mezclados (nombres, registros) o cuando necesito agregar elementos uno a uno.",
  checklist=["Mencioné que las operaciones son elemento a elemento en arrays", "Mencioné que en listas * repite (o falla)", "Mencioné velocidad/memoria", "Dije cuándo siguen siendo útiles las listas"],
  hints=["¿Qué pasa con `[10, 20] * 2`?", "¿Y con `np.array([10, 20]) * 2`?", "¿Qué tipo de datos puede tener una lista que un array no?"]),

E("np-e01", S1, "Duplicar precios", 1, ["np-porque", "np-vector"],
  "Querías duplicar cada precio, pero el resultado tiene el doble de elementos. Corregilo usando NumPy.",
  "precios_lista = [10, 20, 30]\nresultado = precios_lista * 2",
  "precios_lista = [10, 20, 30]\nresultado = np.array(precios_lista) * 2",
  detect=("¿Qué pasó?", [
      ("Con una lista, `* 2` repite la lista en lugar de multiplicar cada valor", True, "[10, 20, 30, 10, 20, 30]."),
      ("Falta redondear", False, "No."),
      ("Hay que usar `+`", False, "Sumar listas también concatena."),
  ]),
  why="Para una lista de Python, `* 2` significa 'repetir la lista dos veces'. Para multiplicar cada elemento hay que convertirla en array (`np.array(...)`), donde las operaciones son elemento a elemento.",
  hints=["Mirá el largo del resultado.", "¿Qué significa `*` para una lista?", "Convertí la lista en un array antes de multiplicar."],
  pseudo="resultado ← array(precios_lista) × 2"),

# ======================================================================== S2
P("np01", S2, ["np-array"],
  ["Tenés una lista de valores y querés un array.", "Hay una función que convierte listas en arrays.", "np.array([...])"],
  "`np.array` convierte una lista de Python en un array de NumPy (todos del mismo tipo).",
  "resultado ← array con [5, 10, 15, 20]",
  problem="Creá un array de NumPy con los valores `5, 10, 15, 20` y guardalo en `resultado`.", level=1),

P("np02", S2, ["np-array"],
  ["Es una secuencia regular: de 0 a 45 de 5 en 5.", "Existe una función que genera rangos (como range pero devuelve un array).", "np.arange(inicio, fin_excluido, paso)."],
  "`np.arange(inicio, fin, paso)` genera la secuencia; el fin no se incluye, por eso se usa 50.",
  "resultado ← secuencia de 0 a 45 de 5 en 5 (fin excluido: 50)",
  problem="Generá el array `0, 5, 10, …, 45` sin escribirlo a mano. Guardalo en `resultado`."),

P("np03", S2, ["np-array"],
  ["Querés saber cuántas filas y columnas tiene la matriz.", "Es un atributo del array.", "Mismo nombre que en pandas."],
  "`shape` devuelve la forma: (5, 3) = 5 alumnos (filas) × 3 exámenes (columnas).",
  "resultado ← notas.shape",
  problem="¿Qué forma tiene la matriz `notas` (cuántos alumnos y cuántos exámenes)? Guardala en `resultado`.", level=1),

P("np04", S2, ["np-array"],
  ["Son 12 números en 3 filas de 4.", "Primero generá los 12 números, después cambiales la forma.", "arange(12) + reshape(filas, columnas)."],
  "Se genera un array de 12 elementos y `reshape(3, 4)` lo reorganiza en 3 filas × 4 columnas (12 = 3 × 4).",
  "resultado ← arange(12) reorganizado en 3 × 4",
  problem="Creá una matriz de **3 filas × 4 columnas** con los números del **0 al 11**."),

A("np-a02", S2, "Un array con un texto colado", 2, ["np-array"],
  "Creás `np.array([21.5, 23.0, 'n/d', 19.8])`. ¿Qué pasa?",
  [("Todo el array se vuelve texto, y `.mean()` va a fallar", True, "Un array tiene un solo dtype."),
   ("Queda un array numérico con un NaN", False, "NumPy no convierte 'n/d' en NaN automáticamente."),
   ("Da error al crearlo", False, "Se crea, pero como texto."),
   ("Se ignora el texto", False, "No.")]),

D("np-d01", S2, "Lecturas que llegaron como texto", 2, ["np-array"],
  "Las lecturas de un sensor llegaron como array de **texto**. Calculá su **promedio** y guardalo en `resultado`.",
  "lecturas_txt = np.array(['21.5', '23.0', '19.8', '25.1'])\nprint(lecturas_txt.dtype)\n\nresultado = ",
  "lecturas_txt = np.array(['21.5', '23.0', '19.8', '25.1'])\nprint(lecturas_txt.dtype)\n\nresultado = lecturas_txt.astype(float).mean()",
  ["Mirá el dtype que imprime: ¿se puede promediar texto?", "Primero hay que cambiar el tipo del array.", "astype(float) y después mean()."],
  "El array es de texto (dtype '<U4'); hay que convertirlo con `astype(float)` antes de calcular el promedio.",
  "numérico ← lecturas_txt convertido a float\nresultado ← promedio de numérico"),

# ======================================================================== S3
P("np05", S3, ["np-index"],
  ["Querés una columna completa (un examen para todos los alumnos).", "En 2D se indexa `[filas, columnas]`.", "`:` significa 'todas las filas'; el segundo examen es la columna 1."],
  "`notas[:, 1]` toma todas las filas (`:`) de la columna 1 (segundo examen).",
  "resultado ← notas[todas las filas, columna 1]",
  problem="Guardá en `resultado` las notas del **segundo examen** de todos los alumnos."),

P("np06", S3, ["np-index"],
  ["Es un bloque: algunas filas y algunas columnas.", "Primeros 3 alumnos = filas 0 a 2; últimos 2 exámenes = columnas 1 y 2.", "Slicing en cada dimensión: `[:3, 1:]`."],
  "Se recorta en ambas dimensiones: filas hasta la 3 (excluida) y columnas desde la 1.",
  "resultado ← notas[filas 0-2, columnas 1-2]",
  problem="Guardá las notas de los **3 primeros alumnos** en los **2 últimos exámenes**."),

P("np07", S3, ["np-index"],
  ["Primero preguntá (máscara), después filtrá.", "`temperaturas > 22` da True/False por elemento.", "Esa máscara entre corchetes se queda con los True."],
  "Igual que en pandas: la máscara booleana entre corchetes devuelve solo los elementos que cumplen.",
  "resultado ← temperaturas[temperaturas > 22]",
  problem="¿Qué días hizo **más de 22 grados**? Guardá esas temperaturas en `resultado`."),

# ======================================================================== S4
P("np08", S4, ["np-vector"],
  ["La fórmula es la misma para cada temperatura.", "Con arrays no hace falta un for.", "Escribí la fórmula usando el array como si fuera un número."],
  "La fórmula se aplica a todo el array a la vez (operación vectorizada).",
  "resultado ← temperaturas × 9/5 + 32",
  problem="Convertí `temperaturas` de Celsius a **Fahrenheit** (`F = C × 9/5 + 32`)."),

P("np10", S4, ["np-broadcast", "np-vector"],
  ["El bonus es uno por examen (3 valores) y la matriz es 5 × 3.", "Por broadcasting, un vector de 3 se suma a cada fila.", "Después, np.minimum(..., 10) pone el tope."],
  "El vector de bonus (3,) se suma a cada fila de la matriz (5, 3) por broadcasting; `np.minimum` limita cada nota a 10.",
  "bonus ← [1, 0, 0.5]\nresultado ← mínimo(notas + bonus, 10)",
  problem="Sumá a `notas` un bonus por examen `[1, 0, 0.5]` y limitá las notas a un **máximo de 10**."),

E("np-e02", S4, "El bonus por alumno que no encaja", 3, ["np-broadcast"],
  "Ahora el bonus es **por alumno** (5 valores, uno por fila). La suma falla. Corregila para que cada alumno reciba su bonus en todos sus exámenes (con tope en 10).",
  "bonus_alumno = np.array([1, 0, 0.5, 0, 1])\nresultado = np.minimum(notas + bonus_alumno, 10)",
  "bonus_alumno = np.array([1, 0, 0.5, 0, 1])\nresultado = np.minimum(notas + bonus_alumno.reshape(5, 1), 10)",
  detect=("¿Por qué falla?", [
      ("Las formas (5, 3) y (5,) no son compatibles: NumPy alinea desde la derecha (3 vs 5)", True, "Hay que convertir el bonus en columna (5, 1)."),
      ("No se pueden sumar decimales a enteros", False, "Sí se puede."),
      ("np.minimum no acepta matrices", False, "Acepta."),
  ]),
  why="Broadcasting compara las formas **desde la derecha**: (5, 3) contra (5,) → compara 3 con 5 y falla. Convirtiendo el bonus en columna `(5, 1)`, la comparación es 3 vs 1 (ok) y 5 vs 5 (ok): cada alumno suma su bonus en sus 3 exámenes.",
  hints=["Leé el error: ¿qué shapes menciona?", "¿Contra qué dimensión de la matriz se alinea un vector de largo 5?", "Probá darle al bonus la forma (5, 1)."],
  pseudo="resultado ← mínimo(notas + bonus como columna (5,1), 10)"),

P("np11", S4, ["np-where", "np-stats"],
  ["Primero necesitás el promedio de cada alumno.", "Después, una decisión por alumno: 'aprobado' o 'recupera'.", "np.where(condición, valor_si, valor_no)."],
  "Se calcula el promedio por fila y `np.where` elige la etiqueta para cada alumno según la condición.",
  "promedios ← notas.mean(axis=1)\nresultado ← where(promedios ≥ 7, 'aprobado', 'recupera')",
  problem="Con el promedio de cada alumno, armá un array que diga **\"aprobado\"** si el promedio es **≥ 7** y **\"recupera\"** si no."),

F("np-f01", S4, "La IA normaliza precios", 3, ["np-vector", "np-stats"],
  "Pediste a una IA 'llevar los precios a una escala de 0 a 1' y te dio este código (normalización min-max).",
  prompt="Tengo un array de precios y quiero escalarlos entre 0 y 1 (el más barato 0, el más caro 1). Mostrame el código y explicá la fórmula y sus casos borde.",
  ai_code="resultado = (precios - precios.min()) / (precios.max() - precios.min())",
  questions=[
      ask("¿Qué valor queda para el producto más caro?", [("1", True, "(max - min) / (max - min) = 1."), ("0", False, "0 es el más barato."), ("Su precio original", False, "No.")]),
      ask("¿Qué forma tiene el resultado?", [("La misma que precios (un valor por producto)", True, "Es una operación elemento a elemento."), ("Un solo número", False, "No."), ("(2,)", False, "No.")]),
      ask("¿Qué pasaría si todos los precios fueran iguales?", [("División por cero: todos los valores quedarían NaN", True, "max - min = 0."), ("Todos quedarían en 1", False, "No."), ("Funciona normal", False, "El denominador es 0.")]),
      ask("¿Por qué alguien querría normalizar así antes de un modelo de ML?", model="Para que variables en escalas muy distintas (precio en miles, cantidad en unidades) sean comparables y ninguna domine solo por su magnitud, especialmente en modelos basados en distancias (KNN) o en descenso por gradiente."),
  ],
  hints=["Ejecutalo y mirá el mínimo y máximo del resultado.", "Probá con un array de valores iguales.", "Pensá en qué modelos importa la escala."],
  explain="Se resta el mínimo (el más barato queda en 0) y se divide por el rango (el más caro queda en 1). Caso borde: rango 0.",
  solution="resultado = (precios - precios.min()) / (precios.max() - precios.min())"),

# ======================================================================== S5
A("np-a03", S5, "Promedio de cada alumno", 2, ["np-stats"],
  "Matriz `notas` de 5 alumnos (filas) × 3 exámenes (columnas). Querés **el promedio de cada alumno**. ¿Qué escribís?",
  [("`notas.mean(axis=1)`", True, "Un valor por fila."), ("`notas.mean(axis=0)`", False, "Un valor por examen."), ("`notas.mean()`", False, "Un solo número global."), ("`np.mean(notas[0])`", False, "Solo el primer alumno.")]),

P("np09", S5, ["np-stats"],
  ["Querés un valor por alumno (por fila).", "mean acepta el parámetro axis.", "axis=1 colapsa las columnas."],
  "`mean(axis=1)` promedia a lo largo de las columnas: un promedio por fila (alumno).",
  "resultado ← promedio de cada fila de notas",
  problem="Calculá el **promedio de cada alumno** (cada fila de `notas`). Guardá el array de 5 promedios."),

G("np-g01", S5, "Transferencia: el examen más fácil", 3, ["np-stats"], "np09",
  "Antes resumiste **por alumno** (filas). Ahora resumís **por examen** (columnas) para ver cuál fue el más fácil.",
  "Calculá el **promedio de cada examen** y guardá en `resultado` el **número de columna** (0, 1 o 2) del examen con el promedio más alto.",
  "resultado = ",
  "promedios_examen = notas.mean(axis=0)\nresultado = promedios_examen.argmax()",
  ["¿Qué eje da un valor por columna?", "Tenés 3 promedios; querés la **posición** del mayor, no su valor.", "Existe un método que devuelve la posición del máximo: argmax."],
  "Con axis=0 se obtiene un promedio por examen; `argmax()` devuelve la posición del mayor (el examen más fácil).",
  "promedios ← notas.mean(axis=0)\nresultado ← posición del máximo de promedios"),

P("np13", S5, ["np-stats", "np-vector"],
  ["Estandarizar = centrar en 0 y medir en desvíos.", "Necesitás la media y el desvío estándar del array.", "(x − media) / desvío, aplicado a todo el array."],
  "Se resta la media (centrar) y se divide por el desvío estándar (escalar). Cada valor queda expresado en 'cuántos desvíos se aleja de la media'.",
  "resultado ← (temperaturas − media) / desvío",
  problem="Estandarizá `temperaturas`: restale su media y dividí por su desvío estándar (`.std()`)."),

P("np14", S5, ["np-stats"],
  ["El percentil 75 es el valor que deja por debajo al 75% de los datos.", "NumPy tiene una función de percentiles.", "np.percentile(datos, 75)."],
  "`np.percentile` calcula el valor por debajo del cual queda el 75% de los precios.",
  "resultado ← percentil 75 de precios",
  problem="¿Qué precio deja por debajo al 75% de los productos? Calculá el **percentil 75** de `precios`."),

C("np-c01", S5, "Plan: detectar temperaturas anómalas", 3, ["np-stats", "np-index"],
  "Querés detectar qué temperaturas de `temperaturas` son **anómalas**: las que se alejan más de 1.5 desvíos estándar de la media. Diseñá el plan.",
  [field("Medidas que necesito", "La media y el desvío estándar del array.", ["Media y desvío estándar", "Solo el máximo", "La suma", "El percentil 10"], 0),
   field("Transformación", "Calcular z = (t − media) / desvío para cada temperatura.", ["Calcular z = (t − media) / desvío", "Ordenar las temperaturas", "Redondear"], 0),
   field("Condición de anomalía", "|z| > 1.5 (vale tanto para muy alto como para muy bajo).", ["|z| > 1.5", "z > 1.5", "t > 1.5"], 0),
   field("Herramienta para seleccionar", "Una máscara booleana: temperaturas[np.abs(z) > 1.5]."),
   field("Cómo verifico", "Miro los z de cada valor y confirmo que los seleccionados son los únicos con |z| > 1.5."),
  ],
  explain="El plan combina estadística (media, desvío, z-score), una operación vectorizada y filtrado con máscara. El valor absoluto permite detectar extremos en ambas direcciones.",
  hints=["¿Qué significa 'alejarse 1.5 desvíos'?", "¿Una temperatura muy baja también es anómala?", "¿Cómo filtrás un array con una condición?"],
  pseudo="z ← (t − media) / desvío\nresultado ← t donde |z| > 1.5"),

D("np-d02", S5, "Implementar: temperaturas anómalas", 3, ["np-stats", "np-index", "np-vector"],
  "Implementá el plan: guardá en `resultado` las temperaturas de `temperaturas` cuyo z-score en valor absoluto sea **mayor a 1.5**.",
  "resultado = ",
  "z = (temperaturas - temperaturas.mean()) / temperaturas.std()\nresultado = temperaturas[np.abs(z) > 1.5]",
  ["Seguí tu plan paso a paso.", "Calculá z para todo el array en una línea.", "np.abs(z) > 1.5 como máscara."],
  "Se calcula el z-score vectorizado y se filtra con la máscara |z| > 1.5.",
  "z ← (t − media) / desvío\nresultado ← t[|z| > 1.5]",
  verify="Imprimí z: el 27.3 tiene z ≈ 1.75, el único por encima de 1.5 en valor absoluto."),

# ======================================================================== S6
P("np12", S6, ["np-random"],
  ["Tiene que ser reproducible: ¿qué necesitás fijar?", "Creá un generador con semilla 0.", "rng.integers(1, 7, size=10): el 7 no se incluye."],
  "Con un generador con semilla fija, la secuencia 'aleatoria' es siempre la misma. `integers(1, 7)` da enteros del 1 al 6.",
  "rng ← generador con semilla 0\nresultado ← 10 enteros entre 1 y 6",
  problem="Simulá **10 tiradas de un dado** (enteros del 1 al 6) de forma **reproducible**, con un generador de semilla **0**."),

P("np15", S6, ["np-vector", "np-stats"],
  ["Cada alumno tiene 3 notas y cada examen un peso: es un promedio ponderado.", "Multiplicar cada nota por su peso y sumar por fila…", "…es exactamente un producto matricial: notas @ pesos."],
  "El producto matricial `notas @ pesos` multiplica cada fila por el vector de pesos y suma: el promedio ponderado de cada alumno.",
  "pesos ← [0.3, 0.3, 0.4]\nresultado ← notas @ pesos",
  problem="Los exámenes pesan distinto: **30%, 30% y 40%**. Calculá la **nota final ponderada** de cada alumno."),

A("np-a04", S6, "De pandas a NumPy", 1, ["np-pandas"],
  "Una función de cálculo matricial te pide un array de NumPy, y tenés la columna `precio` de un DataFrame. ¿Qué hacés?",
  [("`df['precio'].to_numpy()`", True, "Devuelve los valores como ndarray."),
   ("`list(df)`", False, "Devuelve los nombres de columnas."),
   ("`df.shape`", False, "Es el tamaño."),
   ("No se puede", False, "Sí se puede.")]),

D("np-d03", S6, "¿Visitas y ventas se mueven juntas?", 3, ["np-pandas", "np-stats"],
  "Usando NumPy sobre las columnas de `ventas_diarias`, calculá el **coeficiente de correlación** entre `visitas` y `ventas` (un número entre -1 y 1). Guardalo en `resultado`.",
  "resultado = ",
  "resultado = np.corrcoef(ventas_diarias['visitas'], ventas_diarias['ventas'])[0, 1]",
  ["La correlación mide si dos variables crecen juntas.", "NumPy tiene una función que devuelve la matriz de correlación.", "np.corrcoef(a, b) devuelve una matriz 2×2; el valor que buscás está fuera de la diagonal: [0, 1]."],
  "`np.corrcoef` acepta las columnas de pandas directamente y devuelve la matriz de correlación 2×2; el elemento [0, 1] es la correlación entre ambas variables.",
  "matriz ← corrcoef(visitas, ventas)\nresultado ← matriz[0, 1]"),

# ======================================================================== Proyecto
C("np-p1", SP, "Fase 1 · Plan del análisis de sensores", 3, ["np-stats", "np-index", "np-array"],
  "**Contexto:** `sensores` es una matriz de **7 días (filas) × 4 sensores (columnas)** con temperaturas en °C. Te piden: el promedio de cada sensor, detectar lecturas anómalas y reportar qué sensor falló y cuándo. Diseñá el plan.",
  [field("¿Qué forma tiene la matriz y qué es cada eje?", "(7, 4): filas = días, columnas = sensores.", ["(7, 4): filas = días, columnas = sensores", "(4, 7): filas = sensores", "Es una lista"], 0),
   field("Promedio de cada sensor: ¿qué eje?", "axis=0 (un valor por columna).", ["axis=0", "axis=1", "Sin axis"], 0),
   field("Regla de anomalía", "Lecturas mayores a media global + 3 desvíos (o |z| > 3)."),
   field("Cómo obtengo día y sensor de cada anomalía", "np.argwhere(condición) devuelve las posiciones (fila, columna)."),
   field("Riesgo a tener en cuenta", "La propia anomalía infla la media y el desvío del sensor afectado: conviene mirar también la mediana."),
  ],
  explain="Entender qué representa cada eje es la mitad del trabajo: define el axis de cada resumen y cómo interpretar las posiciones de las anomalías.",
  hints=["Imprimí sensores.shape.", "¿Querés un promedio por fila o por columna?", "¿Qué función devuelve posiciones donde se cumple una condición?"],
  pseudo="prom_sensor ← media por columna\nlímite ← media global + 3 × desvío global\nanomalías ← posiciones donde sensores > límite"),

D("np-p2", SP, "Fase 2 · Promedio por sensor", 3, ["np-stats"],
  "Calculá la **temperatura promedio de cada sensor**, redondeada a 2 decimales. Guardá el array (4 valores) en `resultado`.",
  "print(sensores)\n\nresultado = ",
  "resultado = np.round(sensores.mean(axis=0), 2)",
  ["Un valor por sensor: ¿por fila o por columna?", "Los sensores son las columnas.", "mean(axis=0) y después np.round(..., 2)."],
  "Con axis=0 se colapsan los días y queda un promedio por sensor. El sensor 1 sale más alto por la lectura de 41 °C.",
  "resultado ← redondear(media por columna, 2)"),

D("np-p3", SP, "Fase 3 · Encontrar la falla", 4, ["np-index", "np-stats"],
  "Encontrá las posiciones `(día, sensor)` de las lecturas **mayores a la media global + 3 desvíos estándar** (globales). Guardá el resultado de `np.argwhere` en `resultado`.",
  "resultado = ",
  "limite = sensores.mean() + 3 * sensores.std()\nresultado = np.argwhere(sensores > limite)",
  ["Primero calculá el límite con estadísticas de toda la matriz.", "La condición `sensores > limite` es una matriz de True/False.", "np.argwhere(condición) devuelve una fila [día, sensor] por cada True."],
  "Se calcula un umbral global y `np.argwhere` devuelve las coordenadas de los valores que lo superan: día 2, sensor 1.",
  "límite ← media + 3 × desvío\nresultado ← posiciones donde sensores > límite"),

E("np-p4", SP, "Fase 4 · El eje equivocado", 3, ["np-stats"],
  "Un compañero calculó el promedio por sensor, pero obtiene **7 valores** en lugar de 4. Corregilo.",
  "resultado = np.round(sensores.mean(axis=1), 2)",
  "resultado = np.round(sensores.mean(axis=0), 2)",
  detect=("¿Qué está mal?", [
      ("axis=1 promedia cada fila (cada día), no cada columna (sensor)", True, "Por eso salen 7 valores."),
      ("np.round cambia la cantidad de valores", False, "No."),
      ("La matriz tiene 7 sensores", False, "Tiene 4 sensores (columnas)."),
  ]),
  why="axis=1 colapsa las columnas y deja un valor por **fila** (día): 7 valores. Para un valor por **sensor** (columna) hay que colapsar las filas: axis=0. Verificar el largo del resultado detecta este error al instante.",
  hints=["¿Cuántos sensores hay y cuántos valores salen?", "¿Qué representa cada fila?", "¿Qué axis deja un valor por columna?"],
  pseudo="resultado ← redondear(media con axis=0, 2)"),

B("np-p5", SP, "Fase 5 · Reporte de la red de sensores", 3, ["np-stats", "np-index"],
  "Escribí un reporte breve (4-6 líneas): **qué sensor falló y cuándo, cómo lo detectaste, cómo afecta la falla al promedio de ese sensor y qué recomendarías.**",
  model="El sensor 1 registró 41 °C el día 2 (índices desde 0), muy por encima del resto (≈ 22 °C). Lo detecté con un umbral de media global + 3 desvíos y np.argwhere, que devolvió la posición [2, 1]. Esa lectura infla el promedio del sensor 1 (≈ 24.4 °C contra ≈ 22 °C del resto); sin ella, su promedio sería similar a los demás. Recomendaría revisar el sensor, excluir o marcar esa lectura en los análisis y usar la mediana como medida más robusta.",
  checklist=["Identifiqué el sensor y el día de la falla", "Expliqué el método de detección", "Expliqué cómo la falla distorsiona el promedio", "Hice una recomendación (revisar, excluir, mediana)"],
  hints=["Mirá el resultado de la fase 3.", "Compará el promedio del sensor 1 con los demás.", "¿Qué medida no se ve afectada por un valor extremo?"]),
]

QUIZ = [
Q("q-np-01", ["np-porque"], "Necesitás aplicar una fórmula matemática a 5 millones de mediciones numéricas.",
  [("Array de NumPy con operaciones vectorizadas", True, "Rápido y conciso."), ("Lista y for", False, "Lento."), ("Diccionario", False, "No."), ("Un set", False, "No.")]),
Q("q-np-02", ["np-broadcast"], "Querés restar a cada columna de una matriz la media de esa columna.",
  [("matriz - matriz.mean(axis=0) (broadcasting)", True, "(n, m) - (m,) es compatible."), ("Un for por columna", False, "Innecesario."), ("reshape", False, "No alcanza solo."), ("np.random", False, "No.")]),
Q("q-np-03", ["np-stats"], "Querés el desvío estándar de cada sensor en una matriz días × sensores.",
  [("std(axis=0)", True, "Un valor por columna."), ("std(axis=1)", False, "Por día."), ("std()", False, "Global."), ("argmax", False, "No.")]),
Q("q-np-04", ["np-where"], "Querés reemplazar los valores negativos de un array por 0 sin un loop.",
  [("np.where(a < 0, 0, a)", True, "If/else vectorizado."), ("a.sort()", False, "No."), ("a.reshape", False, "No."), ("a.mean()", False, "No.")]),
Q("q-np-05", ["np-random"], "Necesitás generar datos simulados que tu compañero pueda reproducir exactamente.",
  [("default_rng con una semilla fija", True, "Reproducible."), ("random sin semilla", False, "Cambia en cada ejecución."), ("Escribirlos a mano", False, "No escala."), ("np.zeros", False, "No es aleatorio.")]),
Q("q-np-06", ["np-index"], "Querés las coordenadas (fila, columna) de los valores mayores a 100 en una matriz.",
  [("np.argwhere(m > 100)", True, "Devuelve posiciones."), ("m[m > 100]", False, "Devuelve los valores, no las posiciones."), ("m.max()", False, "Solo el máximo."), ("m.shape", False, "No.")]),
Q("q-np-07", ["np-array"], "Una operación falla con 'operands could not be broadcast together with shapes (5,3) (5,)'.",
  [("Revisar shapes y dar forma (5,1) al vector", True, "Se alinean por la derecha."), ("Reinstalar NumPy", False, "No."), ("Usar listas", False, "No."), ("Convertir a texto", False, "No.")]),
Q("q-np-08", ["np-pandas"], "Un modelo de scikit-learn devolvió predicciones como ndarray y querés agregarlas al DataFrame.",
  [("Asignarlas como columna (mismo largo y orden)", True, "df['pred'] = arr."), ("Convertirlas en texto", False, "No."), ("Hacer merge", False, "No hay clave."), ("Imposible", False, "Se puede.")]),
Q("q-np-09", ["np-vector"], "Querés limitar todos los descuentos de un array a un máximo de 0.5.",
  [("np.minimum(descuentos, 0.5)", True, "Tope elemento a elemento."), ("descuentos.min()", False, "Da un solo número."), ("np.max", False, "No."), ("sorted", False, "No.")]),
Q("q-np-10", ["np-stats"], "Querés una medida de 'valor típico' que no se vea afectada por un sensor que marcó 999.",
  [("La mediana (np.median)", True, "Robusta a extremos."), ("La media", False, "Se ve arrastrada."), ("El máximo", False, "Sería 999."), ("La suma", False, "No.")]),
]

PROJECT = project(
    "Estadísticas de una red de sensores",
    "Una red de 4 sensores de temperatura registró datos durante 7 días. Uno falló. Tenés que resumir los datos, encontrar la falla y explicar su impacto.",
    "Promedio por sensor, coordenadas de la falla y un reporte con recomendaciones.",
    [("Planificar", "Ejes, reglas de anomalía y riesgos.", ["np-p1"]),
     ("Resumir", "Promedio por sensor.", ["np-p2"]),
     ("Detectar", "Umbral y coordenadas de anomalías.", ["np-p3"]),
     ("Verificar", "Detectá un error de eje.", ["np-p4"]),
     ("Reportar", "Explicá la falla y su impacto.", ["np-p5"])],
    ["Promedios por sensor", "Posición de la anomalía", "Verificación de shapes", "Reporte con recomendación"],
    ["Pedile a la IA que te explique axis o argwhere, no que haga el análisis.",
     "Antes de cada cálculo, predecí el shape del resultado.",
     "Repetí la fase 3 con un umbral distinto y sin ayuda."],
)

MODULE = module(
    "m03", "03", "NumPy", "🔢", "#a78bfa",
    "Cálculo numérico vectorizado desde el punto de vista práctico: cuándo usar arrays, cómo leer su forma y cómo resumir datos por filas o columnas.",
    learn=["Saber cuándo NumPy conviene sobre Python puro (y cuándo pandas)",
           "Leer shape y dtype para anticipar errores",
           "Indexar, recortar y filtrar matrices",
           "Usar operaciones vectorizadas, broadcasting y np.where",
           "Resumir por ejes y detectar anomalías"],
    why="NumPy es el motor de pandas, matplotlib y scikit-learn. No necesitás un curso de álgebra: necesitás **reconocer** cuándo un problema es 'la misma cuenta sobre muchos números', entender **shape** y **axis**, y leer arrays que te devuelven las librerías (por ejemplo, las predicciones de un modelo).",
    ai="Cuando la IA te dé código con arrays, pedile que te diga el shape de cada variable intermedia y verificalo. Los errores de broadcasting y de axis son los más comunes: si los entendés, los resolvés vos.",
    concepts=CONCEPTS, exercises=EXERCISES, quiz=QUIZ, project=PROJECT,
    setup=SETUP + NUMPY_SETUP, tables=["temperaturas", "notas", "precios", "sensores", "ventas_diarias"], file="numeros.py",
)
