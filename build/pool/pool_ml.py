# -*- coding: utf-8 -*-
"""Módulo 06 · Introducción a Machine Learning con scikit-learn."""

PREP_REG = """from sklearn.model_selection import train_test_split

X = casas[['m2', 'habitaciones', 'antiguedad']]
y = casas['precio']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
"""

FIT_REG = PREP_REG + """
from sklearn.linear_model import LinearRegression
modelo = LinearRegression()
modelo.fit(X_train, y_train)
predicciones = modelo.predict(X_test)
"""

PREP_CLF = """from sklearn.model_selection import train_test_split

X = churn[['meses_cliente', 'cargo_mensual', 'reclamos']]
y = churn['abandona']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
"""

FIT_CLF = PREP_CLF + """
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
modelo = LogisticRegression(max_iter=1000)
modelo.fit(X_train, y_train)
pred = modelo.predict(X_test)
"""

EXERCISES = [
# =========================================================== Preparar
dict(id="ml01", sec="Preparar los datos", title="¿Qué es Machine Learning?", level=1,
theory="""**Machine Learning** (aprendizaje automático) consiste en que un programa **aprenda patrones a partir de ejemplos**, en lugar de escribir las reglas a mano.

En el **aprendizaje supervisado**, que es el más común, le das al modelo ejemplos con la respuesta correcta:
- **X (features o variables)**: los datos de entrada (metros cuadrados, habitaciones, antigüedad…);
- **y (target u objetivo)**: lo que quieres predecir (el precio).

El modelo aprende la relación entre X e y, y después **predice y para casos nuevos**.

Hay dos grandes tipos de problema:
- **Regresión**: predecir un **número** (precio, ventas, temperatura).
- **Clasificación**: predecir una **categoría** (¿abandona o no?, ¿spam o no?).

En este módulo usarás **scikit-learn** (`sklearn`), la librería estándar de ML en Python, y dos datasets: `casas` (precios de viviendas) y `churn` (clientes que abandonan un servicio).

```python
X = df[["col1", "col2"]]    # DataFrame (doble corchete)
y = df["objetivo"]          # Series
```

> ⚠️ Por convención, `X` va en **mayúscula** (es una matriz) e `y` en **minúscula** (es un vector).""",
task="Prepara los datos del problema de precios: guarda en `X` las columnas `m2`, `habitaciones` y `antiguedad` de `casas`, y en `y` la columna `precio`.",
starter="X = \ny = ",
solution="X = casas[['m2', 'habitaciones', 'antiguedad']]\ny = casas['precio']",
hint="X = casas[['m2', 'habitaciones', 'antiguedad']]; y = casas['precio']",
check={"custom": "list(X.columns) == ['m2', 'habitaciones', 'antiguedad'] and len(X) == 200 and y.name == 'precio' and len(y) == 200",
       "custom_msg": "X debe tener las columnas m2, habitaciones y antiguedad (en ese orden) e y debe ser la columna precio."}),

dict(id="ml02", sec="Preparar los datos", title="Entrenamiento y prueba", level=2,
theory="""Si evalúas un modelo con los **mismos datos con los que aprendió**, es como darle a un estudiante el examen con las respuestas: sacará un 10 sin haber aprendido nada. Por eso los datos se dividen en dos partes:

- **train (entrenamiento)**: el modelo aprende con esto (normalmente el 70-80%);
- **test (prueba)**: se reserva para medir cómo funciona con datos que **nunca vio**.

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
```

- `test_size=0.2`: un 20% para test;
- `random_state=42`: fija la semilla para que la división sea **siempre la misma** (reproducible).

> ⚠️ Respeta el orden de las 4 variables de salida: `X_train, X_test, y_train, y_test`.""",
task="Divide `X` e `y` con `train_test_split`: **20% para test** y `random_state=42`. Guarda `X_test` en `resultado`.",
starter="from sklearn.model_selection import train_test_split\n\nX = casas[['m2', 'habitaciones', 'antiguedad']]\ny = casas['precio']\n\n# divide aquí\n\nresultado = X_test",
solution=PREP_REG + "resultado = X_test",
hint="X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)",
),

dict(id="ml03", sec="Preparar los datos", title="Variables categóricas", level=3,
theory="""Los modelos solo entienden **números**. Una columna de texto como `barrio` (`Centro`, `Norte`, `Sur`) hay que convertirla. La técnica más común es el **one-hot encoding**: se crea una columna de 0/1 por cada categoría.

```python
pd.get_dummies(df, columns=["barrio"], drop_first=True, dtype=int)
```

| barrio | → | barrio_Norte | barrio_Sur |
|---|---|---|---|
| Centro | | 0 | 0 |
| Norte | | 1 | 0 |
| Sur | | 0 | 1 |

`drop_first=True` elimina la primera categoría (`Centro`), porque es redundante: si Norte y Sur valen 0, tiene que ser Centro.

> ⚠️ **Error común:** convertir las categorías a 1, 2, 3. El modelo creería que "Sur" vale el triple que "Centro", un orden que no existe.""",
task="Aplica one-hot encoding a la columna `barrio` de `casas` con `pd.get_dummies`, usando `drop_first=True` y `dtype=int`. Guarda el DataFrame completo.",
starter="resultado = ",
solution="resultado = pd.get_dummies(casas, columns=['barrio'], drop_first=True, dtype=int)",
hint="pd.get_dummies(casas, columns=['barrio'], drop_first=True, dtype=int)",
),

# =========================================================== Regresión
dict(id="ml04", sec="Regresión: predecir números", title="Entrena tu primer modelo", level=2,
theory="""Todos los modelos de scikit-learn siguen **el mismo patrón de 3 pasos**:

```python
from sklearn.linear_model import LinearRegression

modelo = LinearRegression()      # 1. crear el modelo
modelo.fit(X_train, y_train)     # 2. entrenar: aprende de los ejemplos
modelo.predict(X_test)           # 3. predecir casos nuevos
```

La **regresión lineal** busca la fórmula:

```
precio = intercepto + coef1·m2 + coef2·habitaciones + coef3·antigüedad
```

Después de entrenar, `modelo.coef_` tiene los coeficientes: **cuánto cambia el precio por cada unidad** de cada variable. Por ejemplo, un coeficiente de 1800 en `m2` significa que cada metro cuadrado suma unos 1800 al precio.

> 💡 Una vez aprendas este patrón, cambiar de modelo (árboles, bosques, redes…) es cambiar **una sola línea**.""",
task="Crea una `LinearRegression`, entrénala con `X_train` e `y_train` y guarda sus coeficientes (`modelo.coef_`) en `resultado`.",
starter=PREP_REG + "\nfrom sklearn.linear_model import LinearRegression\n\nmodelo = \n# entrena aquí\n\nresultado = modelo.coef_",
solution=PREP_REG + "\nfrom sklearn.linear_model import LinearRegression\n\nmodelo = LinearRegression()\nmodelo.fit(X_train, y_train)\n\nresultado = modelo.coef_",
hint="modelo = LinearRegression(); modelo.fit(X_train, y_train)",
),

dict(id="ml05", sec="Regresión: predecir números", title="Hacer predicciones", level=2,
theory="""Con el modelo ya entrenado, `modelo.predict(X_nuevo)` devuelve un **array con una predicción por fila**.

```python
predicciones = modelo.predict(X_test)
predicciones[:3]      # las 3 primeras
```

Para evaluar, se comparan las predicciones con los valores reales (`y_test`), que el modelo **nunca vio** durante el entrenamiento.

> 💡 La entrada de `predict` debe tener **las mismas columnas y en el mismo orden** que usaste en `fit`.""",
task="Usa el modelo entrenado para predecir los precios de `X_test`. Guarda el array de predicciones en `resultado`.",
starter=PREP_REG + "\nfrom sklearn.linear_model import LinearRegression\nmodelo = LinearRegression()\nmodelo.fit(X_train, y_train)\n\nresultado = ",
solution=PREP_REG + "\nfrom sklearn.linear_model import LinearRegression\nmodelo = LinearRegression()\nmodelo.fit(X_train, y_train)\n\nresultado = modelo.predict(X_test)",
hint="modelo.predict(X_test)",
),

dict(id="ml06", sec="Regresión: predecir números", title="¿Qué tan bien predice? MAE", level=2,
theory="""¿Cuánto se equivoca el modelo? En regresión, la métrica más intuitiva es el **MAE** (*Mean Absolute Error*, error absoluto medio): el **promedio de lo que se equivoca**, en las mismas unidades que el objetivo.

```python
from sklearn.metrics import mean_absolute_error
mean_absolute_error(y_test, predicciones)    # por ejemplo 12500 -> se equivoca ~12.500 de media
```

Otras métricas habituales:
- **RMSE**: castiga más los errores grandes;
- **R²** (lo verás a continuación): qué proporción de la variación explica el modelo.

> 💼 **En el trabajo:** "el modelo se equivoca en promedio 12.500 € por casa" es una frase que cualquier persona del negocio entiende.""",
task="Calcula el **MAE** de las predicciones sobre el conjunto de test y guárdalo en `resultado`.",
starter=FIT_REG + "\nfrom sklearn.metrics import mean_absolute_error\nresultado = ",
solution=FIT_REG + "\nfrom sklearn.metrics import mean_absolute_error\nresultado = mean_absolute_error(y_test, predicciones)",
hint="mean_absolute_error(y_test, predicciones): primero los valores reales",
),

dict(id="ml07", sec="Regresión: predecir números", title="Coeficiente R²", level=3,
theory="""El **R²** (coeficiente de determinación) indica qué proporción de la variación del objetivo **explica** el modelo:

- **1.0**: predicción perfecta;
- **0.0**: el modelo no es mejor que predecir siempre la media;
- **negativo**: peor que la media (¡algo va mal!).

```python
from sklearn.metrics import r2_score
r2_score(y_test, predicciones)
```

Muchos modelos también lo calculan directamente con `modelo.score(X_test, y_test)`.

> 💡 Un R² "bueno" depende del problema: 0.9 es excelente para precios de casas, y en fenómenos humanos (ventas, comportamiento) un 0.5 ya puede ser útil.""",
task="Calcula el **R²** del modelo sobre el conjunto de test con `r2_score` y guárdalo en `resultado`.",
starter=FIT_REG + "\nfrom sklearn.metrics import r2_score\nresultado = ",
solution=FIT_REG + "\nfrom sklearn.metrics import r2_score\nresultado = r2_score(y_test, predicciones)",
hint="r2_score(y_test, predicciones)",
),

dict(id="ml08", sec="Regresión: predecir números", title="Predecir un caso nuevo", level=2,
theory="""El objetivo final de un modelo es **predecir casos reales nuevos**. Se prepara un DataFrame con **las mismas columnas** que usaste para entrenar:

```python
nueva = pd.DataFrame([{"m2": 120, "habitaciones": 3, "antiguedad": 5}])
modelo.predict(nueva)       # array([287000.])
modelo.predict(nueva)[0]    # el número suelto
```

`predict` siempre devuelve un **array**, aunque sea para una sola fila; con `[0]` obtienes el valor.

> 💼 **En el trabajo:** así funcionan las APIs de predicción: llega un caso nuevo, se arma su fila de datos y el modelo devuelve la respuesta.""",
task="Predice el precio de una casa de **90 m²**, **3 habitaciones** y **10 años** de antigüedad. Guarda el **número** (no el array) en `resultado`.",
starter=FIT_REG + "\nnueva = pd.DataFrame([{'m2': 90, 'habitaciones': 3, 'antiguedad': 10}])\nresultado = ",
solution=FIT_REG + "\nnueva = pd.DataFrame([{'m2': 90, 'habitaciones': 3, 'antiguedad': 10}])\nresultado = modelo.predict(nueva)[0]",
hint="modelo.predict(nueva)[0]",
),

# =========================================================== Clasificación
dict(id="ml09", sec="Clasificación: predecir categorías", title="Regresión logística", level=3,
theory="""Ahora un problema de **clasificación**: predecir si un cliente **abandona** el servicio (`abandona` = 1) o no (0). Es el famoso problema de **churn**, uno de los casos de ML más comunes en las empresas.

A pesar de su nombre, la **regresión logística** es un modelo de **clasificación**: calcula la **probabilidad** de que ocurra algo y decide 1 si pasa del 50%.

```python
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

modelo = LogisticRegression(max_iter=1000)
modelo.fit(X_train, y_train)
pred = modelo.predict(X_test)
accuracy_score(y_test, pred)      # proporción de aciertos (0 a 1)
```

- `max_iter=1000` le da al algoritmo más iteraciones para converger.
- `stratify=y` en `train_test_split` mantiene la misma proporción de 1 y 0 en train y en test.""",
task="Entrena una `LogisticRegression(max_iter=1000)`, predice sobre `X_test` y guarda la **accuracy** (proporción de aciertos) en `resultado`.",
starter=PREP_CLF + "\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.metrics import accuracy_score\n\nresultado = ",
solution=FIT_CLF + "resultado = accuracy_score(y_test, pred)",
hint="modelo = LogisticRegression(max_iter=1000); modelo.fit(...); pred = modelo.predict(X_test); accuracy_score(y_test, pred)",
),

dict(id="ml10", sec="Clasificación: predecir categorías", title="Matriz de confusión", level=3,
theory="""La accuracy puede **engañar**: si solo el 10% de los clientes abandona, un modelo que siempre dice "no abandona" acierta el 90% sin servir para nada. La **matriz de confusión** muestra **dónde** se equivoca:

|  | predice 0 | predice 1 |
|---|---|---|
| **real 0** | verdaderos negativos | falsos positivos |
| **real 1** | falsos negativos | verdaderos positivos |

```python
from sklearn.metrics import confusion_matrix
confusion_matrix(y_test, pred)
# [[40  5]
#  [12 18]]
```

Métricas que salen de aquí:
- **precision**: de los que predije como 1, ¿cuántos lo eran?
- **recall**: de los que eran 1, ¿cuántos detecté?

> 💼 **En el trabajo:** en churn importa mucho el **recall**. Cada cliente que se va sin que lo detectes es dinero perdido.""",
task="Calcula la **matriz de confusión** de las predicciones del modelo logístico y guárdala en `resultado`.",
starter=FIT_CLF + "\nfrom sklearn.metrics import confusion_matrix\nresultado = ",
solution=FIT_CLF + "\nfrom sklearn.metrics import confusion_matrix\nresultado = confusion_matrix(y_test, pred)",
hint="confusion_matrix(y_test, pred)",
),

dict(id="ml11", sec="Clasificación: predecir categorías", title="Árbol de decisión", level=3,
theory="""Un **árbol de decisión** aprende una serie de preguntas del tipo *sí/no*:

```
¿reclamos > 2?
 ├─ sí → ¿meses_cliente < 12? → abandona
 └─ no → no abandona
```

Es muy **interpretable**: puedes explicarle a cualquiera por qué predijo lo que predijo.

```python
from sklearn.tree import DecisionTreeClassifier
arbol = DecisionTreeClassifier(max_depth=3, random_state=0)
```

`max_depth` limita cuántas preguntas seguidas puede hacer. Sin límite, el árbol **memoriza** los datos de entrenamiento (**overfitting**, sobreajuste) y luego falla con datos nuevos.""",
task="Entrena un `DecisionTreeClassifier(max_depth=3, random_state=0)` y guarda su **accuracy** sobre el conjunto de test en `resultado`.",
starter=PREP_CLF + "\nfrom sklearn.tree import DecisionTreeClassifier\nfrom sklearn.metrics import accuracy_score\n\nresultado = ",
solution=PREP_CLF + "\nfrom sklearn.tree import DecisionTreeClassifier\nfrom sklearn.metrics import accuracy_score\n\narbol = DecisionTreeClassifier(max_depth=3, random_state=0)\narbol.fit(X_train, y_train)\nresultado = accuracy_score(y_test, arbol.predict(X_test))",
hint="arbol = DecisionTreeClassifier(max_depth=3, random_state=0); arbol.fit(...); accuracy_score(y_test, arbol.predict(X_test))",
),

# =========================================================== Buenas prácticas
dict(id="ml12", sec="Buenas prácticas", title="Escalado y Pipeline", level=4,
theory="""Algunos modelos, como **KNN** (vecinos más cercanos), miden **distancias** entre puntos. Si una variable va de 0 a 120 (cargo) y otra de 0 a 5 (reclamos), la primera dominaría. Por eso hay que **escalar**: `StandardScaler` estandariza cada columna (media 0 y desviación 1), como hiciste a mano en NumPy.

Un **Pipeline** encadena el preprocesado y el modelo en **un solo objeto**:

```python
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier

pipe = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=5))
pipe.fit(X_train, y_train)      # escala Y entrena
pipe.predict(X_test)            # escala con lo aprendido en train Y predice
```

> ⚠️ **Error grave muy común:** escalar **todos** los datos antes de dividir. Así se filtra información del test al entrenamiento (*data leakage*). El Pipeline lo evita automáticamente.""",
task="Crea un pipeline con `StandardScaler()` y `KNeighborsClassifier(n_neighbors=5)`, entrénalo y guarda su **accuracy** en test en `resultado`.",
starter=PREP_CLF + "\nfrom sklearn.pipeline import make_pipeline\nfrom sklearn.preprocessing import StandardScaler\nfrom sklearn.neighbors import KNeighborsClassifier\nfrom sklearn.metrics import accuracy_score\n\npipe = \nresultado = ",
solution=PREP_CLF + "\nfrom sklearn.pipeline import make_pipeline\nfrom sklearn.preprocessing import StandardScaler\nfrom sklearn.neighbors import KNeighborsClassifier\nfrom sklearn.metrics import accuracy_score\n\npipe = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=5))\npipe.fit(X_train, y_train)\nresultado = accuracy_score(y_test, pipe.predict(X_test))",
hint="pipe = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=5)); pipe.fit(...)",
),

dict(id="ml13", sec="Buenas prácticas", title="Validación cruzada", level=4,
theory="""Una sola división train/test puede salir **"con suerte"** (o sin ella). La **validación cruzada** (*cross-validation*) divide los datos en *k* partes (*folds*) y entrena *k* veces, usando cada vez una parte distinta como test:

```
Fold 1: [TEST][train][train][train][train]
Fold 2: [train][TEST][train][train][train]
...
```

```python
from sklearn.model_selection import cross_val_score
scores = cross_val_score(modelo, X, y, cv=5)   # 5 accuracies
scores.mean()                                  # la estimación final
```

Obtienes una medida **más confiable** del rendimiento y además ves cuánto varía (`scores.std()`).

> 💼 **En el trabajo:** es la forma estándar de comparar modelos antes de elegir uno.""",
task="Evalúa un `DecisionTreeClassifier(max_depth=3, random_state=0)` con **validación cruzada de 5 folds** sobre `X` e `y` completos, y guarda la **media** de los scores.",
starter="from sklearn.model_selection import cross_val_score\nfrom sklearn.tree import DecisionTreeClassifier\n\nX = churn[['meses_cliente', 'cargo_mensual', 'reclamos']]\ny = churn['abandona']\n\nresultado = ",
solution="from sklearn.model_selection import cross_val_score\nfrom sklearn.tree import DecisionTreeClassifier\n\nX = churn[['meses_cliente', 'cargo_mensual', 'reclamos']]\ny = churn['abandona']\n\nscores = cross_val_score(DecisionTreeClassifier(max_depth=3, random_state=0), X, y, cv=5)\nresultado = scores.mean()",
hint="cross_val_score(DecisionTreeClassifier(max_depth=3, random_state=0), X, y, cv=5).mean()",
),

dict(id="ml14", sec="Buenas prácticas", title="Boss final: proyecto de churn", level=4,
theory="""¡Proyecto completo, como en un trabajo real! El flujo de un proyecto de ML es:

1. **Preparar**: elegir las variables y codificar las categóricas.
2. **Dividir**: train/test.
3. **Entrenar**: aquí usarás un **Random Forest**, un "bosque" de muchos árboles que votan; suele ser muy preciso sin mucho ajuste.
4. **Evaluar** con datos no vistos.

```python
from sklearn.ensemble import RandomForestClassifier
bosque = RandomForestClassifier(n_estimators=100, random_state=42)
```

Después de entrenar, `bosque.feature_importances_` indica **qué variables pesaron más**. ¡Imprímelo con `print` para verlo!

> 💼 Con esto ya puedes armar tu primer proyecto de portfolio: "Modelo de predicción de abandono de clientes".""",
task="""1. Aplica `pd.get_dummies` a `churn` con `columns=['contrato']`, `drop_first=True` y `dtype=int` → `datos`.
2. `X` = todas las columnas de `datos` **menos** `abandona`; `y` = `datos['abandona']`.
3. Divide con `test_size=0.25`, `random_state=42` y `stratify=y`.
4. Entrena `RandomForestClassifier(n_estimators=100, random_state=42)`.
5. Guarda la **accuracy** en test en `resultado`.""",
starter="from sklearn.model_selection import train_test_split\nfrom sklearn.ensemble import RandomForestClassifier\nfrom sklearn.metrics import accuracy_score\n\n# 1. Preparar\n\n# 2. Dividir\n\n# 3. Entrenar\n\n# 4. Evaluar\nresultado = ",
solution="from sklearn.model_selection import train_test_split\nfrom sklearn.ensemble import RandomForestClassifier\nfrom sklearn.metrics import accuracy_score\n\ndatos = pd.get_dummies(churn, columns=['contrato'], drop_first=True, dtype=int)\nX = datos.drop(columns=['abandona'])\ny = datos['abandona']\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)\nbosque = RandomForestClassifier(n_estimators=100, random_state=42)\nbosque.fit(X_train, y_train)\nprint(pd.Series(bosque.feature_importances_, index=X.columns).round(3).sort_values(ascending=False))\nresultado = accuracy_score(y_test, bosque.predict(X_test))",
hint="datos = pd.get_dummies(...); X = datos.drop(columns=['abandona']); ...; accuracy_score(y_test, bosque.predict(X_test))",
),
]
