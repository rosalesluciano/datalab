# -*- coding: utf-8 -*-
"""Módulo 04 · Matplotlib: elegir el gráfico que responde la pregunta."""
from datasets import PLT_SETUP, SETUP
from framework import A, B, C, D, E, F, G, P, Q, ask, concept, field, module, project

S1, S2, S3, S4 = "¿Qué gráfico responde mi pregunta?", "Evolución en el tiempo: líneas", "Comparar categorías: barras", "Distribuciones: histogramas"
S5, S6, S7 = "Relaciones: dispersión", "Anatomía de un gráfico legible", "Varios gráficos y pandas"
SP = "Proyecto: dashboard básico de ventas"

PLOT = "Ejecutá el código y mirá el gráfico: ¿responde la pregunta?"

CONCEPTS = [
concept("viz-pregunta", "Elegir el gráfico según la pregunta", "pregunta → tipo de dato → gráfico",
    problem="Elegir la visualización correcta: cada tipo de gráfico responde un tipo de pregunta.",
    when="Antes de escribir cualquier código de gráficos.",
    signals=["'¿cómo evolucionó…?' → línea", "'¿quién vende más?' → barras", "'¿cómo se distribuye…?' → histograma", "'¿hay relación entre…?' → dispersión"],
    can=["Comparar categorías (barras)", "Mostrar evolución (líneas)", "Ver distribuciones (histogramas, boxplots)", "Estudiar relaciones (scatter)"],
    cant=["Compensar una mala elección de gráfico con colores o estilo"],
    nomemo="Memorizá las 4 preguntas y su gráfico. La sintaxis es casi siempre `plt.<tipo>(x, y)`.",
    ai="«Quiero mostrar cómo cambiaron las ventas mes a mes y compararlas con los gastos. ¿Qué gráfico me recomendás y por qué? Después mostrame el código.»",
    verify="Mirá el gráfico y preguntate: ¿alguien que no conoce los datos entiende la respuesta en 5 segundos?",
    example="""plt.plot(meses, ingresos)        # evolución
plt.bar(categorias, totales)      # comparar categorías
plt.hist(valores, bins=12)        # distribución
plt.scatter(visitas, ventas)      # relación""",
    check=("Querés ver si más visitas a la web se asocian con más ventas. ¿Qué gráfico?", [
        ("Dispersión (scatter)", True, "Dos variables numéricas → relación."),
        ("Torta", False, "Es para partes de un todo."),
        ("Histograma", False, "Muestra una sola variable."),
    ])),

concept("plt-line", "Gráfico de líneas", "plt.plot(x, y)",
    problem="Mostrar cómo cambia una variable a lo largo de algo ordenado, típicamente el tiempo.",
    when="'evolución', 'tendencia', 'mes a mes', 'a lo largo del año'.",
    signals=["El eje X es tiempo u otra secuencia ordenada", "Querés comparar tendencias de 2-3 series"],
    can=["Una o varias series en el mismo gráfico (con label + legend)", "Marcadores y estilos de línea"],
    cant=["Representar bien categorías sin orden (para eso: barras)"],
    nomemo="plot(x, y). Lo demás (color, marker, linestyle) se busca cuando hace falta.",
    ai="«Tengo ventas diarias de 90 días y la línea se ve muy ruidosa. ¿Qué opciones tengo para ver la tendencia?»",
    verify="El eje X debe estar ordenado y tener la unidad de tiempo correcta.",
    example="""plt.plot(dias, sensor_a, label="Sensor A")
plt.plot(dias, sensor_b, label="Sensor B")
plt.legend()""",
    check=("¿Para qué pregunta es ideal un gráfico de líneas?", [
        ("¿Cómo evolucionaron las ventas mes a mes?", True, "Evolución en el tiempo."),
        ("¿Qué porcentaje representa cada categoría?", False, "Eso es composición."),
        ("¿Cómo se distribuyen las edades?", False, "Eso es un histograma."),
    ])),

concept("plt-bar", "Gráfico de barras", "plt.bar · plt.barh",
    problem="Comparar una cantidad entre categorías.",
    when="'¿qué producto tiene más stock?', 'ventas por región', 'top 5'.",
    signals=["Una variable categórica y un número por categoría", "Rankings"],
    can=["Barras verticales u horizontales (mejor para nombres largos)", "Ordenarlas para facilitar la comparación"],
    cant=["Mostrar distribuciones (eso es histograma)", "Representar bien muchas categorías (más de ~15)"],
    nomemo="bar(categorías, valores); barh para etiquetas largas. Ordená antes de graficar.",
    ai="«Quiero un top 5 de productos por facturación. ¿Barras verticales u horizontales? ¿Cómo las ordeno?»",
    verify="Las barras deberían empezar en 0 (si no, exageran las diferencias).",
    example="""top = vendedores.nlargest(5, "ventas")
plt.barh(top["nombre"], top["ventas"])""",
    check=("¿Por qué el eje de un gráfico de barras debería empezar en 0?", [
        ("Porque la longitud de la barra representa el valor: cortarla exagera diferencias", True, "Es la forma más común de engañar con gráficos."),
        ("Porque matplotlib lo exige", False, "No lo exige."),
        ("No importa", False, "Sí importa."),
    ])),

concept("plt-hist", "Histograma", "plt.hist(valores, bins)",
    problem="Ver cómo se **distribuye** una variable numérica: dónde se concentran los valores, si hay asimetría o valores extremos.",
    when="'¿cómo se distribuyen…?', '¿qué valores son típicos?', '¿hay outliers?'.",
    signals=["Una sola variable numérica con muchos valores"],
    can=["Agrupar valores en intervalos (bins) y contar cuántos caen en cada uno", "Detectar asimetría, varios picos y outliers"],
    cant=["Comparar categorías (no confundir con barras)", "Ser interpretado igual con cualquier número de bins"],
    nomemo="hist(valores, bins=n). Probá distintos bins: la forma puede cambiar.",
    ai="«Hice un histograma de ventas diarias y veo dos picos. ¿Qué podría significar y cómo lo investigo?»",
    verify="La suma de las alturas = cantidad de datos.",
    example="""plt.hist(empleados["edad"], bins=10, edgecolor="black")""",
    check=("¿Qué diferencia a un histograma de un gráfico de barras?", [
        ("El histograma agrupa una variable numérica en intervalos; las barras comparan categorías", True, "Distribución vs comparación."),
        ("Ninguna", False, "Responden preguntas distintas."),
        ("El histograma es horizontal", False, "No."),
    ])),

concept("plt-scatter", "Gráfico de dispersión", "plt.scatter(x, y)",
    problem="Estudiar la **relación** entre dos variables numéricas: si crecen juntas, si hay grupos u outliers.",
    when="'¿hay relación entre…?', '¿más X implica más Y?'.",
    signals=["Dos variables numéricas por observación"],
    can=["Ver tendencias, grupos y valores atípicos", "Colorear por una tercera variable"],
    cant=["Probar causalidad: mostrar que X e Y se mueven juntas no prueba que una cause la otra"],
    nomemo="scatter(x, y). La interpretación (correlación ≠ causalidad) es lo importante.",
    ai="«Mi scatter de visitas vs ventas muestra una tendencia positiva. ¿Qué puedo concluir y qué no?»",
    verify="Cantidad de puntos = cantidad de observaciones.",
    example="""plt.scatter(clima["temperatura"], clima["helados_vendidos"])
plt.xlabel("Temperatura"); plt.ylabel("Helados vendidos")""",
    check=("Un scatter muestra que heladerías con más ventas tienen más turistas cerca. ¿Qué podés afirmar?", [
        ("Que hay una asociación; no que una cosa cause la otra", True, "Puede haber una tercera variable (verano)."),
        ("Que los turistas causan las ventas", False, "Correlación ≠ causalidad."),
        ("Nada", False, "Sí muestra una asociación."),
    ])),

concept("plt-anatomia", "Anatomía de un gráfico legible", "título · etiquetas de ejes · leyenda · unidades",
    problem="Que el gráfico se entienda solo: qué se muestra, en qué unidades y qué es cada serie.",
    when="Siempre que el gráfico vaya a ser visto por otra persona (o por vos dentro de un mes).",
    signals=["Ejes sin nombre", "Varias series sin leyenda", "Números sin unidades"],
    can=["`plt.title`, `plt.xlabel`, `plt.ylabel`", "`label=` en cada serie + `plt.legend()`", "Rotar etiquetas largas: `plt.xticks(rotation=45)`"],
    cant=["Tener leyenda si las series no tienen `label`"],
    nomemo="Checklist: título que responda la pregunta, ejes con unidades, leyenda si hay más de una serie.",
    ai="«Revisá este gráfico (te describo título, ejes y series): ¿qué le falta para que lo entienda alguien de otra área?»",
    verify="Mostralo sin explicar nada: ¿se entiende?",
    example="""plt.plot(dias, temp_a, label="Sensor A")
plt.title("Temperatura diaria"); plt.xlabel("Día"); plt.ylabel("Temperatura (°C)")
plt.legend()""",
    check=("Llamás a `plt.legend()` y la leyenda sale vacía. ¿Qué falta?", [
        ("El parámetro `label=` en cada serie", True, "La leyenda muestra los labels."),
        ("Un título", False, "No tiene relación."),
        ("plt.show()", False, "No."),
    ])),

concept("plt-subplots", "Varios gráficos: figura y ejes", "fig, axes = plt.subplots(filas, columnas)",
    problem="Combinar varios gráficos en una figura (un mini dashboard) para comparar vistas de los mismos datos.",
    when="Querés mostrar varias preguntas a la vez, lado a lado.",
    signals=["'dashboard', 'lado a lado', 'en una sola figura'"],
    can=["Crear una grilla: `fig, axs = plt.subplots(2, 2)`", "Dibujar en cada eje: `axs[0, 0].plot(...)`", "Títulos por eje: `ax.set_title(...)`"],
    cant=["Dibujar en un eje concreto usando `plt.plot` (dibuja en el último eje activo)"],
    nomemo="Con subplots, dibujá siempre con el objeto `ax` (ax.plot, ax.bar, ax.set_title).",
    ai="«Quiero un dashboard de 2×2. ¿Cuál es la diferencia entre plt.plot y ax.plot y por qué importa con subplots?»",
    verify="Cada eje debe tener su gráfico y su título.",
    example="""fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
ax1.plot(dias, temperatura); ax1.set_title("Evolución")
ax2.hist(temperatura, bins=8); ax2.set_title("Distribución")""",
    check=("Con `fig, axs = plt.subplots(1, 2)`, ¿dónde dibuja `plt.plot(...)`?", [
        ("En el último eje activo (normalmente el de la derecha)", True, "Por eso conviene usar ax.plot."),
        ("En los dos", False, "No."),
        ("En una figura nueva", False, "No."),
    ])),

concept("plt-pandas", "Graficar desde pandas", "df.plot(x, y, kind=...)",
    problem="Hacer gráficos rápidos directamente desde un DataFrame o Series (pandas usa matplotlib por debajo).",
    when="Exploración rápida de una tabla o de un resultado de groupby.",
    signals=["Ya tenés una Series/DataFrame con los datos listos"],
    can=["`df.plot(x='fecha', y='ventas')`", "`serie.plot(kind='bar')` después de un groupby", "Ajustar con matplotlib (título, ejes) después"],
    cant=["Reemplazar el razonamiento sobre qué gráfico usar"],
    nomemo="`.plot(kind=...)` con line, bar, barh, hist, scatter.",
    ai="«Tengo el resultado de un groupby por categoría. ¿Cómo lo grafico como barras directamente desde pandas?»",
    verify="Igual que con matplotlib: título, ejes, unidades.",
    example="""clima.plot(x="fecha", y="temperatura", title="Temperatura")
df.groupby("region")["ventas"].sum().plot(kind="bar")""",
    check=("¿Qué librería dibuja cuando usás `df.plot()`?", [
        ("Matplotlib, por debajo", True, "pandas delega en matplotlib."),
        ("Seaborn", False, "No."),
        ("Ninguna: pandas dibuja solo", False, "Usa matplotlib."),
    ])),

concept("viz-interpretar", "Interpretar (y no engañar)", "lectura crítica · ejes · escalas · tortas",
    problem="Sacar conclusiones correctas de un gráfico y detectar gráficos engañosos.",
    when="Al leer gráficos ajenos y antes de presentar los propios.",
    signals=["Ejes que no empiezan en 0 en barras", "Tortas con muchas porciones", "Conclusiones causales a partir de un scatter"],
    can=["Describir: tendencia, picos, comparación, dispersión", "Detectar: escalas engañosas, falta de contexto, causalidad no probada"],
    cant=["Concluir más de lo que muestran los datos"],
    nomemo="Tres preguntas: ¿qué muestra?, ¿qué NO muestra?, ¿podría estar engañando?",
    ai="«Te describo un gráfico: [descripción]. ¿Qué conclusiones son válidas y cuáles no?»",
    verify="Cada afirmación sobre el gráfico debe poder señalarse en el gráfico.",
    example="""# Torta: solo para pocas partes de un todo (2-4)
partes = pedidos_web["canal"].value_counts()
plt.pie(partes, labels=partes.index, autopct="%1.0f%%")""",
    check=("¿Cuándo una torta es una mala elección?", [
        ("Cuando hay muchas categorías o valores parecidos", True, "Las porciones son difíciles de comparar; mejor barras."),
        ("Siempre que haya porcentajes", False, "Con 2-4 partes puede funcionar."),
        ("Nunca", False, "A veces sí lo es."),
    ])),
]

