# -*- coding: utf-8 -*-
"""Módulo 06 · Introducción a Machine Learning: base conceptual y primeros modelos."""
from datasets import ML_SETUP, SETUP
from framework import A, B, C, D, E, F, G, P, Q, ask, concept, field, module, project

S1, S2, S3, S4 = "¿Esto es Machine Learning?", "Features, target y división de datos", "Regresión: predecir números", "Clasificación: predecir categorías"
S5 = "Overfitting, pipelines y validación"
SP = "Proyecto: predecir el abandono de clientes"

SPLIT_CHURN = ("from sklearn.model_selection import train_test_split\n\n"
               "X = churn[['meses_cliente', 'cargo_mensual', 'reclamos']]\n"
               "y = churn['abandona']\n"
               "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)\n")
SPLIT_CASAS = ("from sklearn.model_selection import train_test_split\n\n"
               "X = casas[['m2', 'habitaciones', 'antiguedad']]\n"
               "y = casas['precio']\n"
               "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n")

CONCEPTS = [
concept("ml-que", "¿Qué es Machine Learning?", "aprender patrones a partir de ejemplos",
    problem="Construir un modelo que **aprende una relación a partir de datos históricos** para hacer predicciones o encontrar estructura, en lugar de programar las reglas a mano.",
    when="Hay muchos ejemplos con el resultado conocido, la relación es demasiado compleja para escribirla como reglas, y equivocarse a veces es aceptable.",
    signals=["'predecir', 'estimar', 'clasificar', 'detectar', 'recomendar'", "Hay datos históricos con la respuesta", "Las reglas serían cientos de if"],
    can=["Predecir valores o categorías para casos nuevos", "Encontrar grupos parecidos sin etiquetas", "Mejorar con más y mejores datos"],
    cant=["Funcionar sin datos representativos", "Explicar causas por sí solo", "Ser la mejor opción si una regla simple o una consulta resuelve el problema"],
    nomemo="La pregunta clave antes de cualquier código: **¿esto necesita aprender de ejemplos o alcanza con una regla, un filtro o un promedio?**",
    ai="«Quiero predecir qué clientes van a dejar el servicio. ¿Es un problema de ML? ¿De qué tipo? ¿Qué datos necesitaría? No me des código todavía.»",
    verify="Compará siempre contra una solución simple (baseline): si el modelo no la supera, no aporta.",
    example="""# Regla programada:   if reclamos > 3: 'abandona'
# Machine Learning:    el modelo aprende la regla a partir de 300 clientes históricos
modelo.fit(X_train, y_train)      # aprender
modelo.predict(X_nuevos)          # predecir""",
    check=("¿Cuál de estos problemas **no** necesita Machine Learning?", [
        ("Calcular la facturación total del mes", True, "Es una suma: alcanza con pandas."),
        ("Predecir el precio de una casa a partir de sus características", False, "Es regresión."),
        ("Detectar emails de spam", False, "Es clasificación."),
    ])),

concept("ml-tipos", "Tipos de problema", "supervisado (regresión / clasificación) · no supervisado (clustering)",
    problem="Reconocer qué tipo de problema tenés, porque define el modelo, la métrica y cómo se evalúa.",
    when="Al plantear cualquier problema de ML.",
    signals=["Se predice un **número** (precio, demanda) → regresión", "Se predice una **categoría** (sí/no, tipo) → clasificación", "No hay respuesta conocida y se buscan grupos → clustering (no supervisado)"],
    can=["Supervisado: aprender de ejemplos con respuesta (target)", "No supervisado: encontrar estructura sin respuesta"],
    cant=["Evaluar un modelo no supervisado con accuracy (no hay respuesta correcta)"],
    nomemo="Mirá el **target**: ¿número? regresión. ¿categoría? clasificación. ¿No hay target? no supervisado.",
    ai="«Tengo datos de clientes sin ninguna etiqueta y quiero agruparlos por comportamiento. ¿Qué tipo de problema es y qué familia de algoritmos se usa?»",
    verify="El tipo de dato del target confirma el tipo de problema.",
    example="""# Regresión:      y = casas["precio"]        (número)
# Clasificación:  y = churn["abandona"]      (0/1)
# Clustering:     sin y, solo X""",
    check=("Predecir si un cliente pagará su crédito (sí/no) es…", [
        ("Clasificación", True, "El target es una categoría."),
        ("Regresión", False, "No se predice un número continuo."),
        ("Clustering", False, "Hay respuesta conocida en los datos históricos."),
    ])),

concept("ml-features", "Dataset, features y target", "X (features) · y (target) · filas = ejemplos",
    problem="Organizar los datos en **X** (variables que el modelo usa para predecir) e **y** (lo que se quiere predecir).",
    when="Siempre, antes de entrenar.",
    signals=["'a partir de…' → features", "'predecir…' → target", "Columnas que no estarían disponibles en el momento de predecir"],
    can=["Elegir features relevantes y disponibles al predecir", "Transformar features (encoding, escalado)"],
    cant=["Incluir el target (o algo derivado de él) en X: es **data leakage**", "Usar features que no vas a tener cuando el modelo funcione en la realidad"],
    nomemo="X = DataFrame con las columnas de entrada; y = Series con la respuesta.",
    ai="«Quiero predecir el precio de una casa. Te paso las columnas disponibles: ¿cuáles usarías como features y cuáles serían leakage?»",
    verify="Revisá `X.columns`: ¿alguna columna 'conoce' la respuesta?",
    example="""X = autos[["km", "anio", "motor"]]
y = autos["precio"]""",
    check=("Querés predecir el precio de una casa. ¿Cuál **no** debería ser una feature?", [
        ("El precio de venta final de esa misma casa", True, "Es el target: sería leakage."),
        ("Los metros cuadrados", False, "Es una feature válida."),
        ("El barrio", False, "Es una feature válida (codificada)."),
    ])),

concept("ml-split", "Entrenamiento, validación y test", "train_test_split · datos que el modelo no vio",
    problem="Evaluar el modelo con datos que **no vio** al entrenar, para estimar cómo funcionará con casos nuevos.",
    when="Siempre que evalúes un modelo.",
    signals=["'¿qué tan bien predice?'", "Comparar modelos o ajustar parámetros"],
    can=["Separar train/test: `train_test_split(X, y, test_size=0.2, random_state=42)`", "Mantener proporciones de clases: `stratify=y`", "Usar validación (o validación cruzada) para elegir modelos, y test solo al final"],
    cant=["Dar una evaluación honesta si medís sobre los datos de entrenamiento", "Ser reproducible sin `random_state`"],
    nomemo="Train para aprender, test para medir. Nunca medir con lo que se usó para aprender.",
    ai="«¿Por qué no puedo evaluar el modelo con los mismos datos con que lo entrené? ¿Para qué sirve stratify?»",
    verify="`len(X_train)` y `len(X_test)` según el test_size; con stratify, proporciones de clases parecidas en ambos.",
    example="""from sklearn.model_selection import train_test_split
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=0)""",
    check=("¿Por qué se evalúa con un conjunto de test separado?", [
        ("Para estimar el rendimiento con datos que el modelo no vio", True, "Simula casos nuevos."),
        ("Para entrenar más rápido", False, "No."),
        ("Porque sklearn lo exige", False, "No lo exige: es buena práctica."),
    ])),

concept("ml-modelo", "Modelo: entrenar y predecir", "modelo.fit(X_train, y_train) · modelo.predict(X)",
    problem="Elegir un algoritmo, entrenarlo con ejemplos (fit) y usarlo para predecir casos nuevos (predict).",
    when="Después de preparar X/y y dividir los datos.",
    signals=["Una tabla de features lista", "Un caso nuevo para predecir"],
    can=["Regresión lineal, regresión logística, árboles, bosques, KNN…: misma interfaz fit/predict", "Predecir varios casos a la vez (DataFrame con las mismas columnas)"],
    cant=["Predecir con columnas distintas (o en distinto orden) a las de entrenamiento", "Recibir una lista plana: necesita formato de tabla (2D)"],
    nomemo="Toda la API de scikit-learn es: crear → fit → predict (y score/métricas).",
    ai="«Entrené una LinearRegression con m2, habitaciones y antigüedad. ¿Cómo predigo el precio de una casa nueva y en qué formato le paso los datos?»",
    verify="Predecí un caso cuyo resultado puedas razonar (más m2 → más precio).",
    example="""from sklearn.linear_model import LinearRegression
reg = LinearRegression()
reg.fit(X_tr, y_tr)
reg.predict(pd.DataFrame([{"km": 50000, "anio": 2019, "motor": 1.6}]))""",
    check=("¿Qué hace `modelo.fit(X_train, y_train)`?", [
        ("Ajusta el modelo: aprende la relación entre features y target", True, "Es el entrenamiento."),
        ("Predice el test", False, "Eso es predict."),
        ("Divide los datos", False, "Eso es train_test_split."),
    ])),

concept("ml-metricas-reg", "Métricas de regresión", "MAE · R²",
    problem="Medir qué tan lejos están las predicciones numéricas de los valores reales.",
    when="Al evaluar un modelo de regresión.",
    signals=["Target numérico", "'¿cuánto se equivoca en promedio?'"],
    can=["MAE: error absoluto medio, en las unidades del target ('se equivoca $X en promedio')", "R²: proporción de la variabilidad explicada (1 = perfecto, 0 = como predecir el promedio)"],
    cant=["Interpretar un MAE sin contexto (¿$15.000 es mucho o poco para casas de $300.000?)"],
    nomemo="MAE para comunicar el error en unidades; R² para ver qué tanto explica el modelo.",
    ai="«Mi modelo de precios tiene MAE = 12.000 y R² = 0.9. Explicame qué significa cada uno para alguien de negocio.»",
    verify="Compará el MAE con la escala del target y con un baseline (predecir siempre la media).",
    example="""from sklearn.metrics import mean_absolute_error, r2_score
mean_absolute_error(y_test, pred)
r2_score(y_test, pred)""",
    check=("Un MAE de 15.000 en un modelo de precios significa…", [
        ("Que en promedio la predicción se equivoca por 15.000 (en las unidades del precio)", True, "Error absoluto medio."),
        ("Que acierta el 15% de las veces", False, "No es un porcentaje de aciertos."),
        ("Que el R² es 0.15", False, "Son métricas distintas."),
    ])),

concept("ml-metricas-clf", "Métricas de clasificación", "accuracy · matriz de confusión · baseline",
    problem="Medir qué tan bien clasifica un modelo y **qué tipo de errores** comete.",
    when="Al evaluar un modelo de clasificación.",
    signals=["Target categórico", "Clases desbalanceadas (pocos casos positivos)", "Errores con costos distintos (no detectar un fraude vs una falsa alarma)"],
    can=["Accuracy: proporción de aciertos", "Matriz de confusión: aciertos y errores por clase", "Comparar con el baseline de predecir siempre la clase mayoritaria"],
    cant=["Confiar en la accuracy sola con clases desbalanceadas (99% de accuracy puede ser inútil)"],
    nomemo="Siempre mirá la matriz de confusión y el baseline, no solo la accuracy.",
    ai="«Mi clasificador de fraude tiene 98% de accuracy pero solo el 2% de las transacciones son fraude. ¿Es bueno? ¿Qué métrica miro?»",
    verify="Accuracy del modelo > accuracy del baseline (clase mayoritaria).",
    example="""from sklearn.metrics import accuracy_score, confusion_matrix
accuracy_score(y_test, pred)
confusion_matrix(y_test, pred)   # filas = real, columnas = predicho""",
    check=("Con 95% de clientes que NO abandonan, un modelo que siempre dice 'no abandona' tiene accuracy…", [
        ("95%, aunque no detecta a nadie que abandona", True, "Por eso hay que comparar con el baseline y mirar la matriz."),
        ("0%", False, "Acierta todos los 'no'."),
        ("50%", False, "No."),
    ])),

concept("ml-overfit", "Overfitting y underfitting", "memorizar vs aprender · complejidad del modelo",
    problem="Detectar si el modelo **memorizó** los datos de entrenamiento (overfitting) o es **demasiado simple** para captar el patrón (underfitting).",
    when="Al comparar el rendimiento en train y en test, y al elegir la complejidad del modelo.",
    signals=["Train muy alto y test mucho más bajo → overfitting", "Train y test bajos → underfitting", "Árbol sin límite de profundidad, pocos datos y muchas features"],
    can=["Comparar métricas en train vs test", "Regular la complejidad: max_depth, n_neighbors, menos features", "Conseguir más datos"],
    cant=["Detectarse mirando solo el resultado en train"],
    nomemo="Overfitting = estudiar las respuestas del examen de práctica de memoria. Underfitting = no estudiar.",
    ai="«Mi árbol tiene 100% de accuracy en train y 70% en test. ¿Qué está pasando y qué puedo probar?»",
    verify="Siempre reportá train y test juntos.",
    example="""profundo = DecisionTreeClassifier()           # sin límite: puede memorizar
profundo.fit(X_tr, y_tr)
profundo.score(X_tr, y_tr), profundo.score(X_te, y_te)""",
    check=("Train = 99%, test = 68%. ¿Qué indica?", [
        ("Overfitting: el modelo memorizó el entrenamiento", True, "Gran diferencia entre train y test."),
        ("Underfitting", False, "Sería bajo en ambos."),
        ("Un modelo excelente", False, "El test es lo que importa."),
    ])),

concept("ml-encoding", "Variables categóricas", "one-hot encoding · pd.get_dummies",
    problem="Convertir categorías (barrio, tipo de contrato) en números que los modelos puedan usar, sin inventar un orden falso.",
    when="Una feature es texto/categoría.",
    signals=["Columnas de texto en X", "Error 'could not convert string to float' al entrenar"],
    can=["One-hot: una columna 0/1 por categoría (`get_dummies`)", "`drop_first=True` para evitar redundancia en modelos lineales"],
    cant=["Asignar números arbitrarios (Centro=1, Norte=2, Sur=3) sin crear un orden que no existe"],
    nomemo="Categorías sin orden → one-hot.",
    ai="«¿Por qué no conviene codificar barrios como 1, 2, 3 para una regresión lineal? ¿Qué hace get_dummies?»",
    verify="Revisá las columnas nuevas: una por categoría (menos una con drop_first).",
    example="""pd.get_dummies(casas, columns=["barrio"], drop_first=True, dtype=int)
# barrio → barrio_Norte, barrio_Sur (Centro queda como referencia)""",
    check=("¿Por qué no codificar 'Centro'=1, 'Norte'=2, 'Sur'=3 en una regresión lineal?", [
        ("Porque inventa un orden y distancias entre barrios que no existen", True, "El modelo creería que Sur = 3 × Centro."),
        ("Porque los modelos no aceptan números", False, "Aceptan números."),
        ("Está bien hacerlo", False, "Introduce un sesgo."),
    ])),

concept("ml-pipeline", "Pipeline conceptual de un proyecto de ML", "problema → datos → features → split → modelo → evaluación → iteración",
    problem="Ordenar el trabajo de ML de punta a punta y automatizar los pasos de preprocesamiento + modelo para evitar errores.",
    when="Cualquier proyecto de ML, aunque sea chico.",
    signals=["Preprocesamientos (escalado, encoding) que deben aplicarse igual en train y test", "Querés evaluar de forma robusta (validación cruzada)"],
    can=["Encadenar pasos: `make_pipeline(StandardScaler(), KNeighborsClassifier())`", "Validación cruzada: `cross_val_score(modelo, X, y, cv=5)`", "Comparar contra un baseline"],
    cant=["Saltear la definición del problema y la métrica de éxito"],
    nomemo="El orden mental: **problema y métrica → datos → features → split → baseline → modelo → evaluación → mejora**.",
    ai="«Te describo mi problema de churn. Armame un plan de proyecto de ML paso a paso (sin código), incluyendo baseline y métrica.»",
    verify="Cada paso tiene una verificación: tamaños, tipos, baseline, train vs test.",
    example="""from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
pipe = make_pipeline(StandardScaler(), LogisticRegression())
pipe.fit(X_tr, y_tr)""",
    check=("¿Cuál es el primer paso de un proyecto de ML?", [
        ("Definir el problema, el target y cómo se mide el éxito", True, "Sin eso, no sabés qué optimizar."),
        ("Elegir el algoritmo más potente", False, "Viene mucho después."),
        ("Escalar los datos", False, "Es un paso técnico posterior."),
    ])),
]

