# -*- coding: utf-8 -*-
"""Módulo 02 · DataFrames: seleccionar, filtrar, transformar, limpiar, agrupar, unir, reestructurar y SQL."""

EXERCISES = [
# =========================================================== Seleccionar
dict(id="df01", sec="Seleccionar datos", title="Una o varias columnas", level=1,
theory="""Seleccionar columnas es el `SELECT` de pandas:

- `df["col"]` devuelve **una Series** (una sola columna).
- `df[["col1", "col2"]]` devuelve **un DataFrame** con esas columnas, en ese orden.

Fíjate en el **doble corchete** del segundo caso: el de fuera significa "selecciona" y el de dentro es una **lista** de nombres.

```python
productos["precio"]                  # Series
productos[["producto", "precio"]]    # DataFrame con 2 columnas
```

> ⚠️ **Error común:** escribir `df["a", "b"]` con un solo corchete. pandas buscará una columna llamada `("a", "b")` y dará `KeyError`.""",
task="Guarda en `resultado` un DataFrame con las columnas `nombre` y `ciudad` de `clientes`, en ese orden.",
starter="resultado = ",
solution="resultado = clientes[['nombre', 'ciudad']]",
hint="Doble corchete: clientes[['nombre', 'ciudad']]",
sql="SELECT nombre, ciudad FROM clientes;"),

dict(id="df02", sec="Seleccionar datos", title="loc: filas y columnas por etiqueta", level=2,
theory="""`df.loc[filas, columnas]` selecciona filas y columnas a la vez usando sus **etiquetas** (los valores del índice y los nombres de columna).

```python
df.loc[0]                          # la fila con etiqueta 0
df.loc[0:2, ["a", "b"]]            # filas 0 a 2, columnas a y b
df.loc[:, "precio"]                # todas las filas, columna precio
```

> ⚠️ **Muy importante:** con `loc`, los rangos **incluyen el final**. `loc[0:2]` trae las filas 0, 1 **y 2**. Esto es distinto de las listas de Python y de `iloc`.""",
task="Con `loc`, toma de `productos` las filas con índice **2 a 4 (incluido)** y solo las columnas `producto` y `precio`.",
starter="resultado = productos.loc[   ]",
solution="resultado = productos.loc[2:4, ['producto', 'precio']]",
hint="productos.loc[2:4, ['producto', 'precio']]",
sql="SELECT producto, precio FROM productos LIMIT 3 OFFSET 2;"),

dict(id="df03", sec="Seleccionar datos", title="iloc: filas por posición", level=2,
theory="""`df.iloc[...]` selecciona por **posición numérica**, como las listas de Python: empieza en 0, el final del rango **no se incluye** y acepta números negativos.

```python
df.iloc[0]         # primera fila
df.iloc[:5]        # primeras 5 filas
df.iloc[-1]        # última fila
df.iloc[:, 0]      # primera columna
```

> 💡 Regla para recordarlo: **l**oc = **l**abel (etiqueta) e **i**loc = **i**nteger (posición).""",
task="Guarda en `resultado` las **3 últimas filas** de `clientes` usando `iloc`.",
starter="resultado = ",
solution="resultado = clientes.iloc[-3:]",
hint="clientes.iloc[-3:]",
sql="SELECT * FROM clientes ORDER BY cliente_id DESC LIMIT 3;"),

dict(id="df04", sec="Seleccionar datos", title="Buscar un valor concreto", level=2,
theory="""`set_index("col")` convierte una columna en el índice de la tabla. Así puedes buscar filas por un valor con sentido (un nombre o un código) en vez de por un número:

```python
por_nombre = clientes.set_index("nombre")
por_nombre.loc["Ana", "edad"]      # 34
```

Para leer un único valor también existe `.at[fila, columna]`, que es más rápido.

> 💡 `set_index` **no modifica** la tabla original: devuelve una nueva.""",
task="¿Cuál es el `precio` del producto **Monitor**? Guarda el número en `resultado`.",
starter="resultado = ",
solution="resultado = productos.set_index('producto').loc['Monitor', 'precio']",
hint="productos.set_index('producto').loc['Monitor', 'precio']",
sql="SELECT precio FROM productos WHERE producto = 'Monitor';"),

# =========================================================== Filtrar
dict(id="df05", sec="Filtrar filas", title="Una condición", level=1,
theory="""Filtrar filas es el `WHERE` de pandas y funciona igual que con las Series:

1. Creas una **máscara booleana** comparando una columna: `clientes["edad"] > 40`.
2. La pasas entre corchetes: `clientes[máscara]`.

```python
caros = productos[productos["precio"] > 200]
```

Se leería así: *"de productos, dame las filas donde precio > 200"*.""",
task="Guarda en `resultado` los clientes con `edad` **mayor que 40**.",
starter="resultado = ",
solution="resultado = clientes[clientes['edad'] > 40]",
hint="clientes[clientes['edad'] > 40]",
sql="SELECT * FROM clientes WHERE edad > 40;"),

dict(id="df06", sec="Filtrar filas", title="Combinar condiciones", level=2,
theory="""Para combinar condiciones, pandas usa operadores especiales:

| pandas | significa | SQL |
|---|---|---|
| `&` | y | AND |
| `\\|` | o | OR |
| `~` | no | NOT |

Y la regla de oro: **cada condición va entre paréntesis**.

```python
df[(df["precio"] > 100) & (df["stock"] > 0)]
```

> ⚠️ **Error número uno de quien empieza:** usar `and`/`or` de Python o quitar los paréntesis. Da el error *"The truth value of a Series is ambiguous"*.""",
task="Guarda los clientes de **España** con segmento **Premium**.",
starter="resultado = ",
solution="resultado = clientes[(clientes['pais'] == 'España') & (clientes['segmento'] == 'Premium')]",
hint="(cond1) & (cond2), cada una entre paréntesis",
sql="SELECT * FROM clientes WHERE pais = 'España' AND segmento = 'Premium';"),

dict(id="df07", sec="Filtrar filas", title="Varios valores con isin", level=2,
theory="""Si quieres las filas cuyo valor esté **dentro de una lista**, usa `.isin([...])`. Es el `IN` de SQL y queda mucho más limpio que encadenar varios `|`.

```python
clientes[clientes["pais"].isin(["Chile", "Perú"])]
```

Para lo contrario ("que **no** esté en la lista") se antepone `~`:

```python
clientes[~clientes["pais"].isin(["Chile", "Perú"])]
```""",
task="Guarda los pedidos cuyo `estado` sea **enviado** o **pendiente**.",
starter="resultado = ",
solution="resultado = pedidos[pedidos['estado'].isin(['enviado', 'pendiente'])]",
hint="pedidos['estado'].isin(['enviado', 'pendiente'])",
sql="SELECT * FROM pedidos WHERE estado IN ('enviado', 'pendiente');"),

dict(id="df08", sec="Filtrar filas", title="query(): filtros legibles", level=2,
theory="""`df.query("condición")` permite escribir el filtro como un **texto**, casi como en SQL. Se usa `and`/`or` y los nombres de columna van **sin comillas**; los textos sí van entre comillas.

```python
df.query("edad >= 18 and pais == 'Chile'")
```

Para usar una variable de Python dentro de la consulta, se antepone `@`:

```python
minimo = 100
df.query("precio > @minimo")
```

> 💼 **En el trabajo:** con filtros largos, `query` hace el código mucho más fácil de leer.""",
task="Usando `query`, guarda los productos con `precio` **menor que 100** y `stock` **mayor que 0**.",
starter="resultado = productos.query(\"\")",
solution="resultado = productos.query('precio < 100 and stock > 0')",
hint="productos.query('precio < 100 and stock > 0')",
sql="SELECT * FROM productos WHERE precio < 100 AND stock > 0;"),

dict(id="df09", sec="Filtrar filas", title="Filas con datos faltantes", level=2,
theory="""Para filtrar por nulos se usan `isna()` y `notna()` sobre la columna:

```python
clientes[clientes["email"].notna()]   # clientes CON email
```

Para ver cuántos nulos hay en **cada columna** de la tabla:

```python
clientes.isna().sum()
```

> 💼 **En el trabajo:** "¿qué clientes no tienen email?" es una consulta típica para una campaña de actualización de datos.""",
task="Guarda los clientes que **no tienen email**.",
starter="resultado = ",
solution="resultado = clientes[clientes['email'].isna()]",
hint="clientes[clientes['email'].isna()]",
sql="SELECT * FROM clientes WHERE email IS NULL;"),

# =========================================================== Transformar
dict(id="df10", sec="Ordenar y transformar", title="Ordenar con desempate", level=2,
theory="""`sort_values` ordena el DataFrame por una o varias columnas:

```python
df.sort_values("precio")                                  # menor a mayor
df.sort_values("precio", ascending=False)                 # mayor a menor
df.sort_values(["pais", "edad"], ascending=[True, False]) # dos criterios
```

Con varias columnas, la segunda solo se usa para **desempatar** las filas que coinciden en la primera. Es igual que `ORDER BY pais ASC, edad DESC`.""",
task="Ordena `clientes` por `pais` (A→Z) y, dentro de cada país, por `edad` de **mayor a menor**.",
starter="resultado = ",
solution="resultado = clientes.sort_values(['pais', 'edad'], ascending=[True, False])",
hint="ascending=[True, False]",
sql="SELECT * FROM clientes ORDER BY pais ASC, edad DESC;"),

dict(id="df11", sec="Ordenar y transformar", title="Columnas calculadas", level=1,
theory="""Para crear una columna nueva basta con **asignarla**. Las operaciones entre columnas son vectorizadas: se calculan fila por fila de forma automática.

```python
pedidos_ext["total"] = pedidos_ext["precio"] * pedidos_ext["cantidad"]
```

Si la columna ya existe, se **sobrescribe**.

> 💡 Alternativa encadenable: `df.assign(total=df["precio"] * df["cantidad"])`, que devuelve un DataFrame nuevo sin tocar el original.""",
task="Añade a `productos` la columna `valor_stock` = `precio * stock` (cuánto dinero hay en inventario). Guarda el DataFrame completo en `resultado`.",
starter="# crea la columna y luego:\nresultado = productos",
solution="productos['valor_stock'] = productos['precio'] * productos['stock']\nresultado = productos",
hint="productos['valor_stock'] = productos['precio'] * productos['stock']",
sql="SELECT *, precio * stock AS valor_stock FROM productos;"),

dict(id="df12", sec="Ordenar y transformar", title="Categorías por tramos", level=3,
theory="""`pd.cut` convierte números en **categorías por tramos**. Es muy común para edades, rangos de precio o niveles de riesgo.

- `bins`: los bordes de los tramos. El borde **derecho entra** en el tramo: `(0, 29]` incluye el 29.
- `labels`: el nombre de cada tramo (uno menos que la cantidad de bordes).

```python
pd.cut(df["nota"], bins=[0, 4, 7, 10], labels=["bajo", "medio", "alto"])
# 3 -> bajo, 5 -> medio, 7 -> medio, 9 -> alto
```

> 💼 **En el trabajo:** segmentar clientes por edad o por gasto para marketing.""",
task="Añade a `clientes` la columna `rango_edad`: **joven** (hasta 29), **adulto** (30 a 44) y **senior** (45 o más). Guarda en `resultado` solo las columnas `nombre`, `edad` y `rango_edad`.",
starter="clientes['rango_edad'] = \nresultado = ",
solution="clientes['rango_edad'] = pd.cut(clientes['edad'], bins=[0, 29, 44, 120], labels=['joven', 'adulto', 'senior'])\nresultado = clientes[['nombre', 'edad', 'rango_edad']]",
hint="bins=[0, 29, 44, 120], labels=['joven', 'adulto', 'senior']",
sql="SELECT nombre, edad,\n  CASE WHEN edad <= 29 THEN 'joven'\n       WHEN edad <= 44 THEN 'adulto'\n       ELSE 'senior' END AS rango_edad\nFROM clientes;"),

dict(id="df13", sec="Ordenar y transformar", title="Renombrar y descartar", level=2,
theory="""Dos operaciones de mantenimiento muy frecuentes:

- `df.rename(columns={"viejo": "nuevo"})` cambia nombres de columnas.
- `df.drop(columns=["col"])` elimina columnas.

Ambas devuelven un DataFrame **nuevo**, así que se pueden **encadenar**:

```python
df.drop(columns=["tmp"]).rename(columns={"cant": "cantidad"})
```""",
task="A partir de `pedidos`: elimina la columna `estado` y renombra `cantidad` a `unidades`.",
starter="resultado = ",
solution="resultado = pedidos.drop(columns=['estado']).rename(columns={'cantidad': 'unidades'})",
hint="pedidos.drop(columns=[...]).rename(columns={...})",
sql="SELECT pedido_id, cliente_id, producto_id, cantidad AS unidades, fecha FROM pedidos;"),

# =========================================================== Limpiar
dict(id="df14", sec="Limpiar datos", title="Adiós, duplicados", level=1,
theory="""Se dice que el **80% del trabajo con datos es limpieza**. La tabla `sucio` tiene los problemas típicos: duplicados, espacios, mayúsculas mezcladas, números guardados como texto y nulos.

Para los duplicados:
- `df.duplicated()` marca con True las filas repetidas.
- `df.drop_duplicates()` las elimina (conserva la primera aparición).
- `subset=[...]` compara solo algunas columnas; `keep="last"` conserva la última.

```python
df.drop_duplicates(subset=["email"])   # un registro por email
```""",
task="Elimina las filas duplicadas de `sucio`.",
starter="resultado = ",
solution="resultado = sucio.drop_duplicates()",
hint="sucio.drop_duplicates()",
sql="SELECT DISTINCT * FROM sucio;"),

dict(id="df15", sec="Limpiar datos", title="Texto a número", level=2,
theory="""Cuando una columna numérica llega como texto y trae valores basura (por ejemplo `"n/d"`), `astype(int)` falla. La solución es:

```python
pd.to_numeric(serie, errors="coerce")
```

`errors="coerce"` convierte lo que puede y pone **NaN** en lo que no. Después decides qué hacer con esos NaN (rellenarlos, descartarlos…).

Para limpiar símbolos, antes se usa `.str.replace()`:

```python
s.str.replace("€", "", regex=False)
```""",
task="Convierte la columna `monto` de `sucio` a número decimal: quita los `$` y las `,` y luego conviértela con `astype(float)`. Los nulos deben seguir siendo nulos. Guarda la Series.",
starter="resultado = ",
solution="resultado = sucio['monto'].str.replace('$', '', regex=False).str.replace(',', '', regex=False).astype(float)",
hint="Dos .str.replace(..., regex=False) y luego .astype(float)",
sql="SELECT CAST(REPLACE(REPLACE(monto, '$', ''), ',', '') AS DECIMAL) FROM sucio;"),

dict(id="df16", sec="Limpiar datos", title="Rellenar y descartar nulos", level=2,
theory="""Hay dos estrategias para los nulos, y cuál conviene depende del caso:

**Rellenarlos** con `fillna`:
```python
df["email"].fillna("sin_email")
df.fillna({"stock": 0, "email": "?"})     # un valor por columna
```

**Descartarlos** con `dropna`:
```python
df.dropna()                          # quita filas con CUALQUIER nulo
df.dropna(subset=["nombre"])         # solo si falta el nombre
```

> 💼 **En el trabajo:** limita `dropna` con `subset` para no perder filas valiosas por un dato secundario que falta.""",
task="De `sucio`, elimina las filas donde falte el `nombre` **o** el `monto`.",
starter="resultado = ",
solution="resultado = sucio.dropna(subset=['nombre', 'monto'])",
hint="sucio.dropna(subset=['nombre', 'monto'])",
sql="SELECT * FROM sucio WHERE nombre IS NOT NULL AND monto IS NOT NULL;"),

dict(id="df17", sec="Limpiar datos", title="Pipeline de limpieza", level=3,
theory="""En un proyecto real se juntan todos los pasos de limpieza en uno solo, **encadenando** métodos. `assign` crea o reemplaza columnas, y con `lambda d:` accedes al DataFrame de ese punto de la cadena:

```python
limpio = (
    df.drop_duplicates()
      .assign(nombre=lambda d: d["nombre"].str.strip().str.title())
)
```

Así el código se lee de arriba abajo como una **receta**.""",
task="""Limpia `sucio` en una sola cadena:
1. Elimina los duplicados.
2. `ciudad`: sin espacios sobrantes y en formato Título (`Madrid`, `Lima`...).
3. `edad`: numérica (los valores inválidos pasan a NaN).

Guarda el DataFrame resultante, con las mismas columnas.""",
starter="resultado = (\n    sucio\n    # .drop_duplicates()\n    # .assign(...)\n)",
solution="resultado = (\n    sucio.drop_duplicates()\n    .assign(ciudad=lambda d: d['ciudad'].str.strip().str.title(),\n            edad=lambda d: pd.to_numeric(d['edad'], errors='coerce'))\n)",
hint="sucio.drop_duplicates().assign(ciudad=lambda d: ..., edad=lambda d: pd.to_numeric(..., errors='coerce'))",
sql="SELECT DISTINCT id, nombre, TRY_CAST(edad AS INT) AS edad,\n       INITCAP(TRIM(ciudad)) AS ciudad, monto\nFROM sucio;"),

# =========================================================== Agrupar
dict(id="df18", sec="Agrupar y resumir", title="Media por grupo", level=2,
theory="""`groupby` sigue el patrón **dividir → aplicar → combinar**:

1. **Divide** la tabla en grupos según una columna.
2. **Aplica** un cálculo a cada grupo (suma, media, conteo…).
3. **Combina** los resultados en una tabla nueva.

```python
empleados.groupby("depto")["salario"].mean()
# depto
# Dirección    9000.0
# IT           5366.7
# ...
```

Se lee así: *"agrupa por depto, toma el salario y calcula la media"*.""",
task="Calcula la edad **media** de los clientes de cada `segmento`.",
starter="resultado = ",
solution="resultado = clientes.groupby('segmento')['edad'].mean()",
hint="clientes.groupby('segmento')['edad'].mean()",
sql="SELECT segmento, AVG(edad) FROM clientes GROUP BY segmento;"),

dict(id="df19", sec="Agrupar y resumir", title="Varias métricas a la vez", level=3,
theory="""Con la **agregación con nombre** (*named aggregation*) calculas varias métricas y eliges el nombre de cada columna de salida con el formato `nombre=("columna", "función")`:

```python
pedidos.groupby("estado").agg(
    unidades=("cantidad", "sum"),
    n_pedidos=("pedido_id", "count"),
)
```

Funciones habituales: `"sum"`, `"mean"`, `"median"`, `"min"`, `"max"`, `"count"`, `"nunique"`, `"std"`.""",
task="Por `categoria` de `productos`, calcula `precio_medio` (media de precio), `stock_total` (suma de stock) y `n_productos` (cuántos productos hay).",
starter="resultado = productos.groupby('categoria').agg(\n    \n)",
solution="resultado = productos.groupby('categoria').agg(\n    precio_medio=('precio', 'mean'),\n    stock_total=('stock', 'sum'),\n    n_productos=('producto_id', 'count'),\n)",
hint="precio_medio=('precio', 'mean'), stock_total=('stock', 'sum'), n_productos=('producto_id', 'count')",
sql="SELECT categoria, AVG(precio) AS precio_medio, SUM(stock) AS stock_total,\n       COUNT(*) AS n_productos\nFROM productos GROUP BY categoria;"),

dict(id="df20", sec="Agrupar y resumir", title="Filtrar grupos (HAVING)", level=3,
theory="""En SQL, los grupos se filtran con `HAVING`. En pandas primero **agregas** y después **filtras** el resultado como cualquier Series:

```python
conteo = pedidos["cliente_id"].value_counts()
conteo[conteo >= 3]      # clientes con 3 o más pedidos
```

> 💡 Recuerda el orden lógico: primero se agrupa y después se filtra sobre el resultado agregado.""",
task="Guarda los países con **al menos 2** clientes (una Series con el conteo de cada país).",
starter="conteo = clientes['pais'].value_counts()\nresultado = ",
solution="conteo = clientes['pais'].value_counts()\nresultado = conteo[conteo >= 2]",
hint="conteo[conteo >= 2]",
sql="SELECT pais, COUNT(*) FROM clientes GROUP BY pais HAVING COUNT(*) >= 2;",
check={"ordered": False}),

dict(id="df21", sec="Agrupar y resumir", title="Comparar con tu grupo", level=4,
theory="""`transform` calcula una métrica por grupo pero devuelve **un valor por fila**, alineado con la tabla original. Así puedes comparar cada fila con su grupo:

```python
media = empleados.groupby("depto")["salario"].transform("mean")
empleados["dif_media"] = empleados["salario"] - media
```

`agg` en cambio devuelve **una fila por grupo**.

> 💼 **En el trabajo:** "¿qué vendedores superan el promedio de su zona?" o "¿qué productos se venden por encima de la media de su categoría?".""",
task="Guarda los empleados que cobran **más que la media de su departamento**.",
starter="media_depto = empleados.groupby('depto')['salario'].transform('mean')\nresultado = ",
solution="media_depto = empleados.groupby('depto')['salario'].transform('mean')\nresultado = empleados[empleados['salario'] > media_depto]",
hint="empleados[empleados['salario'] > media_depto]",
sql="SELECT * FROM (\n  SELECT *, AVG(salario) OVER (PARTITION BY depto) AS media_depto\n  FROM empleados) t\nWHERE salario > media_depto;"),

# =========================================================== Unir
dict(id="df22", sec="Unir tablas", title="Inner join con merge", level=2,
theory="""En las bases de datos la información se reparte en varias tablas: `pedidos` guarda el `producto_id`, pero el nombre y el precio están en `productos`. Para juntarlas se usa `merge` (el `JOIN` de SQL):

```python
pedidos.merge(productos, on="producto_id")
```

Tipos de unión (`how=`):
- `"inner"` (por defecto): solo las filas que coinciden en ambas tablas;
- `"left"`: todas las de la izquierda, completando con NaN lo que no coincide;
- `"right"` / `"outer"`: todas las de la derecha / todas las de ambas.

> 💡 Si las columnas clave tienen nombres distintos: `left_on="id_cli", right_on="cliente_id"`.""",
task="Une `pedidos` con `productos` por `producto_id`.",
starter="resultado = ",
solution="resultado = pedidos.merge(productos, on='producto_id')",
hint="pedidos.merge(productos, on='producto_id')",
sql="SELECT * FROM pedidos p\nJOIN productos pr ON p.producto_id = pr.producto_id;",
check={"ordered": False, "ignore_index": True}),

dict(id="df23", sec="Unir tablas", title="¿Cuánto facturamos?", level=2,
theory="""Una vez unidas las tablas, puedes calcular con columnas de las dos. El patrón típico es:

1. **Unir** (`merge`).
2. **Filtrar** lo que no cuenta (pedidos cancelados, devoluciones…).
3. **Calcular** el importe de cada fila.
4. **Agregar** (sumar, promediar…).

```python
df = pedidos.merge(productos, on="producto_id")
(df["cantidad"] * df["precio"]).sum()
```""",
task="Calcula la facturación total (`cantidad * precio`) de los pedidos que **no** están `cancelado`. Guarda un número.",
starter="df = pedidos.merge(productos, on='producto_id')\nresultado = ",
solution="df = pedidos.merge(productos, on='producto_id')\ndf = df[df['estado'] != 'cancelado']\nresultado = (df['cantidad'] * df['precio']).sum()",
hint="Filtra estado != 'cancelado' y luego (cantidad * precio).sum()",
sql="SELECT SUM(p.cantidad * pr.precio)\nFROM pedidos p JOIN productos pr USING (producto_id)\nWHERE p.estado <> 'cancelado';"),

dict(id="df24", sec="Unir tablas", title="Clientes sin pedidos", level=3,
theory="""Un **anti join** busca las filas de A que **no tienen pareja** en B. En pandas, lo más directo es un `isin` negado:

```python
a[~a["id"].isin(b["id"])]
```

Otra forma es hacer un `merge(how="left", indicator=True)`, que añade la columna `_merge` con `both`, `left_only` o `right_only`, y filtrar `left_only`.

> 💼 **En el trabajo:** clientes que se registraron y nunca compraron. ¡Oro para el equipo de marketing!""",
task="Guarda los clientes que **nunca** hicieron un pedido.",
starter="resultado = ",
solution="resultado = clientes[~clientes['cliente_id'].isin(pedidos['cliente_id'])]",
hint="~clientes['cliente_id'].isin(pedidos['cliente_id'])",
sql="SELECT c.* FROM clientes c\nLEFT JOIN pedidos p ON c.cliente_id = p.cliente_id\nWHERE p.pedido_id IS NULL;"),

dict(id="df25", sec="Unir tablas", title="Apilar tablas", level=2,
theory="""`pd.concat([df1, df2])` **apila** tablas una debajo de otra, igual que `UNION ALL` en SQL. Es útil, por ejemplo, para juntar los archivos de enero, febrero y marzo en una sola tabla.

```python
anual = pd.concat([enero, febrero, marzo], ignore_index=True)
```

Con `ignore_index=True` el índice se renumera desde 0; sin él, se conservan los índices originales (y pueden repetirse).""",
task="Apila primero los clientes de **España** y luego los de **Perú**, con el índice renumerado desde 0.",
starter="espana = clientes[clientes['pais'] == 'España']\nperu = clientes[clientes['pais'] == 'Perú']\nresultado = ",
solution="espana = clientes[clientes['pais'] == 'España']\nperu = clientes[clientes['pais'] == 'Perú']\nresultado = pd.concat([espana, peru], ignore_index=True)",
hint="pd.concat([espana, peru], ignore_index=True)",
sql="SELECT * FROM clientes WHERE pais = 'España'\nUNION ALL\nSELECT * FROM clientes WHERE pais = 'Perú';"),

# =========================================================== Reestructurar y fechas
dict(id="df26", sec="Reestructurar y fechas", title="Tabla dinámica", level=3,
theory="""`pd.pivot_table` es la **tabla dinámica** de Excel:

- `index`: lo que va en las filas;
- `columns`: lo que va en las columnas;
- `values`: la columna a resumir;
- `aggfunc`: cómo resumirla (`"sum"`, `"mean"`...);
- `fill_value=0`: qué poner en las combinaciones vacías.

```python
pd.pivot_table(df, index="mes", columns="tienda", values="ventas", aggfunc="sum")
```""",
task="Une `pedidos` con `productos` y crea una tabla con `estado` en las filas, `categoria` en las columnas y la **suma de `cantidad`**. Los huecos deben ser 0.",
starter="df = pedidos.merge(productos, on='producto_id')\nresultado = pd.pivot_table(df, )",
solution="df = pedidos.merge(productos, on='producto_id')\nresultado = pd.pivot_table(df, index='estado', columns='categoria', values='cantidad', aggfunc='sum', fill_value=0)",
hint="index='estado', columns='categoria', values='cantidad', aggfunc='sum', fill_value=0",
sql="SELECT estado,\n  SUM(CASE WHEN categoria='Audio' THEN cantidad ELSE 0 END) AS Audio\n  -- ...una columna por categoría\nFROM pedidos JOIN productos USING (producto_id)\nGROUP BY estado;"),

dict(id="df27", sec="Reestructurar y fechas", title="De ancho a largo con melt", level=3,
theory="""La tabla `trimestral` está en formato **ancho**: una columna por trimestre. Es cómoda de leer, pero incómoda de analizar. El formato **largo** (una fila por observación) es el preferido por las bases de datos, por seaborn y por los modelos. Para pasar de uno a otro se usa `melt`:

```python
df.melt(id_vars="tienda", var_name="trimestre", value_name="ventas")
```

- `id_vars`: las columnas que se mantienen fijas;
- `var_name`: el nombre de la nueva columna con los antiguos encabezados;
- `value_name`: el nombre de la columna con los valores.""",
task="Convierte `trimestral` a formato largo con las columnas `tienda`, `trimestre` y `ventas`.",
starter="resultado = trimestral.melt()",
solution="resultado = trimestral.melt(id_vars='tienda', var_name='trimestre', value_name='ventas')",
hint="id_vars='tienda', var_name='trimestre', value_name='ventas'",
sql="SELECT tienda, 'Q1' AS trimestre, Q1 AS ventas FROM trimestral\nUNION ALL SELECT tienda, 'Q2', Q2 FROM trimestral\nUNION ALL SELECT tienda, 'Q3', Q3 FROM trimestral;",
check={"ordered": False, "ignore_index": True}),

dict(id="df28", sec="Reestructurar y fechas", title="Trabajar con fechas", level=2,
theory="""Las columnas de tipo fecha (`datetime64`) tienen el accesor **`.dt`**, que permite extraer partes de la fecha:

```python
pedidos["fecha"].dt.year        # año
pedidos["fecha"].dt.month       # mes (1-12)
pedidos["fecha"].dt.day_name()  # nombre del día
```

Y puedes **agrupar directamente** por esas partes:

```python
pedidos.groupby(pedidos["fecha"].dt.month).size()
```

> ⚠️ Si la fecha llegó como texto, primero conviértela con `pd.to_datetime(df["fecha"])`.""",
task="Cuenta cuántos pedidos hubo en cada **mes** (número de mes del 1 al 12). Guarda la Series.",
starter="resultado = ",
solution="resultado = pedidos.groupby(pedidos['fecha'].dt.month).size()",
hint="pedidos.groupby(pedidos['fecha'].dt.month).size()",
sql="SELECT EXTRACT(MONTH FROM fecha) AS mes, COUNT(*) FROM pedidos GROUP BY mes;"),

dict(id="df29", sec="Reestructurar y fechas", title="Series temporales", level=3,
theory="""Con datos diarios es habitual **cambiar la frecuencia** o **suavizar** la serie:

- `resample("W")` agrupa por semana (`"MS"` por mes). Necesita que la fecha sea el **índice**.
- `rolling(7).mean()` calcula la **media móvil**: el promedio de los últimos 7 valores de cada punto. Suaviza el ruido del día a día y deja ver la tendencia.

```python
s = ventas_diarias.set_index("fecha")["ventas"]
s.resample("MS").sum()        # ventas por mes
s.rolling(7).mean()           # media móvil semanal
```""",
task="Calcula la suma de `ventas` por **semana** (`\"W\"`) de `ventas_diarias`. Guarda la Series.",
starter="resultado = ",
solution="resultado = ventas_diarias.set_index('fecha')['ventas'].resample('W').sum()",
hint="ventas_diarias.set_index('fecha')['ventas'].resample('W').sum()",
sql="SELECT DATE_TRUNC('week', fecha) AS semana, SUM(ventas)\nFROM ventas_diarias GROUP BY semana;"),

dict(id="df30", sec="Reestructurar y fechas", title="Ranking por grupo", level=4,
theory="""`groupby(...)["col"].rank()` calcula la **posición** de cada fila dentro de su grupo. Es el `RANK() OVER (PARTITION BY ...)` de SQL.

- `ascending=False`: el valor más alto queda en la posición 1.
- `method="dense"`: los empates comparten posición y no se saltan números (1, 2, 2, 3).

```python
df["pos"] = df.groupby("tienda")["ventas"].rank(ascending=False, method="dense")
```""",
task="Añade a `empleados` la columna `ranking` con la posición del salario **dentro de su depto** (1 = el que más cobra; método `dense`). Guarda las columnas `nombre`, `depto`, `salario` y `ranking`.",
starter="empleados['ranking'] = \nresultado = empleados[['nombre', 'depto', 'salario', 'ranking']]",
solution="empleados['ranking'] = empleados.groupby('depto')['salario'].rank(method='dense', ascending=False)\nresultado = empleados[['nombre', 'depto', 'salario', 'ranking']]",
hint="empleados.groupby('depto')['salario'].rank(method='dense', ascending=False)",
sql="SELECT nombre, depto, salario,\n  DENSE_RANK() OVER (PARTITION BY depto ORDER BY salario DESC) AS ranking\nFROM empleados;"),

# =========================================================== SQL
dict(id="df31", sec="DataFrames y bases de datos", title="Consultar una base de datos", level=2,
theory="""En el trabajo, los datos rara vez vienen en un CSV: viven en **bases de datos** (PostgreSQL, MySQL, SQL Server, Snowflake…). Con `pd.read_sql(consulta, conexión)` ejecutas SQL y el resultado llega directamente a un DataFrame.

En este módulo tienes una base SQLite en memoria llamada `conn`, con las tablas `clientes`, `productos` y `pedidos`.

```python
pd.read_sql("SELECT * FROM productos WHERE stock > 0", conn)
```

En un proyecto real, `conn` sería una conexión creada con SQLAlchemy:

```python
from sqlalchemy import create_engine
conn = create_engine("postgresql://usuario:clave@servidor/base")
```

> 💼 **En el trabajo:** la regla de oro es **filtrar y agregar en la base de datos** y traer a pandas solo lo necesario.""",
task="Con `read_sql`, trae el `nombre` y la `ciudad` de los clientes con `edad > 40`.",
starter="resultado = pd.read_sql('''\n    SELECT ...\n''', conn)",
solution="resultado = pd.read_sql('SELECT nombre, ciudad FROM clientes WHERE edad > 40', conn)",
hint="SELECT nombre, ciudad FROM clientes WHERE edad > 40",
sql="SELECT nombre, ciudad FROM clientes WHERE edad > 40;"),

dict(id="df32", sec="DataFrames y bases de datos", title="Parámetros seguros", level=3,
theory="""**Nunca** metas valores dentro de una consulta con f-strings (`f"... WHERE pais = '{pais}'"`). Es la puerta de entrada a la **inyección SQL**, uno de los fallos de seguridad más graves. Usa **parámetros**:

```python
pd.read_sql("SELECT * FROM clientes WHERE pais = ?", conn, params=("Chile",))
```

El marcador cambia según el motor: `?` en SQLite y `%s` o `:nombre` en otros.

> ⚠️ `params` espera una **tupla**. Con un solo valor, no olvides la coma: `(valor,)`.""",
task="Usando un parámetro, trae los productos con `precio` mayor que `precio_min`.",
starter="precio_min = 100\nresultado = pd.read_sql('SELECT * FROM productos WHERE precio > ?', conn, )",
solution="precio_min = 100\nresultado = pd.read_sql('SELECT * FROM productos WHERE precio > ?', conn, params=(precio_min,))",
hint="params=(precio_min,)",
sql="SELECT * FROM productos WHERE precio > :precio_min;"),

dict(id="df33", sec="DataFrames y bases de datos", title="Guardar en la base de datos", level=3,
theory="""`df.to_sql("tabla", conn, index=False, if_exists=...)` **escribe** un DataFrame como tabla en la base de datos. Es el paso *Load* de un proceso **ETL** (*Extract, Transform, Load*).

Valores de `if_exists`:
- `"fail"` (por defecto): da error si la tabla ya existe;
- `"replace"`: la borra y la vuelve a crear;
- `"append"`: añade filas (para cargas incrementales, por ejemplo diarias).

```python
resumen.to_sql("resumen_ventas", conn, index=False, if_exists="replace")
```""",
task="Calcula con pandas el número de clientes por país (columnas `pais` y `n_clientes`), guárdalo en la tabla `resumen_pais` y léelo de vuelta con `read_sql` en `resultado`.",
starter="resumen = \nresumen.to_sql('resumen_pais', conn, index=False, if_exists='replace')\nresultado = pd.read_sql('SELECT * FROM resumen_pais', conn)",
solution="resumen = clientes.groupby('pais', as_index=False).agg(n_clientes=('cliente_id', 'count'))\nresumen.to_sql('resumen_pais', conn, index=False, if_exists='replace')\nresultado = pd.read_sql('SELECT * FROM resumen_pais', conn)",
hint="clientes.groupby('pais', as_index=False).agg(n_clientes=('cliente_id', 'count'))",
sql="CREATE TABLE resumen_pais AS\nSELECT pais, COUNT(*) AS n_clientes FROM clientes GROUP BY pais;",
check={"ordered": False, "ignore_index": True}),
]
