# -*- coding: utf-8 -*-
"""Módulo 05 · Seaborn. Los checks combinan el código usado (_pq_code) con la figura resultante."""

DIAS = "['Jue', 'Vie', 'Sáb', 'Dom']"


def chk(expr, msg):
    return {"plot": True, "custom": expr, "custom_msg": msg}


EXERCISES = [
# =========================================================== Distribuciones
dict(id="sns01", sec="Distribuciones", title="Hola, seaborn", level=1,
theory="""**Seaborn** está construida sobre matplotlib y está pensada para **gráficos estadísticos**: con una sola línea obtienes gráficos bonitos que entienden DataFrames directamente.

```python
import seaborn as sns
sns.histplot(data=df, x="columna")
```

El patrón es siempre el mismo:
- `data=`: el DataFrame;
- `x=` / `y=`: los **nombres** de las columnas (como texto);
- `hue=`: una columna para **colorear por grupos** (lo verás enseguida).

En este módulo tienes el dataset `propinas`: las cuentas de un restaurante, con `cuenta`, `propina`, `dia`, `momento` (Almuerzo/Cena), `fumador` y `personas`.

> 💡 Como seaborn dibuja con matplotlib, puedes seguir usando `plt.title()`, `plt.xlabel()`…""",
task="Dibuja un histograma de la columna `cuenta` de `propinas` con `sns.histplot`.",
starter="# sns y plt ya están importados\n",
solution="sns.histplot(data=propinas, x='cuenta')",
hint="sns.histplot(data=propinas, x='cuenta')",
check=chk("'histplot' in _pq_code and len(_ax().patches) > 0", "Usa sns.histplot con la columna 'cuenta'.")),

dict(id="sns02", sec="Distribuciones", title="Histograma con curva de densidad", level=2,
theory="""`histplot` tiene parámetros muy útiles:

- `bins=`: cantidad de barras;
- `kde=True`: añade una **curva de densidad** suavizada, que muestra la forma de la distribución;
- `stat="percent"`: muestra porcentajes en lugar de conteos.

```python
sns.histplot(data=df, x="edad", bins=20, kde=True)
```

> 💼 **En el trabajo:** antes de modelar, se mira la distribución de cada variable. Una variable muy **asimétrica** (con cola larga, como los salarios) a veces se transforma con un logaritmo.""",
task="Dibuja el histograma de `propina` con **15 bins** y la curva de densidad (`kde=True`).",
starter="sns.histplot(data=propinas, x='propina')",
solution="sns.histplot(data=propinas, x='propina', bins=15, kde=True)",
hint="bins=15, kde=True",
check=chk("len(_ax().patches) == 15 and len(_ax().lines) >= 1", "Deben verse 15 barras y la curva KDE.")),

dict(id="sns03", sec="Distribuciones", title="Comparar distribuciones con hue", level=2,
theory="""El parámetro **`hue`** colorea según una columna categórica y dibuja **un grupo por color**, con su leyenda automática. Es la superpotencia de seaborn.

`kdeplot` dibuja solo la curva de densidad, así que es ideal para **superponer grupos** sin que las barras se tapen:

```python
sns.kdeplot(data=df, x="salario", hue="genero", fill=True)
```

`fill=True` rellena el área bajo cada curva.""",
task="Compara la distribución de `cuenta` entre **Almuerzo** y **Cena**: usa `sns.kdeplot` con `hue='momento'` y `fill=True`.",
starter="",
solution="sns.kdeplot(data=propinas, x='cuenta', hue='momento', fill=True)",
hint="sns.kdeplot(data=propinas, x='cuenta', hue='momento', fill=True)",
check=chk("'kdeplot' in _pq_code and sorted(_legend()) == ['Almuerzo', 'Cena']",
          "Usa sns.kdeplot con hue='momento' (la leyenda debe mostrar Almuerzo y Cena).")),

# =========================================================== Relaciones
dict(id="sns04", sec="Relaciones", title="Dispersión con colores", level=2,
theory="""`sns.scatterplot` es el gráfico de dispersión de seaborn. Con `hue` coloreas los puntos por grupo y con `size` puedes hacer que su tamaño dependa de otra variable:

```python
sns.scatterplot(data=df, x="m2", y="precio", hue="barrio")
```

De un vistazo ves si la relación entre X e Y cambia según el grupo.""",
task="Dibuja un scatter de `propinas` con `cuenta` en X, `propina` en Y y el color según `momento`.",
starter="",
solution="sns.scatterplot(data=propinas, x='cuenta', y='propina', hue='momento')",
hint="sns.scatterplot(data=propinas, x='cuenta', y='propina', hue='momento')",
check=chk("'scatterplot' in _pq_code and sum(len(c.get_offsets()) for c in _ax().collections) == 120 and {'Almuerzo', 'Cena'} <= set(_legend())",
          "Deben verse los 120 puntos, coloreados por 'momento'.")),

dict(id="sns05", sec="Relaciones", title="Línea de tendencia", level=3,
theory="""`sns.regplot` dibuja los puntos **y una recta de regresión** que resume la tendencia. La franja sombreada es el **intervalo de confianza**: cuanto más estrecha, más segura es la tendencia.

```python
sns.regplot(data=df, x="horas_estudio", y="nota")
```

Es tu primer contacto con un **modelo**: la recta que mejor se ajusta a los puntos. En el módulo de Machine Learning la calcularás tú mismo con scikit-learn.""",
task="Dibuja la relación entre `cuenta` (X) y `propina` (Y) con su recta de tendencia, usando `sns.regplot`.",
starter="",
solution="sns.regplot(data=propinas, x='cuenta', y='propina')",
hint="sns.regplot(data=propinas, x='cuenta', y='propina')",
check=chk("'regplot' in _pq_code and len(_ax().lines) >= 1 and len(_ax().collections) >= 1",
          "Usa sns.regplot con cuenta en X y propina en Y.")),

dict(id="sns06", sec="Relaciones", title="Tendencias en el tiempo", level=2,
theory="""`sns.lineplot` dibuja series temporales y, si hay varias observaciones por punto, calcula la media y su intervalo automáticamente.

Con `sns.set_theme(style=...)` cambias el estilo de **todos** los gráficos siguientes: `"whitegrid"`, `"darkgrid"`, `"white"`, `"ticks"`.

```python
sns.set_theme(style="whitegrid")
sns.lineplot(data=df, x="fecha", y="ventas")
plt.xticks(rotation=45)
```""",
task="Aplica el estilo **\"whitegrid\"**, dibuja con `sns.lineplot` las `ventas` por `fecha` de `ventas_diarias` y pon el título **\"Tendencia de ventas\"**.",
starter="",
solution="sns.set_theme(style='whitegrid')\nsns.lineplot(data=ventas_diarias, x='fecha', y='ventas')\nplt.title('Tendencia de ventas')\nplt.xticks(rotation=45)",
hint="sns.set_theme(style='whitegrid'); sns.lineplot(...); plt.title('...')",
check=chk("'lineplot' in _pq_code and 'whitegrid' in _pq_code and len(_ax().lines) >= 1 and _ax().get_title() == 'Tendencia de ventas'",
          "Usa set_theme(style='whitegrid'), sns.lineplot y el título 'Tendencia de ventas'.")),

# =========================================================== Categorías
dict(id="sns07", sec="Comparar categorías", title="Boxplot", level=2,
theory="""El **boxplot** (diagrama de caja) resume una distribución en 5 números:

- la **línea central** es la mediana;
- la **caja** va del percentil 25 al 75 (ahí está el 50% central de los datos);
- los **bigotes** llegan hasta los valores "normales";
- los **puntos sueltos** son **outliers** (valores atípicos).

```python
sns.boxplot(data=df, x="categoria", y="precio", order=["A", "B", "C"])
```

`order=` fija el orden de las categorías en el eje.

> 💼 **En el trabajo:** comparar sueldos por departamento o tiempos de entrega por proveedor, y detectar outliers de un vistazo.""",
task=f"Dibuja un boxplot de `propina` por `dia`, con los días en el orden `{DIAS}`.",
starter="",
solution=f"sns.boxplot(data=propinas, x='dia', y='propina', order={DIAS})",
hint=f"sns.boxplot(data=propinas, x='dia', y='propina', order={DIAS})",
check=chk(f"'boxplot' in _pq_code and _xticks() == {DIAS}",
          "Usa sns.boxplot con x='dia', y='propina' y el orden de días indicado.")),

dict(id="sns08", sec="Comparar categorías", title="Barras con promedios", level=3,
theory="""`sns.barplot` **calcula por ti** la media de `y` para cada categoría de `x` (no cuenta filas: promedia).

```python
sns.barplot(data=df, x="region", y="ventas", errorbar=None)
```

Por defecto dibuja una **barra de error** (el intervalo de confianza de la media); con `errorbar=None` la quitas. Con `estimator="sum"` suma en vez de promediar.

> ⚠️ No lo confundas con `countplot`, que **cuenta filas** (lo verás en el siguiente ejercicio).""",
task=f"Dibuja un barplot con la **propina media** por `dia` (orden `{DIAS}`) y sin barras de error.",
starter="",
solution=f"sns.barplot(data=propinas, x='dia', y='propina', order={DIAS}, errorbar=None)",
hint=f"sns.barplot(data=propinas, x='dia', y='propina', order={DIAS}, errorbar=None)",
check=chk(f"'barplot' in _pq_code and len(_ax().patches) == 4 and np.allclose(_heights(), propinas.groupby('dia')['propina'].mean().reindex({DIAS}).values)",
          "Deben verse 4 barras con la propina media de cada día, en el orden pedido.")),

dict(id="sns09", sec="Comparar categorías", title="Contar categorías", level=1,
theory="""`sns.countplot` dibuja una barra por categoría con **cuántas filas** tiene cada una. Es la versión gráfica de `value_counts()`.

```python
sns.countplot(data=df, x="metodo_pago")
```

Con `hue` puedes partir cada barra por otra variable, por ejemplo `hue="fumador"`.""",
task="Dibuja con `sns.countplot` cuántas cuentas hay de cada `momento` (Almuerzo/Cena).",
starter="",
solution="sns.countplot(data=propinas, x='momento')",
hint="sns.countplot(data=propinas, x='momento')",
check=chk("'countplot' in _pq_code and len(_ax().patches) == 2 and sum(_heights()) == 120",
          "Usa sns.countplot con x='momento' (2 barras que sumen 120).")),

dict(id="sns10", sec="Comparar categorías", title="Dos variables categóricas", level=3,
theory="""Combinando `x` y `hue` en un mismo gráfico comparas **dos variables categóricas a la vez**. Por ejemplo, un boxplot por día que además separa fumadores y no fumadores:

```python
sns.boxplot(data=df, x="dia", y="propina", hue="fumador")
plt.title("...")
```

Cada día tendrá **dos cajas**, una por grupo, y la leyenda indica cuál es cuál.""",
task=f"Dibuja un boxplot de `propina` por `dia` (orden `{DIAS}`), separado por `fumador` con `hue`, y pon el título **\"Propinas por día y fumador\"**.",
starter="",
solution=f"sns.boxplot(data=propinas, x='dia', y='propina', hue='fumador', order={DIAS})\nplt.title('Propinas por día y fumador')",
hint="sns.boxplot(..., hue='fumador') + plt.title('Propinas por día y fumador')",
check=chk(f"'boxplot' in _pq_code and _xticks() == {DIAS} and sorted(_legend()) == ['No', 'Sí'] and _ax().get_title() == 'Propinas por día y fumador'",
          "Boxplot por día (orden pedido), hue='fumador' y el título exacto.")),

# =========================================================== Correlación
dict(id="sns11", sec="Correlación", title="Mapa de calor de correlaciones", level=3,
theory="""La **correlación** mide de -1 a 1 cuánto se mueven juntas dos variables numéricas:
- **1**: suben juntas perfectamente;
- **0**: no hay relación lineal;
- **-1**: cuando una sube, la otra baja.

`df.corr()` calcula la **matriz de correlación** y `sns.heatmap` la pinta con colores. Con `annot=True` escribe el valor en cada celda:

```python
corr = df[["a", "b", "c"]].corr()
sns.heatmap(corr, annot=True, cmap="coolwarm")
```

> 💼 **En el trabajo:** antes de entrenar un modelo, el heatmap de correlaciones muestra qué variables tienen relación con lo que quieres predecir.

> ⚠️ Correlación **no implica** causalidad.""",
task="Calcula la correlación entre `cuenta`, `propina` y `personas` y dibújala con `sns.heatmap`, con los valores escritos (`annot=True`) y el mapa de colores `\"coolwarm\"`.",
starter="corr = \n",
solution="corr = propinas[['cuenta', 'propina', 'personas']].corr()\nsns.heatmap(corr, annot=True, cmap='coolwarm')",
hint="corr = propinas[['cuenta', 'propina', 'personas']].corr(); sns.heatmap(corr, annot=True, cmap='coolwarm')",
check=chk("'heatmap' in _pq_code and 'coolwarm' in _pq_code and len(_ax().texts) == 9",
          "El heatmap debe ser de 3x3, con annot=True y cmap='coolwarm'.")),
]