EXERCISES = [
# ======================================================================== S1
A("ml-a01", S1, "¿Es ML? (1)", 1, ["ml-que"],
  "Una tienda quiere saber **cuánto facturó cada sucursal el mes pasado**. ¿Necesita Machine Learning?",
  [("No: es una agregación con pandas (groupby + sum)", True, "Los datos ya tienen la respuesta: solo hay que resumirlos."),
   ("Sí, regresión", False, "No hay nada que predecir."),
   ("Sí, clasificación", False, "No."),
   ("Sí, clustering", False, "No.")]),
A("ml-a02", S1, "¿Es ML? (2)", 1, ["ml-que", "ml-tipos"],
  "Una inmobiliaria tiene 5.000 ventas históricas (m², barrio, antigüedad y precio) y quiere **estimar el precio de casas que todavía no se vendieron**. ¿Qué tipo de problema es?",
  [("ML supervisado: regresión", True, "Hay ejemplos con la respuesta (precio) y el target es un número."),
   ("ML supervisado: clasificación", False, "El precio es numérico."),
   ("No supervisado", False, "Hay target conocido."),
   ("No es ML: un promedio alcanza", False, "Un promedio ignora las características de cada casa.")]),
A("ml-a03", S1, "¿Es ML? (3)", 1, ["ml-tipos"],
  "Un banco quiere **detectar si una transacción es fraudulenta** a partir de 2 millones de transacciones etiquetadas. ¿Qué tipo de problema es?",
  [("Clasificación", True, "Target categórico: fraude sí/no."), ("Regresión", False, "No se predice un número."), ("Clustering", False, "Hay etiquetas."), ("No es ML", False, "Las reglas manuales no capturan los patrones complejos.")]),
A("ml-a04", S1, "¿Es ML? (4)", 2, ["ml-tipos"],
  "Una empresa tiene datos de compras de sus clientes (frecuencia, monto, categorías) **sin ninguna etiqueta** y quiere **agruparlos en perfiles** para hacer campañas distintas. ¿Qué tipo de problema es?",
  [("No supervisado: clustering", True, "No hay target; se buscan grupos."), ("Clasificación", False, "No hay clases conocidas."), ("Regresión", False, "No hay un número a predecir."), ("No es ML", False, "Agrupar por similitud en varias dimensiones es un problema clásico de ML.")]),
A("ml-a05", S1, "¿Es ML? (5)", 2, ["ml-que"],
  "Querés **marcar los pedidos con monto mayor a $1000** para revisarlos manualmente. ¿Necesitás ML?",
  [("No: es una regla simple (un filtro)", True, "Si la regla es conocida y simple, se programa."), ("Sí, clasificación", False, "No hay nada que aprender: la regla ya está definida."), ("Sí, regresión", False, "No."), ("Sí, clustering", False, "No.")]),

B("ml-b01", S1, "Cuándo NO usar ML", 2, ["ml-que"],
  "Tu jefe dice: *'Usemos inteligencia artificial para calcular el stock que falta reponer'*. Hoy se calcula como `stock_mínimo − stock_actual`. **¿Conviene usar ML? Explicá cuándo sí tendría sentido y cuándo no.**",
  model="Con la regla actual **no conviene**: es una cuenta exacta y conocida; un modelo agregaría complejidad y errores. ML tendría sentido si el problema cambiara a **predecir la demanda futura** (cuánto se va a vender la próxima semana) a partir de datos históricos, estacionalidad, promociones, etc., donde no hay una fórmula exacta y hay muchos ejemplos para aprender. Siempre compararía el modelo contra una solución simple (por ejemplo, el promedio de las últimas semanas).",
  checklist=["Dije que con una regla exacta no hace falta ML", "Propuse un caso donde sí tendría sentido (predecir demanda)", "Mencioné la necesidad de datos históricos/ejemplos", "Mencioné comparar con una solución simple (baseline)"],
  hints=["¿El cálculo actual tiene incertidumbre?", "¿Qué parte del problema sí es una predicción?", "¿Contra qué compararías un modelo?"]),

# ======================================================================== S2
A("ml-a06", S2, "Identificar el target", 1, ["ml-features"],
  "Querés predecir si un cliente **abandona** el servicio usando sus meses como cliente, su cargo mensual y sus reclamos. ¿Cuál es el target?",
  [("abandona", True, "Es lo que se quiere predecir."), ("meses_cliente", False, "Es una feature."), ("cargo_mensual", False, "Es una feature."), ("reclamos", False, "Es una feature.")]),

P("ml01", S2, ["ml-features"],
  ["¿Qué querés predecir? Eso es y.", "Las columnas que usás para predecir van en X (como DataFrame).", "Doble corchete para X; corchete simple para y."],
  "X es un DataFrame con las features (doble corchete) e y una Series con el target (corchete simple).",
  "X ← casas[['m2', 'habitaciones', 'antiguedad']]\ny ← casas['precio']",
  problem="Preparás un modelo para estimar precios de casas. Guardá en `X` las features `m2`, `habitaciones` y `antiguedad` de `casas`, y en `y` el target `precio`.", level=1),

P("ml02", S2, ["ml-split"],
  ["El modelo se evalúa con datos que no vio.", "train_test_split separa X e y en entrenamiento y prueba.", "test_size=0.2 y random_state=42; devuelve 4 objetos en orden."],
  "`train_test_split` separa al azar (de forma reproducible) un 20% de las filas para test; devuelve X_train, X_test, y_train, y_test.",
  "X_train, X_test, y_train, y_test ← dividir(X, y, 20% test, semilla 42)\nresultado ← X_test",
  problem="Reservá un **20% de los datos para test** (de forma reproducible, `random_state=42`). Guardá `X_test` en `resultado`."),

E("ml-e01", S2, "La feature que sabe demasiado", 3, ["ml-features", "ml-split"],
  "Este modelo de churn tiene una accuracy **sospechosamente perfecta**. Encontrá el problema y corregilo para que use solo `meses_cliente`, `cargo_mensual` y `reclamos`.",
  "from sklearn.model_selection import train_test_split\nfrom sklearn.tree import DecisionTreeClassifier\nfrom sklearn.metrics import accuracy_score\n\nX = churn[['meses_cliente', 'cargo_mensual', 'reclamos', 'abandona']]\ny = churn['abandona']\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)\narbol = DecisionTreeClassifier(max_depth=3, random_state=0).fit(X_train, y_train)\nresultado = accuracy_score(y_test, arbol.predict(X_test))",
  "from sklearn.model_selection import train_test_split\nfrom sklearn.tree import DecisionTreeClassifier\nfrom sklearn.metrics import accuracy_score\n\nX = churn[['meses_cliente', 'cargo_mensual', 'reclamos']]\ny = churn['abandona']\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)\narbol = DecisionTreeClassifier(max_depth=3, random_state=0).fit(X_train, y_train)\nresultado = accuracy_score(y_test, arbol.predict(X_test))",
  detect=("¿Por qué la accuracy es perfecta?", [
      ("El target 'abandona' está incluido dentro de las features (data leakage)", True, "El modelo 've' la respuesta."),
      ("El árbol es muy bueno", False, "Un 100% en un problema real es una señal de alerta."),
      ("Falta escalar los datos", False, "Los árboles no necesitan escalado."),
  ]),
  why="La columna `abandona` está en X: el modelo aprende 'si abandona = 1, predecí 1'. Es **data leakage**: el rendimiento es irreal porque en producción no vas a conocer la respuesta. Una métrica perfecta casi siempre es motivo para revisar X.",
  hints=["Ejecutalo: ¿qué accuracy da? ¿Es creíble?", "Revisá las columnas de X una por una.", "¿Alguna columna es la respuesta que querés predecir?"],
  pseudo="X ← solo features disponibles al predecir (sin 'abandona')"),

P("ml03", S2, ["ml-encoding"],
  ["barrio es texto: el modelo no lo puede usar así.", "Hay que convertir cada barrio en una columna 0/1.", "pd.get_dummies(df, columns=[...], drop_first=True, dtype=int)."],
  "`get_dummies` crea una columna 0/1 por barrio; con `drop_first=True` se elimina una (la de referencia), que queda implícita.",
  "resultado ← one-hot de 'barrio' en casas (drop_first, enteros)",
  problem="El barrio influye en el precio, pero es texto. Convertí la columna `barrio` de `casas` en columnas numéricas 0/1 (one-hot) con `drop_first=True` y `dtype=int`. Guardá el DataFrame completo."),

C("ml-c01", S2, "Plan: plantear un problema de ML", 3, ["ml-pipeline", "ml-tipos", "ml-features"],
  "Una telefónica quiere **anticipar qué clientes van a abandonar** para ofrecerles un descuento. Tiene la tabla `churn`. Planteá el problema antes de escribir código.",
  [field("Tipo de problema", "Supervisado, clasificación binaria.", ["Clasificación binaria", "Regresión", "Clustering"], 0),
   field("Target", "abandona (0/1).", ["abandona", "cargo_mensual", "contrato"], 0),
   field("Features candidatas", "meses_cliente, cargo_mensual, reclamos y contrato (codificado con one-hot)."),
   field("Cómo evalúo", "Train/test estratificado; accuracy comparada con el baseline (clase mayoritaria) y matriz de confusión.", ["Train/test + baseline + matriz de confusión", "Accuracy sobre los datos de entrenamiento", "Mirando algunos casos a ojo"], 0),
   field("¿Qué error es más costoso para el negocio?", "No detectar a alguien que se va (falso negativo) suele costar más que ofrecer un descuento de más (falso positivo)."),
  ],
  explain="Plantear bien el problema (tipo, target, features, evaluación y costo de los errores) es lo que determina si el modelo sirve. El código viene después.",
  hints=["¿Qué querés predecir y de qué tipo es?", "¿Qué columnas estarían disponibles antes de que el cliente se vaya?", "¿Contra qué comparás el modelo?"],
  pseudo="problema: clasificación (abandona)\nX: meses, cargo, reclamos, contrato(one-hot)\nsplit estratificado → baseline → modelo → accuracy + matriz"),

# ======================================================================== S3
P("ml04", S3, ["ml-modelo"],
  ["Crear el modelo, entrenarlo y mirar lo que aprendió.", "fit(X_train, y_train) entrena.", "Los coeficientes están en modelo.coef_."],
  "La regresión lineal aprende un coeficiente por feature: cuánto cambia el precio por cada unidad de esa feature (manteniendo las demás).",
  "modelo ← LinearRegression()\nentrenar con (X_train, y_train)\nresultado ← modelo.coef_",
  problem="Entrená una regresión lineal (`LinearRegression`) con `X_train` e `y_train` y guardá lo que aprendió (sus coeficientes, `modelo.coef_`) en `resultado`."),

P("ml05", S3, ["ml-modelo"],
  ["El modelo ya está entrenado: ahora hay que usarlo.", "predict recibe features con las mismas columnas que en el entrenamiento.", "modelo.predict(X_test)."],
  "`predict` aplica lo aprendido a las filas de X_test y devuelve un array con un precio estimado por casa.",
  "resultado ← modelo.predict(X_test)",
  problem="Usá el modelo entrenado para estimar los precios de las casas de `X_test`. Guardá el array de predicciones."),

P("ml06", S3, ["ml-metricas-reg"],
  ["¿Cuánto se equivoca el modelo en promedio?", "Comparás predicciones con los valores reales de test.", "mean_absolute_error(y_test, predicciones)."],
  "El MAE promedia la diferencia absoluta entre real y predicho: 'el modelo se equivoca en promedio por X'.",
  "resultado ← MAE(y_test, predicciones)",
  problem="¿Cuánto se equivoca el modelo en promedio? Calculá el **MAE** sobre el conjunto de test."),

E("ml-e02", S3, "Evaluar con lo que ya vio", 2, ["ml-split", "ml-metricas-reg"],
  "Este código calcula el MAE del modelo de precios, pero lo hace sobre los datos equivocados. Corregilo para obtener una evaluación honesta.",
  SPLIT_CASAS + "\nfrom sklearn.linear_model import LinearRegression\nfrom sklearn.metrics import mean_absolute_error\nmodelo = LinearRegression().fit(X_train, y_train)\nresultado = mean_absolute_error(y_train, modelo.predict(X_train))",
  SPLIT_CASAS + "\nfrom sklearn.linear_model import LinearRegression\nfrom sklearn.metrics import mean_absolute_error\nmodelo = LinearRegression().fit(X_train, y_train)\nresultado = mean_absolute_error(y_test, modelo.predict(X_test))",
  detect=("¿Qué está mal?", [
      ("Evalúa sobre los datos de entrenamiento, que el modelo ya vio", True, "La evaluación honesta es con X_test / y_test."),
      ("MAE no sirve para regresión", False, "Sí sirve."),
      ("Falta escalar", False, "No es el problema."),
  ]),
  why="Medir con los datos de entrenamiento da una estimación **optimista**: el modelo ya se ajustó a ellos. Para estimar el rendimiento con casas nuevas hay que medir sobre **test**, que no participó del entrenamiento.",
  hints=["¿Con qué datos se entrenó el modelo?", "¿Con qué datos se está midiendo?", "¿Qué conjunto simula 'casas nuevas'?"],
  pseudo="resultado ← MAE(y_test, predicciones sobre X_test)"),

P("ml07", S3, ["ml-metricas-reg"],
  ["Otra métrica: qué proporción de la variabilidad explica el modelo.", "Se compara y_test con las predicciones.", "r2_score(y_test, predicciones)."],
  "El R² compara el error del modelo con el de predecir siempre el promedio: 1 = perfecto, 0 = no mejora al promedio.",
  "resultado ← R²(y_test, predicciones)",
  problem="Calculá el **R²** del modelo sobre test (`r2_score`) y guardalo en `resultado`."),

P("ml08", S3, ["ml-modelo"],
  ["El caso nuevo tiene que tener el mismo formato que X: una tabla con las mismas columnas.", "Armá un DataFrame de una fila con m2, habitaciones y antiguedad.", "predict devuelve un array: tomá el primer elemento con [0]."],
  "predict espera una tabla (2D) con las mismas columnas que el entrenamiento; para un solo caso se arma un DataFrame de una fila y se toma el primer valor del array.",
  "nueva ← DataFrame de una fila {m2: 90, habitaciones: 3, antiguedad: 10}\nresultado ← predict(nueva)[0]",
  problem="Un cliente pregunta cuánto valdría una casa de **90 m²**, **3 habitaciones** y **10 años**. Estimá su precio y guardá el **número** (no el array) en `resultado`."),

E("ml-e03", S3, "Predecir con una lista plana", 2, ["ml-modelo"],
  "Este código intenta predecir el precio de una casa nueva, pero falla. Corregilo (devolviendo el número).",
  SPLIT_CASAS + "\nfrom sklearn.linear_model import LinearRegression\nmodelo = LinearRegression().fit(X_train, y_train)\nresultado = modelo.predict([90, 3, 10])[0]",
  SPLIT_CASAS + "\nfrom sklearn.linear_model import LinearRegression\nmodelo = LinearRegression().fit(X_train, y_train)\nnueva = pd.DataFrame([{'m2': 90, 'habitaciones': 3, 'antiguedad': 10}])\nresultado = modelo.predict(nueva)[0]",
  detect=("¿Por qué falla?", [
      ("predict espera una tabla 2D (filas × features), no una lista plana", True, "Una fila = un caso; hay que pasar [[90, 3, 10]] o un DataFrame."),
      ("El modelo no está entrenado", False, "Sí lo está."),
      ("Los números deben ser decimales", False, "No."),
  ]),
  why="scikit-learn espera siempre una estructura 2D: **filas = casos, columnas = features**. `[90, 3, 10]` es 1D y da `Expected 2D array`. Lo más claro es un DataFrame de una fila con los mismos nombres de columna que en el entrenamiento.",
  hints=["Leé el error: ¿qué forma espera?", "¿Cómo se representa 'una casa' en X?", "Armá un DataFrame de una fila con los nombres de columna."],
  pseudo="nueva ← DataFrame de una fila con las features\nresultado ← predict(nueva)[0]"),

F("ml-f01", S3, "La IA agrega el barrio al modelo", 4, ["ml-encoding", "ml-modelo", "ml-metricas-reg"],
  "Querías mejorar el modelo de precios agregando el barrio. La IA te dio este código. Analizalo antes de confiar en el resultado.",
  prompt="Tengo el DataFrame casas (m2, habitaciones, antiguedad, barrio, precio). Quiero una regresión lineal que use también el barrio. Explicá cómo tratás la variable categórica y cómo evaluás.",
  ai_code="from sklearn.model_selection import train_test_split\nfrom sklearn.linear_model import LinearRegression\nfrom sklearn.metrics import mean_absolute_error\n\ndatos = pd.get_dummies(casas, columns=['barrio'], drop_first=True, dtype=int)\nX = datos.drop(columns=['precio'])\ny = datos['precio']\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\nmodelo = LinearRegression().fit(X_train, y_train)\nresultado = mean_absolute_error(y_test, modelo.predict(X_test))",
  questions=[
      ask("¿Qué columnas tiene X?", [("m2, habitaciones, antiguedad, barrio_Norte y barrio_Sur", True, "Todo menos precio; barrio pasó a dos columnas 0/1."), ("Solo m2, habitaciones y antiguedad", False, "Incluye las columnas del barrio."), ("Incluye precio", False, "drop(columns=['precio']) lo saca.")]),
      ask("¿Por qué falta la columna barrio_Centro?", [("Por drop_first=True: Centro queda como categoría de referencia", True, "Si Norte = 0 y Sur = 0, es Centro."), ("Porque Centro no tiene casas", False, "Sí tiene."), ("Por un error", False, "Es intencional.")]),
      ask("Si el MAE baja respecto del modelo sin barrio, ¿qué podés concluir?", [("Que agregar el barrio mejora las predicciones en test", True, "Mismo split → comparación justa."), ("Que el barrio causa el precio", False, "El modelo mide asociación."), ("Nada", False, "La comparación en el mismo test es válida.")]),
      ask("¿Qué pasaría si mañana aparece una casa en un barrio nuevo ('Oeste')?", model="get_dummies no tendría una columna para ese barrio, y el DataFrame nuevo tendría columnas distintas a las de entrenamiento: habría que alinear las columnas (por ejemplo con reindex) o usar un OneHotEncoder dentro de un pipeline con handle_unknown='ignore'. Además, el modelo no sabría nada de ese barrio."),
  ],
  hints=["Ejecutalo y mirá `list(X.columns)`.", "Compará el MAE con el del ejercicio ml06.", "Pensá qué columnas tendría una casa nueva de otro barrio."],
  explain="El código codifica el barrio con one-hot, separa features y target y evalúa en test. Es correcto, pero hay que entender la categoría de referencia y el problema de categorías nuevas.",
  solution="from sklearn.model_selection import train_test_split\nfrom sklearn.linear_model import LinearRegression\nfrom sklearn.metrics import mean_absolute_error\n\ndatos = pd.get_dummies(casas, columns=['barrio'], drop_first=True, dtype=int)\nX = datos.drop(columns=['precio'])\ny = datos['precio']\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\nmodelo = LinearRegression().fit(X_train, y_train)\nresultado = mean_absolute_error(y_test, modelo.predict(X_test))"),

# ======================================================================== S4
D("ml-d01", S4, "El baseline: ¿cuánto acierta no hacer nada?", 2, ["ml-metricas-clf"],
  "Antes de entrenar un clasificador de churn, calculá la **accuracy del baseline**: predecir siempre la clase más frecuente en `y_test`. Guardala en `resultado`.",
  SPLIT_CHURN + "\nresultado = ",
  SPLIT_CHURN + "\nproporcion_1 = y_test.mean()\nresultado = max(proporcion_1, 1 - proporcion_1)",
  ["Si siempre predecís la clase más frecuente, ¿qué proporción acertás?", "La media de una columna 0/1 es la proporción de 1.", "La accuracy del baseline es la proporción de la clase mayoritaria: max(p, 1 − p)."],
  "Si siempre se predice la clase mayoritaria, se acierta exactamente la proporción de esa clase. Cualquier modelo útil tiene que superar este número.",
  "p ← proporción de 1 en y_test\nresultado ← máximo(p, 1 − p)",
  verify="Debe estar entre 0.5 y 1."),

P("ml09", S4, ["ml-modelo", "ml-metricas-clf"],
  ["Mismo patrón: crear → fit → predict → medir.", "LogisticRegression(max_iter=1000) es un clasificador.", "accuracy_score(y_test, predicciones)."],
  "La regresión logística, a pesar del nombre, es un clasificador: estima la probabilidad de abandono y predice 0/1. Se mide con accuracy en test.",
  "modelo ← LogisticRegression(max_iter=1000); entrenar\npred ← predecir X_test\nresultado ← accuracy(y_test, pred)",
  problem="Entrená un clasificador `LogisticRegression(max_iter=1000)`, predecí sobre `X_test` y guardá la **accuracy**. Después compará mentalmente con el baseline."),

P("ml10", S4, ["ml-metricas-clf"],
  ["La accuracy no dice qué tipo de errores comete.", "La matriz de confusión cruza valores reales con predichos.", "confusion_matrix(y_test, pred)."],
  "La matriz de confusión muestra aciertos y errores por clase: filas = valor real, columnas = predicción. Permite ver cuántos abandonos no se detectaron.",
  "resultado ← matriz de confusión(y_test, pred)",
  problem="¿Qué tipo de errores comete el modelo logístico? Calculá su **matriz de confusión** y guardala en `resultado`."),

B("ml-b02", S4, "Leer una matriz de confusión", 3, ["ml-metricas-clf"],
  "Un modelo de churn tiene esta matriz de confusión en test (filas = real, columnas = predicho):\n\n| | Predice 0 | Predice 1 |\n|---|---|---|\n| **Real 0** | 40 | 5 |\n| **Real 1** | 20 | 10 |\n\n**Calculá la accuracy, explicá qué errores comete y si te parece útil para el negocio de retener clientes.**",
  model="Accuracy = (40 + 10) / 75 = **0.67**. Comete dos tipos de errores: 5 **falsos positivos** (dice que se van y no se iban: se les ofrece un descuento innecesario) y 20 **falsos negativos** (se van y el modelo no los detecta). De los 30 que realmente abandonan, detecta solo 10 (33%). El baseline (predecir siempre 0) tendría 45/75 = 0.60. Mejora poco, y para retener clientes lo grave son los falsos negativos: **no parece útil todavía**; habría que priorizar detectar más abandonos (recall).",
  checklist=["Calculé la accuracy (≈0.67)", "Distinguí falsos positivos y falsos negativos", "Calculé o mencioné que detecta pocos de los que se van", "Lo comparé con el baseline", "Concluí sobre su utilidad según el costo de los errores"],
  hints=["La accuracy es la diagonal sobre el total.", "¿Cuántos de los que realmente abandonan (fila Real 1) detecta?", "¿Cuál sería la accuracy de predecir siempre 0?"]),

P("ml11", S4, ["ml-modelo"],
  ["Mismo flujo con otro algoritmo.", "DecisionTreeClassifier(max_depth=3, random_state=0).", "fit, predict y accuracy_score."],
  "Un árbol de decisión aprende reglas del tipo 'si reclamos > 2 y meses < 12…'. max_depth=3 limita su complejidad.",
  "árbol ← DecisionTreeClassifier(profundidad 3, semilla 0); entrenar\nresultado ← accuracy en test",
  problem="Probá otro algoritmo: entrená un `DecisionTreeClassifier(max_depth=3, random_state=0)` y guardá su **accuracy** en test."),

# ======================================================================== S5
G("ml-g01", S5, "Transferencia: el árbol sin límites", 4, ["ml-overfit", "ml-modelo"], "ml11",
  "Antes entrenaste un árbol limitado a profundidad 3. Ahora vas a sacar el límite y comparar **train vs test** para ver qué pasa.",
  "Entrená un `DecisionTreeClassifier(random_state=0)` **sin max_depth** y guardá en `resultado` una lista `[accuracy_train, accuracy_test]`.",
  SPLIT_CHURN + "\nfrom sklearn.tree import DecisionTreeClassifier\nfrom sklearn.metrics import accuracy_score\n\nresultado = ",
  SPLIT_CHURN + "\nfrom sklearn.tree import DecisionTreeClassifier\nfrom sklearn.metrics import accuracy_score\n\narbol = DecisionTreeClassifier(random_state=0)\narbol.fit(X_train, y_train)\nresultado = [accuracy_score(y_train, arbol.predict(X_train)), accuracy_score(y_test, arbol.predict(X_test))]",
  ["¿Qué cambia respecto del árbol de profundidad 3?", "Necesitás medir dos veces: con los datos de entrenamiento y con los de test.", "accuracy_score(y_train, arbol.predict(X_train)) y lo mismo con test."],
  "Sin límite de profundidad, el árbol puede memorizar el entrenamiento (accuracy de train cercana a 1) y rendir peor en test: overfitting. Comparar train vs test es la forma de detectarlo.",
  "árbol ← DecisionTreeClassifier sin límite; entrenar\nresultado ← [accuracy en train, accuracy en test]"),

B("ml-b03", S5, "Explicar el overfitting", 2, ["ml-overfit"],
  "En el ejercicio anterior, el árbol sin límite dio una accuracy casi perfecta en train y bastante menor en test. **Explicá qué pasó con una analogía y qué harías para mejorarlo.**",
  model="El árbol **memorizó** los ejemplos de entrenamiento (incluido el ruido) en lugar de aprender el patrón general, como alguien que estudia de memoria las respuestas del examen de práctica y falla con preguntas nuevas. Eso es **overfitting**: rinde muy bien con lo que vio y peor con datos nuevos. Para mejorarlo: limitar la complejidad (max_depth, min_samples_leaf), usar validación cruzada para elegir esos parámetros, conseguir más datos o usar modelos más robustos (como un bosque aleatorio).",
  checklist=["Expliqué que el modelo memorizó en vez de generalizar", "Usé una analogía comprensible", "Relacioné la diferencia train/test con el overfitting", "Propuse al menos una solución concreta (limitar profundidad, más datos, validación cruzada)"],
  hints=["¿Qué significa rendir perfecto en lo que ya viste?", "Pensá en estudiar para un examen.", "¿Qué parámetro controlaba la complejidad del árbol?"]),

P("ml12", S5, ["ml-pipeline"],
  ["KNN mide distancias: las escalas de las features importan.", "Un pipeline encadena el escalado y el modelo para aplicarlos siempre juntos.", "make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=5))."],
  "El pipeline aprende el escalado solo con train y lo aplica igual a test, evitando errores y fugas de información; KNN clasifica según los 5 vecinos más cercanos.",
  "pipe ← pipeline(escalado estándar → KNN con 5 vecinos); entrenar\nresultado ← accuracy en test",
  problem="Armá un pipeline con `StandardScaler()` y `KNeighborsClassifier(n_neighbors=5)`, entrenalo y guardá su **accuracy** en test."),

P("ml13", S5, ["ml-pipeline", "ml-split"],
  ["Un solo split puede tener suerte o mala suerte.", "La validación cruzada entrena y evalúa 5 veces con distintas particiones.", "cross_val_score(modelo, X, y, cv=5).mean()."],
  "`cross_val_score` divide los datos en 5 partes, entrena con 4 y evalúa con la restante, rotando; la media es una estimación más estable del rendimiento.",
  "scores ← validación cruzada de 5 folds del árbol (profundidad 3)\nresultado ← promedio de scores",
  problem="Evaluá un `DecisionTreeClassifier(max_depth=3, random_state=0)` con **validación cruzada de 5 folds** sobre `X` e `y` completos y guardá la **media** de los scores."),

A("ml-a07", S5, "¿Qué hacer primero?", 2, ["ml-pipeline"],
  "Tu jefe te pide 'un modelo de IA para predecir ventas'. ¿Cuál es el primer paso razonable?",
  [("Definir qué se predice exactamente, con qué datos y cómo se mide el éxito", True, "Sin problema y métrica claros, no hay modelo útil."),
   ("Entrenar una red neuronal", False, "Primero hay que entender el problema."),
   ("Escalar todas las columnas", False, "Es un paso técnico posterior."),
   ("Pedirle a una IA el código completo", False, "Sin plan, no podés evaluar si sirve.")]),

# ======================================================================== Proyecto
C("ml-p1", SP, "Fase 1 · Plantear el proyecto", 3, ["ml-pipeline", "ml-features", "ml-metricas-clf"],
  "**Contexto:** la telefónica quiere un primer modelo para predecir abandono con la tabla `churn` (incluye la columna categórica `contrato`). Definí el plan completo.",
  [field("Preparación de features", "One-hot de 'contrato' (drop_first); X = todo menos 'abandona'.", ["One-hot de contrato; X sin 'abandona'", "Dejar contrato como texto", "Incluir 'abandona' en X"], 0),
   field("División", "Train/test 75/25, estratificado por y, random_state=42.", ["75/25 estratificado y reproducible", "Sin dividir", "Dividir por orden de filas"], 0),
   field("Referencia mínima", "Baseline: accuracy de predecir siempre la clase mayoritaria."),
   field("Modelo", "RandomForestClassifier(n_estimators=100, random_state=42) como primer intento."),
   field("Qué reporto", "Accuracy vs baseline, matriz de confusión e importancia de variables, con sus limitaciones."),
  ],
  explain="El plan define cada paso y su verificación: encoding, split estratificado, baseline, modelo y métricas.",
  hints=["¿Qué columna no puede usarse tal cual?", "¿Qué columna nunca puede estar en X?", "¿Contra qué número vas a comparar el modelo?"],
  pseudo="datos ← one-hot(contrato)\nX, y ← datos sin 'abandona', 'abandona'\nsplit estratificado\nbaseline → bosque → métricas"),

D("ml-p2", SP, "Fase 2 · El baseline del proyecto", 3, ["ml-metricas-clf", "ml-encoding", "ml-split"],
  "Prepará los datos según el plan (one-hot de `contrato` con `drop_first=True` y `dtype=int`; X sin `abandona`), dividí 75/25 estratificado con `random_state=42` y guardá en `resultado` la **accuracy del baseline** (clase mayoritaria de `y_test`).",
  "from sklearn.model_selection import train_test_split\n\nresultado = ",
  "from sklearn.model_selection import train_test_split\n\ndatos = pd.get_dummies(churn, columns=['contrato'], drop_first=True, dtype=int)\nX = datos.drop(columns=['abandona'])\ny = datos['abandona']\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)\np = y_test.mean()\nresultado = max(p, 1 - p)",
  ["Seguí el plan: preparar → dividir → baseline.", "get_dummies sobre churn con columns=['contrato']; después separá X e y.", "El baseline es max(p, 1 − p) con p = proporción de 1 en y_test."],
  "Se preparan los datos como en el plan y se calcula la referencia mínima que el modelo deberá superar.",
  "datos ← one-hot(contrato); X, y\nsplit 75/25 estratificado\nresultado ← proporción de la clase mayoritaria en y_test"),

P("ml14", SP, ["ml-modelo", "ml-encoding", "ml-pipeline"],
  ["Repetí la preparación de la fase 2.", "Entrená un RandomForestClassifier(n_estimators=100, random_state=42).", "Medí la accuracy en test y comparala con el baseline."],
  "Un bosque aleatorio combina muchos árboles entrenados con variantes de los datos: suele generalizar mejor que un solo árbol. Las importancias muestran qué variables usa más.",
  "datos ← one-hot(contrato); X, y; split estratificado\nbosque ← RandomForest(100 árboles, semilla 42); entrenar\nresultado ← accuracy en test",
  title="Fase 3 · Entrenar el modelo",
  problem="Con los datos preparados como en la fase 2, entrená un `RandomForestClassifier(n_estimators=100, random_state=42)` y guardá su **accuracy** en test. (El código de la solución también imprime la importancia de cada variable.)"),

E("ml-p4", SP, "Fase 4 · El escalado que espía", 4, ["ml-split", "ml-pipeline"],
  "Un compañero escaló los datos **antes** de dividirlos para entrenar un KNN. Funciona, pero es una mala práctica que filtra información del test. Corregilo usando un pipeline que escale **solo con train**.",
  "from sklearn.model_selection import train_test_split\nfrom sklearn.preprocessing import StandardScaler\nfrom sklearn.neighbors import KNeighborsClassifier\nfrom sklearn.metrics import accuracy_score\n\nX = churn[['meses_cliente', 'cargo_mensual', 'reclamos']]\ny = churn['abandona']\nX_esc = StandardScaler().fit_transform(X)\nX_train, X_test, y_train, y_test = train_test_split(X_esc, y, test_size=0.25, random_state=42, stratify=y)\nknn = KNeighborsClassifier(n_neighbors=5).fit(X_train, y_train)\nresultado = accuracy_score(y_test, knn.predict(X_test))",
  "from sklearn.model_selection import train_test_split\nfrom sklearn.preprocessing import StandardScaler\nfrom sklearn.neighbors import KNeighborsClassifier\nfrom sklearn.pipeline import make_pipeline\nfrom sklearn.metrics import accuracy_score\n\nX = churn[['meses_cliente', 'cargo_mensual', 'reclamos']]\ny = churn['abandona']\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)\npipe = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=5)).fit(X_train, y_train)\nresultado = accuracy_score(y_test, pipe.predict(X_test))",
  detect=("¿Cuál es el problema?", [
      ("El escalador calcula media y desvío usando también las filas de test (data leakage)", True, "El preprocesamiento debe aprender solo de train."),
      ("KNN no necesita escalado", False, "Sí lo necesita: usa distancias."),
      ("Falta stratify", False, "stratify está."),
  ]),
  why="`fit_transform` sobre todo X calcula la media y el desvío **con los datos de test incluidos**: el modelo recibe información que en la realidad no tendría. El efecto suele ser pequeño pero la evaluación deja de ser honesta. Con un **pipeline** ajustado sobre train, el escalador aprende solo de train y se aplica igual a test.",
  hints=["¿Con qué filas se calculan la media y el desvío del StandardScaler?", "¿El test debería influir en algo del entrenamiento?", "Dividí primero y encadená escalado + modelo con make_pipeline."],
  pseudo="dividir primero\npipe ← pipeline(escalado → KNN), entrenado solo con train\nresultado ← accuracy en test",
  check={"custom": "('make_pipeline' in _pq_code or 'Pipeline' in _pq_code) and 'fit_transform' not in _pq_code and 0.5 <= float(resultado) <= 1",
         "custom_msg": "Dividí primero y usá un pipeline (make_pipeline) ajustado con train; sin fit_transform sobre todo X. Guardá la accuracy en resultado."}),

B("ml-p5", SP, "Fase 5 · Informe del modelo", 3, ["ml-metricas-clf", "ml-overfit", "ml-que"],
  "Escribí el informe para la gerencia (5-7 líneas): **qué predice el modelo, cuánto mejora al baseline, qué variables pesan más, qué tipo de errores comete y qué limitaciones y próximos pasos hay.**",
  model="El modelo predice si un cliente va a abandonar a partir de su antigüedad, cargo mensual, reclamos y tipo de contrato. En test supera al baseline (predecir que nadie se va), aunque la mejora debe leerse junto con la matriz de confusión: lo importante es cuántos abandonos detecta. Las variables más influyentes según el bosque son el cargo mensual, la antigüedad y los reclamos. Limitaciones: 300 clientes simulados, una sola partición de test, y las importancias indican asociación, no causa. Próximos pasos: validación cruzada, priorizar la detección de abandonos (recall) y probar el modelo con datos nuevos antes de usarlo para decidir descuentos.",
  checklist=["Dije qué predice y con qué datos", "Comparé con el baseline", "Mencioné las variables más importantes", "Hablé del tipo de errores (matriz de confusión / falsos negativos)", "Incluí limitaciones y próximos pasos"],
  hints=["Usá los números de las fases 2 y 3.", "Mirá la importancia de variables que imprime la solución de la fase 3.", "¿Importancia de una variable implica que causa el abandono?"]),
]

