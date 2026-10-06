# -*- coding: utf-8 -*-
"""Módulo 04 · Matplotlib. Los checks inspeccionan la figura con los helpers de pq_core (_ax, _fig, _legend...)."""

P = {"plot": True}


def chk(expr, msg):
    return dict(P, custom=expr, custom_msg=msg)


EXERCISES = [
# =========================================================== Primeros gráficos
dict(id="plt01", sec="Primeros gráficos", title="Tu primer gráfico", level=1,
theory="""**Matplotlib** es la librería de gráficos más usada de Python y la base de otras como seaborn o el `.plot()` de pandas. Su módulo principal se importa así:

```python
import matplotlib.pyplot as plt
```

El gráfico más básico es el de **líneas**: `plt.plot(x, y)` une los puntos con una línea. Es ideal para ver cómo **evoluciona** algo en el tiempo.

```python
plt.plot([1, 2, 3], [10, 30, 20])
```

En este módulo tienes cargadas las listas `meses`, `ingresos` y `gastos` (en miles), además de las tablas del curso.

> 💡 En Colab/Jupyter el gráfico aparece solo al final de la celda. En un script de Python hace falta `plt.show()`.""",
task="Dibuja un gráfico de líneas con `meses` en el eje X e `ingresos` en el eje Y.",
starter="# plt ya está importado\n",
solution="plt.plot(meses, ingresos)",
hint="plt.plot(meses, ingresos)",
check=chk("len(_ax().lines) == 1 and list(_ax().lines[0].get_ydata()) == ingresos",
          "Debe haber una línea con los valores de `ingresos` en el eje Y.")),

dict(id="plt02", sec="Primeros gráficos", title="Título y etiquetas", level=1,
theory="""Un gráfico sin título ni etiquetas **no comunica**: quien lo mire no sabrá qué representa. Siempre añade:

```python
plt.title("Ventas 2024")
plt.xlabel("Mes")
plt.ylabel("Unidades vendidas")
```

> 💼 **En el trabajo:** un gráfico en una presentación debe entenderse **en 5 segundos** sin que nadie lo explique. Título claro, ejes con nombre y unidades.""",
task="Dibuja `ingresos` por mes y añade el título **\"Ingresos por mes\"**, la etiqueta X **\"Mes\"** y la etiqueta Y **\"Ingresos (miles)\"** (escríbelos exactamente así).",
starter="plt.plot(meses, ingresos)\n# añade título y etiquetas\n",
solution="plt.plot(meses, ingresos)\nplt.title('Ingresos por mes')\nplt.xlabel('Mes')\nplt.ylabel('Ingresos (miles)')",
hint="plt.title('...'), plt.xlabel('...'), plt.ylabel('...')",
check=chk("len(_ax().lines) == 1 and _ax().get_title() == 'Ingresos por mes' and _ax().get_xlabel() == 'Mes' and _ax().get_ylabel() == 'Ingresos (miles)'",
          "Revisa que el título y las etiquetas estén escritos exactamente como se pide.")),

dict(id="plt03", sec="Primeros gráficos", title="Comparar con leyenda", level=2,
theory="""Puedes dibujar **varias líneas** en el mismo gráfico llamando a `plt.plot` varias veces. Para distinguirlas, pon a cada una un `label` y llama a `plt.legend()`:

```python
plt.plot(x, ventas_2023, label="2023")
plt.plot(x, ventas_2024, label="2024")
plt.legend()
```

Matplotlib asigna un color distinto a cada línea automáticamente.""",
task="Dibuja `ingresos` y `gastos` por mes en el mismo gráfico, con las etiquetas **\"Ingresos\"** y **\"Gastos\"**, y muestra la leyenda.",
starter="",
solution="plt.plot(meses, ingresos, label='Ingresos')\nplt.plot(meses, gastos, label='Gastos')\nplt.legend()",
hint="Dos plt.plot(..., label='...') y luego plt.legend()",
check=chk("len(_ax().lines) == 2 and sorted(_legend()) == ['Gastos', 'Ingresos']",
          "Deben verse 2 líneas y una leyenda con 'Ingresos' y 'Gastos'.")),

dict(id="plt04", sec="Primeros gráficos", title="Dale estilo", level=2,
theory="""`plt.plot` acepta parámetros de estilo:

| Parámetro | Ejemplos |
|---|---|
| `color` | `"red"`, `"green"`, `"#ff5733"` |
| `marker` | `"o"` (círculo), `"s"` (cuadrado), `"^"` (triángulo) |
| `linestyle` | `"-"` (sólida), `"--"` (guiones), `":"` (puntos) |
| `linewidth` | `2`, `3`… |

```python
plt.plot(x, y, color="purple", marker="s", linestyle=":")
```

> 💡 Los marcadores ayudan cuando hay pocos puntos: así se ve dónde está cada dato real.""",
task="Dibuja `ingresos` por mes en color **\"green\"**, con marcador **\"o\"** y línea de guiones **\"--\"**.",
starter="plt.plot(meses, ingresos)",
solution="plt.plot(meses, ingresos, color='green', marker='o', linestyle='--')",
hint="color='green', marker='o', linestyle='--'",
check=chk("len(_ax().lines) == 1 and _hex(_ax().lines[0].get_color()) == '#008000' and _ax().lines[0].get_marker() == 'o' and _ax().lines[0].get_linestyle() == '--'",
          "La línea debe ser verde ('green'), con marcador 'o' y estilo '--'.")),

# =========================================================== Tipos de gráfico
dict(id="plt05", sec="Tipos de gráfico", title="Gráfico de barras", level=1,
theory="""Las **barras** sirven para **comparar cantidades entre categorías** (productos, países, vendedores…):

```python
plt.bar(categorias, valores)
```

Si los nombres son largos y se superponen, gíralos:

```python
plt.xticks(rotation=45)
```

> 💡 **¿Líneas o barras?** Líneas para tendencias en el tiempo; barras para comparar categorías.""",
task="Dibuja un gráfico de barras con el `stock` de cada `producto` de la tabla `productos`.",
starter="",
solution="plt.bar(productos['producto'], productos['stock'])\nplt.xticks(rotation=45)",
hint="plt.bar(productos['producto'], productos['stock'])",
check=chk("len(_ax().patches) == 10 and _heights() == productos['stock'].tolist()",
          "Debe haber 10 barras con el stock de cada producto, en el orden de la tabla.")),

dict(id="plt06", sec="Tipos de gráfico", title="Barras horizontales: un top 5", level=2,
theory="""`plt.barh(categorias, valores)` dibuja **barras horizontales**. Son ideales para los rankings, porque los nombres se leen cómodamente.

Lo habitual es preparar los datos primero con pandas y después graficar:

```python
top = df.nlargest(5, "ventas")
plt.barh(top["vendedor"], top["ventas"])
```

> 💼 **En el trabajo:** "Top 10 productos", "Top 5 clientes"… los gráficos de ranking están en todos los dashboards.""",
task="Obtén los **5 productos más caros** con `nlargest` y dibújalos con barras horizontales (`producto` y `precio`).",
starter="top = \n",
solution="top = productos.nlargest(5, 'precio')\nplt.barh(top['producto'], top['precio'])",
hint="top = productos.nlargest(5, 'precio'); plt.barh(top['producto'], top['precio'])",
check=chk("len(_ax().patches) == 5 and sorted(_widths()) == sorted(productos.nlargest(5, 'precio')['precio'].tolist())",
          "Debe haber 5 barras horizontales con los precios de los 5 productos más caros.")),

dict(id="plt07", sec="Tipos de gráfico", title="Histograma", level=2,
theory="""Un **histograma** muestra la **distribución** de una variable numérica: divide el rango en intervalos (*bins*) y cuenta cuántos valores caen en cada uno.

```python
plt.hist(datos, bins=20, edgecolor="black")
```

Con él respondes preguntas como: ¿los valores se concentran en el centro? ¿hay valores extremos? ¿la distribución es simétrica?

> ⚠️ El número de `bins` cambia mucho la lectura: con pocos se pierde detalle y con demasiados aparece ruido. Prueba varios.""",
task="Dibuja un histograma de la columna `ventas` de `ventas_diarias` con **12 bins**.",
starter="",
solution="plt.hist(ventas_diarias['ventas'], bins=12, edgecolor='black')",
hint="plt.hist(ventas_diarias['ventas'], bins=12)",
check=chk("len(_ax().patches) == 12 and sum(_heights()) == 90",
          "El histograma debe tener 12 barras con los 90 días de ventas.")),

dict(id="plt08", sec="Tipos de gráfico", title="Dispersión: ¿hay relación?", level=2,
theory="""El gráfico de **dispersión** (*scatter*) pone un punto por cada observación, con una variable en cada eje. Sirve para ver si dos variables están **relacionadas**:

- los puntos suben juntos: relación **positiva**;
- uno sube y el otro baja: relación **negativa**;
- nube sin forma: **no hay relación**.

```python
plt.scatter(df["publicidad"], df["ventas"], alpha=0.6)
```

`alpha` añade transparencia, que viene bien cuando hay muchos puntos superpuestos.""",
task="Dibuja un gráfico de dispersión de `ventas_diarias` con `visitas` en X y `ventas` en Y. Pon las etiquetas de eje **\"Visitas\"** y **\"Ventas\"**.",
starter="",
solution="plt.scatter(ventas_diarias['visitas'], ventas_diarias['ventas'])\nplt.xlabel('Visitas')\nplt.ylabel('Ventas')",
hint="plt.scatter(x, y) + plt.xlabel / plt.ylabel",
check=chk("len(_ax().collections) == 1 and len(_ax().collections[0].get_offsets()) == 90 and _ax().get_xlabel() == 'Visitas' and _ax().get_ylabel() == 'Ventas'",
          "Debe haber un scatter con los 90 días y las etiquetas 'Visitas' y 'Ventas'.")),

dict(id="plt09", sec="Tipos de gráfico", title="Gráfico de torta", level=2,
theory="""El gráfico de **torta** (*pie*) muestra **proporciones de un total**. `autopct` escribe el porcentaje dentro de cada porción:

```python
plt.pie(valores, labels=nombres, autopct="%1.0f%%")
```

El formato `"%1.0f%%"` significa: número sin decimales seguido del símbolo `%`.

> ⚠️ Úsalo solo con **pocas categorías** (hasta unas 5). Con más, un gráfico de barras se lee mucho mejor.""",
task="Cuenta cuántos productos hay por `categoria` (con `value_counts`) y dibuja una torta con las etiquetas de cada categoría y los porcentajes (`autopct`).",
starter="conteo = productos['categoria'].value_counts()\n",
solution="conteo = productos['categoria'].value_counts()\nplt.pie(conteo, labels=conteo.index, autopct='%1.0f%%')",
hint="plt.pie(conteo, labels=conteo.index, autopct='%1.0f%%')",
check=chk("len(_ax().patches) == 4 and len(_ax().texts) == 8",
          "La torta debe tener 4 porciones, con su etiqueta y su porcentaje cada una (usa labels y autopct).")),

# =========================================================== Composición
dict(id="plt10", sec="Composición y pandas", title="Varios gráficos juntos", level=3,
theory="""Hasta ahora usaste la interfaz rápida (`plt.plot`). Para gráficos más complejos se usa la **interfaz orientada a objetos**, con una **figura** (`fig`) que contiene varios **ejes** (`ax`):

```python
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))   # 1 fila, 2 columnas
ax1.plot(x, y)
ax1.set_title("Evolución")
ax2.bar(cats, vals)
ax2.set_title("Comparación")
```

Fíjate en que con ejes se usa `ax.set_title()` en lugar de `plt.title()`.

> 💼 **En el trabajo:** los informes suelen tener varios gráficos lado a lado. `plt.subplots` es la forma profesional de montarlos.""",
task="Crea una figura con **2 gráficos lado a lado**: a la izquierda, una línea de `ingresos` por mes; a la derecha, barras de `gastos` por mes.",
starter="fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))\n",
solution="fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))\nax1.plot(meses, ingresos)\nax2.bar(meses, gastos)",
hint="ax1.plot(meses, ingresos) y ax2.bar(meses, gastos)",
check=chk("len(_fig().axes) == 2 and len(_ax(0).lines) == 1 and len(_ax(1).patches) == 6",
          "Izquierda: una línea con ingresos. Derecha: 6 barras con gastos.")),

dict(id="plt11", sec="Composición y pandas", title="Graficar directo desde pandas", level=2,
theory="""Los DataFrames tienen el método **`.plot()`**, que usa matplotlib por debajo. Es la forma más rápida de graficar datos que ya están en una tabla:

```python
df.plot(x="fecha", y="ventas")                  # líneas
df.plot(x="producto", y="precio", kind="bar")   # barras
df["edad"].plot(kind="hist", bins=10)           # histograma
```

También acepta `title=`, `figsize=`, `color=`…

> 💼 **En el trabajo:** para explorar datos, `df.plot()` es lo más cómodo. Para un gráfico final pulido, matplotlib o seaborn.""",
task="Con `ventas_diarias.plot`, dibuja las `ventas` a lo largo de la `fecha` con el título **\"Ventas diarias\"**.",
starter="",
solution="ventas_diarias.plot(x='fecha', y='ventas', title='Ventas diarias')",
hint="ventas_diarias.plot(x='fecha', y='ventas', title='Ventas diarias')",
check=chk("len(_ax().lines) >= 1 and len(_ax().lines[0].get_ydata()) == 90 and _ax().get_title() == 'Ventas diarias'",
          "Debe verse una línea con los 90 días y el título 'Ventas diarias'.")),
]