EXERCISES = [
# ======================================================================== S1
A("plt-a01", S1, "Evolución en el tiempo", 1, ["viz-pregunta", "plt-line"],
  "Pregunta: **¿cómo evolucionaron los ingresos mes a mes durante el semestre?** ¿Qué gráfico necesitás?",
  [("Línea", True, "Tiempo en X, valor en Y."), ("Torta", False, "No muestra evolución."), ("Histograma", False, "Muestra distribución, no evolución."), ("Dispersión", False, "Para relación entre dos variables.")]),
A("plt-a02", S1, "Comparar categorías", 1, ["viz-pregunta", "plt-bar"],
  "Pregunta: **¿qué producto tiene más stock?** ¿Qué gráfico necesitás?",
  [("Barras", True, "Una categoría (producto) y un número (stock)."), ("Línea", False, "Los productos no tienen orden temporal."), ("Histograma", False, "No es una distribución."), ("Scatter", False, "No hay dos variables numéricas.")]),
A("plt-a03", S1, "Distribución", 1, ["viz-pregunta", "plt-hist"],
  "Pregunta: **¿cómo se distribuyen las ventas diarias? ¿Hay días atípicos?** ¿Qué gráfico necesitás?",
  [("Histograma", True, "Una variable numérica → distribución."), ("Barras por día", False, "90 barras no muestran la distribución."), ("Torta", False, "No."), ("Línea", False, "Mostraría la evolución, no la distribución.")]),
A("plt-a04", S1, "Relación entre variables", 1, ["viz-pregunta", "plt-scatter"],
  "Pregunta: **¿los días con más visitas tienen más ventas?** ¿Qué gráfico necesitás?",
  [("Dispersión (scatter)", True, "Dos variables numéricas por día."), ("Torta", False, "No."), ("Barras", False, "No compara categorías."), ("Histograma", False, "Una sola variable.")]),

C("plt-c01", S1, "Plan: el gráfico de una pregunta de negocio", 2, ["viz-pregunta", "plt-anatomia"],
  "Dirección pregunta: **'¿Los ingresos crecen más rápido que los gastos?'** Tenés `meses`, `ingresos` y `gastos`. Planificá el gráfico antes de programarlo.",
  [field("Tipo de pregunta", "Evolución en el tiempo y comparación de dos series.", ["Evolución de dos series en el tiempo", "Distribución", "Composición de un total"], 0),
   field("Gráfico", "Dos líneas en el mismo gráfico.", ["Dos líneas en el mismo gráfico", "Dos tortas", "Un histograma"], 0),
   field("Eje X y eje Y", "X: meses; Y: monto en miles."),
   field("Elementos de legibilidad", "Título que responda la pregunta, etiquetas de ejes con unidades y leyenda con Ingresos y Gastos."),
   field("¿Qué tendría que verse para responder 'sí'?", "Que la distancia entre la línea de ingresos y la de gastos aumente mes a mes."),
  ],
  explain="El plan parte de la pregunta (evolución comparada), elige el gráfico (líneas) y define qué tendría que verse para responderla.",
  hints=["¿La pregunta habla de tiempo?", "¿Cuántas series hay que comparar?", "¿Qué patrón visual indicaría que los ingresos crecen más rápido?"],
  pseudo="línea(meses, ingresos, label='Ingresos')\nlínea(meses, gastos, label='Gastos')\ntítulo, ejes, leyenda"),

# ======================================================================== S2
P("plt01", S2, ["plt-line"],
  ["Es una evolución mes a mes: ¿qué gráfico?", "En X van los meses y en Y los ingresos.", "plt.plot(x, y)"],
  "`plt.plot(x, y)` dibuja una línea uniendo los puntos (mes, ingreso) en orden.",
  "línea(meses, ingresos)",
  problem="Mostrá cómo evolucionaron los `ingresos` a lo largo de los `meses`.", level=1),

P("plt02", S2, ["plt-anatomia", "plt-line"],
  ["El gráfico tiene que entenderse sin explicación.", "Faltan título y nombres de ejes.", "plt.title, plt.xlabel, plt.ylabel (con el texto exacto)."],
  "Título y etiquetas convierten una línea en un gráfico interpretable: qué se muestra y en qué unidades.",
  "línea(meses, ingresos)\ntítulo 'Ingresos por mes'; eje X 'Mes'; eje Y 'Ingresos (miles)'",
  problem="Graficá los `ingresos` por mes y hacé que se entienda solo: título **\"Ingresos por mes\"**, eje X **\"Mes\"** y eje Y **\"Ingresos (miles)\"** (exactamente así)."),

P("plt03", S2, ["plt-line", "plt-anatomia"],
  ["Son dos series sobre el mismo eje de tiempo.", "Dos llamadas a plot en el mismo gráfico; cada una con su label.", "plt.legend() muestra los labels."],
  "Cada `plot` agrega una línea; `label=` le da nombre y `legend()` muestra la leyenda para distinguirlas.",
  "línea(meses, ingresos, label='Ingresos')\nlínea(meses, gastos, label='Gastos')\nleyenda",
  problem="Implementá tu plan: `ingresos` y `gastos` por mes en el mismo gráfico, con las etiquetas **\"Ingresos\"** y **\"Gastos\"** y la leyenda visible."),

E("plt-e01", S2, "La leyenda vacía", 2, ["plt-anatomia"],
  "Este gráfico debería mostrar una leyenda con Ingresos y Gastos, pero la leyenda no aparece. Corregilo.",
  "plt.plot(meses, ingresos)\nplt.plot(meses, gastos)\nplt.legend()",
  "plt.plot(meses, ingresos, label='Ingresos')\nplt.plot(meses, gastos, label='Gastos')\nplt.legend()",
  detect=("¿Por qué no hay leyenda?", [
      ("Las líneas no tienen `label`, así que legend() no tiene qué mostrar", True, "La leyenda muestra los labels de cada serie."),
      ("legend() va antes de plot()", False, "Va después."),
      ("Falta plt.show()", False, "No es el problema."),
  ]),
  why="`plt.legend()` muestra el `label` de cada serie. Si ninguna serie tiene label, no hay nada que mostrar (matplotlib avisa 'No artists with labels found').",
  hints=["Mirá la salida: ¿hay algún aviso?", "¿De dónde saca la leyenda los nombres?", "Agregá un parámetro a cada plot."],
  pseudo="línea(..., label='Ingresos'); línea(..., label='Gastos'); leyenda",
  check={"plot": True, "custom": "len(_ax().lines) == 2 and sorted(_legend()) == ['Gastos', 'Ingresos']",
         "custom_msg": "Deben verse 2 líneas y una leyenda con 'Ingresos' y 'Gastos'."}),

E("plt-e02", S2, "Los ejes al revés", 2, ["plt-line"],
  "Este gráfico de evolución quedó con los meses en el eje vertical. Corregilo para que el tiempo vaya en X.",
  "plt.plot(ingresos, meses)",
  "plt.plot(meses, ingresos)",
  detect=("¿Qué está mal?", [
      ("El orden de los argumentos: plot(x, y) recibe primero el eje X", True, "El tiempo va en X."),
      ("Falta un título", False, "No es el problema principal."),
      ("Debería ser un gráfico de barras", False, "Línea es correcto para evolución."),
  ]),
  why="`plt.plot(x, y)`: el primer argumento va al eje horizontal. Por convención, el tiempo (meses) va en X y la variable medida en Y.",
  hints=["Mirá el gráfico: ¿dónde quedaron los meses?", "¿Qué argumento va al eje X?", "Invertí el orden."],
  pseudo="línea(meses, ingresos)",
  check={"plot": True, "custom": "len(_ax().lines) == 1 and list(_ax().lines[0].get_ydata()) == ingresos",
         "custom_msg": "Debe haber una línea con los meses en X y los ingresos en Y."}),

P("plt04", S2, ["plt-line", "plt-anatomia"],
  ["Son tres opciones de estilo de la misma línea.", "plot acepta parámetros de color, marcador y estilo de línea.", "color='green', marker='o', linestyle='--'."],
  "Los parámetros de estilo (color, marker, linestyle) cambian cómo se ve la línea sin cambiar los datos.",
  "línea(meses, ingresos, verde, marcador 'o', guiones '--')",
  problem="Graficá `ingresos` por mes en color **\"green\"**, con marcador **\"o\"** y línea de guiones **\"--\"**."),

# ======================================================================== S3
P("plt05", S3, ["plt-bar"],
  ["Comparás una cantidad entre categorías (productos).", "Barras: categorías en X, valores en Y.", "plt.bar(categorías, valores); rotá las etiquetas si se superponen."],
  "`plt.bar` dibuja una barra por producto con altura igual a su stock.",
  "barras(productos['producto'], productos['stock'])",
  problem="¿Qué productos tienen más (y menos) stock? Dibujá un gráfico con el `stock` de cada `producto` de la tabla `productos`, en el orden de la tabla.", level=1),

P("plt06", S3, ["plt-bar", "pd-ordenar"],
  ["Primero los datos: los 5 más caros.", "nlargest(5, 'precio') da el top.", "Barras horizontales: plt.barh(categorías, valores)."],
  "Se seleccionan los 5 más caros con `nlargest` y se grafican con barras horizontales (más legibles para nombres).",
  "top ← 5 productos más caros\nbarras_horizontales(top['producto'], top['precio'])",
  problem="Mostrá un **top 5 de productos más caros** con barras horizontales (`producto` y `precio`)."),

D("plt-d01", S3, "Stock total por categoría", 3, ["plt-bar", "pd-groupby"],
  "¿Qué categoría tiene más unidades en stock? Calculá el **stock total por categoría** y graficalo con barras (una barra por categoría).",
  "",
  "stock_cat = productos.groupby('categoria')['stock'].sum()\nplt.bar(stock_cat.index, stock_cat.values)\nplt.title('Stock por categoría')",
  ["Primero los datos: hay que agregar antes de graficar.", "groupby('categoria')['stock'].sum() te da una Series categoría → total.", "El índice va a X y los valores a Y en plt.bar."],
  "Se agrega con groupby (una fila por categoría) y se grafica el resultado: los gráficos de barras casi siempre muestran datos ya resumidos.",
  "stock_cat ← suma de stock por categoría\nbarras(stock_cat.index, stock_cat.values)",
  check={"plot": True, "custom": "len(_ax().patches) == 4 and sorted(_heights()) == sorted(productos.groupby('categoria')['stock'].sum().tolist())",
         "custom_msg": "Debe haber 4 barras (una por categoría) con el stock total de cada una."}),

G("plt-g01", S3, "Transferencia: ordenar las barras", 3, ["plt-bar", "pd-ordenar"], "plt-d01",
  "Antes graficaste el stock por categoría en orden alfabético. Ahora querés que las barras queden **ordenadas de mayor a menor** para facilitar la comparación.",
  "Graficá el **stock total por categoría** con las barras ordenadas de **mayor a menor**.",
  "",
  "stock_cat = productos.groupby('categoria')['stock'].sum().sort_values(ascending=False)\nplt.bar(stock_cat.index, stock_cat.values)",
  ["¿Dónde se decide el orden de las barras: en el gráfico o en los datos?", "Ordená la Series antes de graficar.", "sort_values(ascending=False)."],
  "El orden de las barras es el orden de los datos: basta con ordenar la Series antes de graficar.",
  "stock_cat ← suma por categoría, ordenada de mayor a menor\nbarras(stock_cat.index, stock_cat.values)",
  check={"plot": True, "custom": "len(_ax().patches) == 4 and _heights() == sorted(productos.groupby('categoria')['stock'].sum().tolist(), reverse=True)",
         "custom_msg": "Deben verse 4 barras con el stock por categoría, de mayor a menor."}),

# ======================================================================== S4
P("plt07", S4, ["plt-hist"],
  ["La pregunta es sobre la distribución de una variable.", "Histograma: agrupa los valores en intervalos.", "plt.hist(valores, bins=12)."],
  "El histograma divide el rango de ventas en 12 intervalos y cuenta cuántos días cae en cada uno.",
  "histograma(ventas_diarias['ventas'], 12 intervalos)",
  problem="¿Cómo se distribuyen las ventas diarias? Dibujá la distribución de `ventas` de `ventas_diarias` con **12 intervalos (bins)**."),

G("plt-g02", S4, "Transferencia: distribución de visitas", 2, ["plt-hist"], "plt07",
  "Misma pregunta (distribución), otra variable y otra cantidad de intervalos.",
  "Dibujá la distribución de `visitas` de `ventas_diarias` con **8 intervalos** y el título **\"Distribución de visitas\"**.",
  "",
  "plt.hist(ventas_diarias['visitas'], bins=8)\nplt.title('Distribución de visitas')",
  ["¿Qué cambia respecto del ejercicio anterior?", "Mismo tipo de gráfico, otra columna y otro número de bins.", "Agregá el título."],
  "Mismo gráfico (histograma), otra variable: la habilidad es reconocer la pregunta 'distribución', no recordar la línea de código.",
  "histograma(visitas, 8 intervalos); título",
  check={"plot": True, "custom": "len(_ax().patches) == 8 and sum(_heights()) == 90 and _ax().get_title() == 'Distribución de visitas'",
         "custom_msg": "El histograma debe tener 8 barras con los 90 días de visitas y el título 'Distribución de visitas'."}),

B("plt-b01", S4, "Interpretar un histograma", 3, ["plt-hist", "viz-interpretar"],
  "Ejecutá mentalmente (o en el ejercicio anterior) el histograma de ventas diarias. Tiene la mayoría de los días entre 1000 y 2000, y **unos pocos días con ventas mucho más altas** (cerca de 3000). **¿Qué conclusiones sacarías y qué investigarías?**",
  model="La mayoría de los días las ventas están en un rango típico, pero hay **algunos días atípicos** con ventas muy superiores. Antes de concluir, investigaría **qué pasó esos días** (promociones, feriados, errores de carga) mirando las fechas concretas (`ventas_diarias.nlargest(3, 'ventas')`). También notaría que esos picos inflan la media: para describir 'un día típico' usaría la mediana. No concluiría nada causal solo con el histograma.",
  checklist=["Describí la zona típica y los valores atípicos", "Propuse investigar qué pasó en esos días (fechas)", "Mencioné que podrían ser errores o eventos especiales", "Mencioné el efecto sobre la media / usar la mediana"],
  hints=["¿Qué representan las barras aisladas a la derecha?", "¿Cómo encontrarías qué días fueron?", "¿Cómo afectan esos días al promedio?"]),

# ======================================================================== S5
P("plt08", S5, ["plt-scatter", "plt-anatomia"],
  ["Dos variables numéricas por día: ¿qué gráfico?", "Cada punto es un día: visitas en X, ventas en Y.", "plt.scatter(x, y) + etiquetas de ejes."],
  "Cada punto representa un día con sus visitas y ventas; la nube muestra si hay relación.",
  "dispersión(visitas, ventas)\neje X 'Visitas'; eje Y 'Ventas'",
  problem="¿Los días con más visitas tienen más ventas? Dibujá cada día como un punto (`visitas` en X, `ventas` en Y) con las etiquetas de eje **\"Visitas\"** y **\"Ventas\"**."),

B("plt-b02", S5, "Correlación no es causalidad", 3, ["plt-scatter", "viz-interpretar"],
  "Tu scatter muestra que los días con más visitas suelen tener más ventas. Alguien concluye: *'Si compramos publicidad para duplicar las visitas, vamos a duplicar las ventas'*. **¿Qué está bien y qué está mal de ese razonamiento?**",
  model="Está bien que hay una **asociación positiva** entre visitas y ventas. Está mal asumir **causalidad** y **proporcionalidad**: puede haber una tercera variable que mueva ambas (fines de semana, temporada, promociones), las visitas compradas pueden ser de menor calidad (convertir menos) y la relación puede no ser lineal. Para saberlo habría que hacer un experimento (por ejemplo, una campaña en un período y comparar) o al menos controlar por otras variables.",
  checklist=["Reconocí que existe una asociación", "Expliqué que correlación no implica causalidad", "Mencioné posibles terceras variables", "Mencioné que duplicar no implica duplicar (proporcionalidad/calidad)", "Propuse cómo comprobarlo (experimento o controles)"],
  hints=["¿Qué otra cosa podría hacer subir visitas y ventas a la vez?", "¿Todas las visitas valen lo mismo?", "¿Cómo podrías probar el efecto de la publicidad?"]),

P("plt09", S5, ["viz-interpretar", "pd-inspeccion"],
  ["Es composición: partes de un total (pocas categorías).", "Primero contá productos por categoría.", "plt.pie(valores, labels=..., autopct='%1.0f%%')."],
  "La torta muestra la proporción de productos de cada categoría. Funciona porque son solo 4 partes; con muchas, mejor barras.",
  "conteo ← cantidad de productos por categoría\ntorta(conteo, etiquetas = categorías, porcentajes)",
  problem="¿Qué proporción del catálogo es de cada `categoria`? Contá los productos por categoría y dibujá una torta con la etiqueta de cada categoría y su porcentaje (`autopct`)."),

# ======================================================================== S7
A("plt-a05", S7, "plt.plot o ax.plot", 2, ["plt-subplots"],
  "Creaste `fig, (ax1, ax2) = plt.subplots(1, 2)` y querés dibujar una línea en el gráfico de la **izquierda**. ¿Qué escribís?",
  [("`ax1.plot(...)`", True, "Dibujás en el eje concreto."), ("`plt.plot(...)`", False, "Dibuja en el último eje activo (el de la derecha)."), ("`fig.plot(...)`", False, "La figura no tiene plot."), ("`plt.subplot(...)`", False, "No.")]),

P("plt10", S7, ["plt-subplots"],
  ["Son dos gráficos en una figura, lado a lado.", "plt.subplots(1, 2) devuelve la figura y dos ejes.", "Dibujá en cada eje con ax.plot / ax.bar."],
  "`plt.subplots(1, 2)` crea una figura con dos ejes; cada gráfico se dibuja con su objeto `ax`.",
  "fig, (ax1, ax2) ← subplots(1 fila, 2 columnas)\nax1: línea de ingresos; ax2: barras de gastos",
  problem="Armá una figura con **2 gráficos lado a lado**: a la izquierda, la evolución de `ingresos` por mes (línea); a la derecha, los `gastos` por mes (barras)."),

F("plt-f01", S7, "La IA arma un mini dashboard", 3, ["plt-subplots", "plt-anatomia"],
  "Pediste a una IA 'un dashboard de 2 gráficos con ventas diarias'. Te dio esto. Ejecutalo y respondé.",
  prompt="Necesito una figura con dos gráficos lado a lado a partir de ventas_diarias: la evolución de las ventas y su distribución. Explicame la estructura figura/ejes.",
  ai_code="fig, axs = plt.subplots(1, 2, figsize=(11, 4))\naxs[0].plot(ventas_diarias['fecha'], ventas_diarias['ventas'])\naxs[0].set_title('Ventas diarias')\naxs[1].hist(ventas_diarias['ventas'], bins=12)\naxs[1].set_title('Distribución de ventas')\nfig.tight_layout()",
  questions=[
      ask("¿Qué es `axs`?", [("Un array con los dos ejes (gráficos) de la figura", True, "axs[0] es el de la izquierda y axs[1] el de la derecha."), ("La figura", False, "La figura es fig."), ("Los datos", False, "No.")]),
      ask("¿Por qué se usa `set_title` en lugar de `plt.title`?", [("Porque se titula cada eje concreto", True, "plt.title titularía solo el eje activo."), ("Porque plt.title no existe", False, "Existe."), ("Es lo mismo", False, "Con varios ejes no es lo mismo.")]),
      ask("¿Qué pregunta responde cada gráfico?", [("Izquierda: evolución en el tiempo; derecha: distribución de valores", True, "Dos preguntas complementarias."), ("Los dos muestran lo mismo", False, "No."), ("Izquierda: relación; derecha: composición", False, "No.")]),
      ask("¿Qué le agregarías para que lo entienda alguien de otra área?", model="Etiquetas de ejes con unidades (por ejemplo 'Ventas ($)' y 'Cantidad de días'), quizá rotar las fechas, y un título general con fig.suptitle que diga qué se concluye (por ejemplo 'Las ventas crecen con picos puntuales')."),
  ],
  hints=["Ejecutalo y relacioná cada línea con lo que se ve.", "Probá cambiar axs[1].set_title por plt.title y observá.", "Pensá qué le falta a cada eje."],
  explain="La estructura figura/ejes permite componer gráficos que responden preguntas distintas sobre los mismos datos.",
  solution="fig, axs = plt.subplots(1, 2, figsize=(11, 4))\naxs[0].plot(ventas_diarias['fecha'], ventas_diarias['ventas'])\naxs[0].set_title('Ventas diarias')\naxs[1].hist(ventas_diarias['ventas'], bins=12)\naxs[1].set_title('Distribución de ventas')\nfig.tight_layout()",
  check={"plot": True, "custom": "len(_fig().axes) == 2 and len(_ax(0).lines) == 1 and len(_ax(1).patches) == 12",
         "custom_msg": "Izquierda: una línea; derecha: un histograma de 12 barras."}),

P("plt11", S7, ["plt-pandas"],
  ["Los datos ya están en un DataFrame.", "Los DataFrames tienen su propio método para graficar.", "df.plot(x=..., y=..., title=...)."],
  "`df.plot` usa matplotlib por debajo y permite graficar columnas directamente indicando x, y y título.",
  "ventas_diarias.plot(x='fecha', y='ventas', title='Ventas diarias')",
  problem="Sin usar `plt.plot`, graficá directamente desde el DataFrame `ventas_diarias` las `ventas` a lo largo de la `fecha`, con el título **\"Ventas diarias\"**."),

# ======================================================================== Proyecto
C("plt-p1", SP, "Fase 1 · Diseñar el dashboard", 3, ["viz-pregunta", "plt-subplots"],
  "**Contexto:** el gerente quiere un dashboard de **4 gráficos** (2×2) para la reunión semanal. Sus preguntas: (1) ¿cómo evolucionan las ventas? (2) ¿cuáles son las ventas típicas y hay días raros? (3) ¿las visitas se traducen en ventas? (4) ¿qué categoría tiene más stock? Asigná un gráfico a cada pregunta.",
  [field("(1) Evolución de ventas", "Línea: fecha en X, ventas en Y.", ["Línea", "Torta", "Histograma", "Scatter"], 0),
   field("(2) Ventas típicas y días raros", "Histograma de ventas.", ["Histograma", "Línea", "Barras por categoría", "Torta"], 0),
   field("(3) Visitas vs ventas", "Dispersión: visitas en X, ventas en Y.", ["Scatter", "Torta", "Línea", "Histograma"], 0),
   field("(4) Stock por categoría", "Barras con el stock total por categoría.", ["Barras", "Línea", "Scatter", "Histograma"], 0),
   field("Elementos comunes", "Un título por gráfico que nombre la pregunta; ejes con unidades; fig.tight_layout() para que no se superpongan."),
  ],
  explain="Un dashboard es un conjunto de preguntas: cada eje responde una. El diseño (pregunta → gráfico) se decide antes del código.",
  hints=["Repasá las 4 preguntas básicas de visualización.", "¿Cuál habla de tiempo, cuál de distribución, cuál de relación y cuál de comparación?", "¿Qué hace falta para que cada gráfico se entienda solo?"],
  pseudo="fig, axs ← subplots(2, 2)\naxs[0,0] línea · axs[0,1] histograma · axs[1,0] scatter · axs[1,1] barras\ntítulos + tight_layout"),

D("plt-p2", SP, "Fase 2 · Construir el dashboard", 4, ["plt-subplots", "plt-line", "plt-hist", "plt-scatter", "plt-bar"],
  "Construí el dashboard 2×2 diseñado: arriba a la izquierda la **línea** de ventas por fecha, arriba a la derecha el **histograma** de ventas, abajo a la izquierda el **scatter** visitas vs ventas y abajo a la derecha las **barras** de stock por categoría. **Cada gráfico con su título.**",
  "fig, axs = plt.subplots(2, 2, figsize=(12, 8))\n",
  "fig, axs = plt.subplots(2, 2, figsize=(12, 8))\naxs[0, 0].plot(ventas_diarias['fecha'], ventas_diarias['ventas'])\naxs[0, 0].set_title('Evolución de ventas')\naxs[0, 1].hist(ventas_diarias['ventas'], bins=12)\naxs[0, 1].set_title('Distribución de ventas')\naxs[1, 0].scatter(ventas_diarias['visitas'], ventas_diarias['ventas'])\naxs[1, 0].set_title('Visitas vs ventas')\nstock_cat = productos.groupby('categoria')['stock'].sum()\naxs[1, 1].bar(stock_cat.index, stock_cat.values)\naxs[1, 1].set_title('Stock por categoría')\nfig.tight_layout()",
  ["Seguí tu diseño eje por eje.", "Con una grilla 2×2, cada eje se accede como axs[fila, columna].", "Usá ax.plot, ax.hist, ax.scatter, ax.bar y ax.set_title en cada uno."],
  "Cada eje de la grilla responde una pregunta. Se dibuja con el objeto ax correspondiente y se titula con set_title.",
  "fig, axs ← subplots(2, 2)\npara cada eje: dibujar su gráfico y ponerle título\ntight_layout",
  check={"plot": True, "custom": "len(_fig().axes) == 4 and len(_ax(0).lines) >= 1 and len(_ax(1).patches) >= 5 and len(_ax(2).collections) >= 1 and len(_ax(3).patches) == 4 and all(_ax(i).get_title() for i in range(4))",
         "custom_msg": "Se esperan 4 ejes: línea (arriba izq.), histograma (arriba der.), scatter (abajo izq.), 4 barras (abajo der.), todos con título."}),

E("plt-p3", SP, "Fase 3 · Todo en el mismo gráfico", 3, ["plt-subplots"],
  "Un compañero armó una versión de 2 gráficos, pero los dos quedaron dibujados en el de la derecha y el de la izquierda está vacío. Corregilo.",
  "fig, axs = plt.subplots(1, 2, figsize=(10, 4))\nplt.plot(meses, ingresos)\nplt.bar(meses, gastos)",
  "fig, axs = plt.subplots(1, 2, figsize=(10, 4))\naxs[0].plot(meses, ingresos)\naxs[1].bar(meses, gastos)",
  detect=("¿Por qué quedó todo a la derecha?", [
      ("plt.plot y plt.bar dibujan en el último eje activo; hay que usar cada ax", True, "Con subplots, dibujá con el objeto de cada eje."),
      ("subplots(1, 2) crea un solo gráfico", False, "Crea dos."),
      ("Falta tight_layout", False, "Eso solo ajusta espacios."),
  ]),
  why="Después de `plt.subplots`, el eje 'activo' es el último creado. `plt.plot` y `plt.bar` dibujan ahí, así que ambos gráficos quedan en el eje derecho. Hay que dibujar explícitamente con `axs[0]` y `axs[1]`.",
  hints=["Mirá el gráfico: ¿qué eje quedó vacío?", "¿En qué eje dibuja plt.plot cuando hay varios?", "Usá axs[0] y axs[1]."],
  pseudo="axs[0]: línea de ingresos\naxs[1]: barras de gastos",
  check={"plot": True, "custom": "len(_fig().axes) == 2 and len(_ax(0).lines) == 1 and len(_ax(1).patches) == 6 and len(_ax(1).lines) == 0",
         "custom_msg": "Izquierda: la línea de ingresos. Derecha: solo las 6 barras de gastos."}),

B("plt-p4", SP, "Fase 4 · Presentar el dashboard", 3, ["viz-interpretar", "viz-pregunta"],
  "Preparate para la reunión: escribí (4-6 líneas) **qué responde cada gráfico del dashboard, cuál es el hallazgo principal y qué NO se puede concluir con estos gráficos.**",
  model="(1) La línea muestra que las ventas crecen a lo largo del período, con picos los fines de semana y tres días excepcionales. (2) El histograma confirma un rango típico y esos pocos días atípicos. (3) El scatter muestra una asociación positiva entre visitas y ventas. (4) Las barras muestran que Accesorios concentra el stock en unidades. Hallazgo principal: crecimiento sostenido con picos puntuales que conviene explicar. No se puede concluir que las visitas **causen** las ventas ni que el stock en unidades refleje el valor del inventario (para eso habría que multiplicar por el precio).",
  checklist=["Expliqué qué pregunta responde cada uno de los 4 gráficos", "Enuncié un hallazgo principal", "Mencioné una conclusión que NO se puede sacar (causalidad, valor vs unidades)", "Usé evidencia visible en los gráficos"],
  hints=["Recorré el dashboard gráfico por gráfico.", "¿Qué patrón aparece en más de un gráfico?", "¿Stock en unidades es lo mismo que dinero inmovilizado?"]),
]