QUIZ = [
Q("q-ml-01", ["ml-tipos"], "Predecir cuántas unidades se venderán la semana que viene.",
  [("Regresión", True, "Target numérico."), ("Clasificación", False, "No es una categoría."), ("Clustering", False, "Hay histórico con respuesta."), ("No es ML", False, "Es un problema de predicción.")]),
Q("q-ml-02", ["ml-tipos"], "Clasificar reseñas de clientes como positivas o negativas a partir de miles de reseñas etiquetadas.",
  [("Clasificación", True, "Target categórico."), ("Regresión", False, "No."), ("Clustering", False, "Hay etiquetas."), ("No es ML", False, "Las reglas manuales fallarían.")]),
Q("q-ml-03", ["ml-que"], "Calcular el promedio de edad de los clientes por ciudad.",
  [("No es ML: es un groupby", True, "Resumir datos existentes."), ("Regresión", False, "No."), ("Clasificación", False, "No."), ("Clustering", False, "No.")]),
Q("q-ml-04", ["ml-tipos"], "Agrupar productos que suelen comprarse juntos sin tener categorías previas.",
  [("No supervisado", True, "No hay target."), ("Regresión", False, "No."), ("Clasificación", False, "No hay clases."), ("No es ML", False, "Es un problema clásico de ML.")]),
Q("q-ml-05", ["ml-overfit"], "Tu modelo da 100% en train y 60% en test.",
  [("Overfitting", True, "Memorizó el entrenamiento."), ("Underfitting", False, "Sería bajo en ambos."), ("Está perfecto", False, "Test es lo que importa."), ("Falta encoding", False, "No es lo que indica.")]),
Q("q-ml-06", ["ml-metricas-clf"], "El 97% de las transacciones son legítimas y tu modelo de fraude tiene 97% de accuracy.",
  [("Puede ser inútil: hay que ver la matriz de confusión", True, "Iguala al baseline."), ("Es excelente", False, "Puede no detectar ningún fraude."), ("Es overfitting", False, "No necesariamente."), ("Falta escalar", False, "No.")]),
Q("q-ml-07", ["ml-features"], "Para predecir si un cliente abandona, alguien incluye la columna 'fecha_de_baja'.",
  [("Data leakage: esa columna solo existe cuando ya se fue", True, "No estará disponible al predecir."), ("Es una buena feature", False, "Revela la respuesta."), ("Hay que escalarla", False, "No."), ("Hay que hacerle one-hot", False, "No.")]),
Q("q-ml-08", ["ml-encoding"], "Una feature es 'método de pago' con valores tarjeta, efectivo y transferencia.",
  [("One-hot encoding", True, "Categorías sin orden."), ("Asignar 1, 2, 3", False, "Inventa un orden."), ("Eliminarla siempre", False, "Puede ser útil."), ("Escalarla", False, "Es texto.")]),
Q("q-ml-09", ["ml-split"], "Querés estimar cómo funcionará el modelo con clientes nuevos.",
  [("Evaluar en un conjunto de test que no se usó al entrenar", True, "Simula datos nuevos."), ("Evaluar en train", False, "Optimista."), ("Mirar los coeficientes", False, "No mide rendimiento."), ("Entrenar más tiempo", False, "No.")]),
Q("q-ml-10", ["ml-pipeline"], "Tenés que escalar features y entrenar un KNN sin filtrar información del test.",
  [("Pipeline (escalador + modelo) ajustado solo con train", True, "Evita leakage."), ("Escalar todo antes de dividir", False, "Filtra información."), ("No escalar nunca", False, "KNN lo necesita."), ("Escalar solo el test", False, "No.")]),
Q("q-ml-11", ["ml-metricas-reg"], "Querés comunicar a un gerente cuánto se equivoca, en pesos, tu modelo de precios.",
  [("MAE", True, "Está en las unidades del target."), ("Accuracy", False, "Es para clasificación."), ("Matriz de confusión", False, "Es para clasificación."), ("Correlación", False, "No mide error.")]),
Q("q-ml-12", ["ml-modelo"], "Ya entrenaste un modelo y querés la predicción para 50 casos nuevos.",
  [("modelo.predict(DataFrame con las mismas columnas)", True, "Mismas features, mismo orden."), ("modelo.fit con los nuevos", False, "Eso reentrena."), ("train_test_split", False, "No."), ("get_dummies del modelo", False, "No.")]),
]