QUIZ = [
Q("q-plt-01", ["viz-pregunta", "plt-bar"], "Querés comparar la facturación de 6 sucursales.",
  [("Barras", True, "Categorías + valor."), ("Línea", False, "No hay tiempo."), ("Histograma", False, "No."), ("Scatter", False, "No.")]),
Q("q-plt-02", ["viz-pregunta", "plt-hist"], "Querés ver si la mayoría de los clientes tiene entre 25 y 40 años.",
  [("Histograma de edades", True, "Distribución."), ("Torta", False, "No."), ("Línea", False, "No."), ("Barras por cliente", False, "Demasiadas barras.")]),
Q("q-plt-03", ["viz-pregunta", "plt-line"], "Querés mostrar la temperatura de un sensor hora a hora durante una semana.",
  [("Línea", True, "Evolución temporal."), ("Torta", False, "No."), ("Histograma", False, "Perdería el orden temporal."), ("Barras horizontales", False, "No.")]),
Q("q-plt-04", ["viz-pregunta", "plt-scatter"], "Querés saber si los productos más caros tienen menos stock.",
  [("Scatter precio vs stock", True, "Relación entre dos numéricas."), ("Torta", False, "No."), ("Línea", False, "No."), ("Histograma de precios", False, "Una sola variable.")]),
Q("q-plt-05", ["plt-subplots"], "Querés mostrar 4 gráficos distintos en una sola imagen para un informe.",
  [("plt.subplots(2, 2) y dibujar en cada ax", True, "Grilla de ejes."), ("4 veces plt.plot", False, "Quedarían superpuestos."), ("Una torta grande", False, "No."), ("plt.legend", False, "No.")]),
Q("q-plt-06", ["plt-anatomia"], "Mostraste un gráfico y te preguntan '¿esto está en pesos o en miles?'.",
  [("Faltan unidades en la etiqueta del eje", True, "ylabel con unidades."), ("Falta la leyenda", False, "No es eso."), ("Hay que cambiar a torta", False, "No."), ("Faltan colores", False, "No.")]),
Q("q-plt-07", ["viz-interpretar"], "Un gráfico de barras muestra una diferencia enorme entre dos valores, pero el eje Y empieza en 950.",
  [("El eje truncado exagera la diferencia", True, "Las barras deberían empezar en 0."), ("Está perfecto", False, "Puede engañar."), ("Hay que usar torta", False, "No."), ("Falta leyenda", False, "No es el problema.")]),
Q("q-plt-08", ["plt-pandas"], "Tenés un groupby por mes ya calculado y querés verlo rápido como barras.",
  [("serie.plot(kind='bar')", True, "pandas grafica directo."), ("Recalcular en un for", False, "No."), ("plt.pie", False, "No."), ("to_csv", False, "No.")]),
]

PROJECT = project(
    "Dashboard básico de ventas",
    "El gerente quiere una sola imagen para la reunión semanal que responda 4 preguntas sobre ventas, visitas y stock.",
    "Un dashboard 2×2 donde cada gráfico responde una pregunta y una presentación oral breve.",
    [("Diseñar", "Pregunta → gráfico para cada panel.", ["plt-p1"]),
     ("Construir", "Grilla 2×2 con títulos.", ["plt-p2"]),
     ("Verificar", "Corregí un error de ejes.", ["plt-p3"]),
     ("Presentar", "Hallazgos y límites.", ["plt-p4"])],
    ["Diseño pregunta → gráfico", "Dashboard 2×2 con títulos", "Interpretación con límites"],
    ["La IA puede ayudarte con estilo y sintaxis de subplots; el diseño pregunta → gráfico es tuyo.",
     "Revisá que cada gráfico se entienda sin explicación.",
     "Rehacé un panel sin ayuda al final."],
)

MODULE = module(
    "m04", "04", "Matplotlib", "📈", "#fb923c",
    "Visualización con criterio: qué gráfico responde cada pregunta, cómo hacerlo legible y cómo interpretarlo sin engañar.",
    learn=["Elegir el gráfico según la pregunta: evolución, comparación, distribución o relación",
           "Hacer gráficos legibles: títulos, ejes con unidades, leyendas",
           "Componer varios gráficos en un dashboard con figura y ejes",
           "Interpretar gráficos y detectar conclusiones inválidas"],
    why="Un gráfico es una **respuesta visual a una pregunta**. La sintaxis de matplotlib se olvida y se busca; lo que no se puede delegar es decidir *qué* gráfico responde *qué* pregunta y *qué* se puede concluir de él.",
    ai="Describí la pregunta y el tipo de datos, y pedile a la IA que justifique el gráfico que propone. Pedile ayuda con estilo y subplots. Pero la interpretación es tuya: no aceptes conclusiones causales a partir de un scatter.",
    concepts=CONCEPTS, exercises=EXERCISES, quiz=QUIZ, project=PROJECT,
    setup=SETUP + PLT_SETUP, packages=["matplotlib"], tables=["meses", "ingresos", "gastos", "productos", "ventas_diarias"], file="graficos.py",
)