PROJECT = project(
    "Predecir el abandono de clientes",
    "Una telefónica quiere anticipar qué clientes van a darse de baja para ofrecerles un descuento. Es tu primer proyecto de clasificación de punta a punta.",
    "Un modelo evaluado honestamente contra un baseline, con sus errores, variables importantes y limitaciones explicadas.",
    [("Plantear", "Tipo de problema, features, split, baseline y métricas.", ["ml-p1"]),
     ("Baseline", "Preparar datos y calcular la referencia mínima.", ["ml-p2"]),
     ("Modelo", "Entrenar un bosque aleatorio y medirlo.", ["ml14"]),
     ("Verificar", "Detectar una fuga de información en el escalado.", ["ml-p4"]),
     ("Informar", "Resultados, errores y límites para la gerencia.", ["ml-p5"])],
    ["Plan del proyecto", "Baseline calculado", "Modelo con accuracy en test", "Pipeline sin leakage", "Informe para la gerencia"],
    ["La IA puede ayudarte con la API de scikit-learn; el planteo del problema, el baseline y la interpretación son tuyos.",
     "Desconfiá de cualquier métrica 'perfecta': buscá leakage.",
     "Repetí la fase 3 con otro modelo (por ejemplo, un árbol) sin ayuda."],
)

MODULE = module(
    "m06", "06", "Introducción a Machine Learning", "🤖", "#facc15",
    "Una base conceptual sólida: reconocer si un problema es de ML y de qué tipo, preparar features y target, entrenar, evaluar honestamente y detectar overfitting y leakage.",
    learn=["Reconocer si un problema necesita ML y de qué tipo es (regresión, clasificación, no supervisado)",
           "Separar features y target y evitar data leakage",
           "Entrenar y predecir con la interfaz fit/predict de scikit-learn",
           "Evaluar con test, baseline y métricas adecuadas (MAE, R², accuracy, matriz de confusión)",
           "Detectar overfitting y usar pipelines y validación cruzada"],
    why="Este módulo no pretende enseñarte todo Machine Learning. Pretende que puedas **reconocer** un problema de ML, **plantearlo** bien y **evaluar** si un modelo realmente sirve. Una IA te puede escribir `RandomForestClassifier().fit(...)` en segundos; lo que no te puede dar es el criterio para saber si el resultado es honesto, útil o una ilusión por leakage.",
    ai="Usá la IA para la API de scikit-learn y para que critique tu planteo. Pero definí vos el target, las features, el baseline y la métrica. Ante una métrica sorprendentemente buena, preguntale (y preguntate) dónde podría haber leakage.",
    concepts=CONCEPTS, exercises=EXERCISES, quiz=QUIZ, project=PROJECT,
    setup=SETUP + ML_SETUP, packages=["scikit-learn"], tables=["casas", "churn"], file="modelo.py",
)
