# -*- coding: utf-8 -*-
"""Módulo 00 · Python para Ciencia de Datos."""
from datasets import PY_SETUP
from framework import A, B, C, D, E, F, G, Q, ask, concept, field, module, project

S1, S2, S3, S4, S5 = "Variables, tipos y números", "Strings: texto que llega sucio", "Listas, tuplas y sets", "Diccionarios", "Decisiones: booleanos y condicionales"
S6, S7, S8, S9 = "Loops: repetir sobre los datos", "Funciones: empaquetar lógica", "Comprensiones", "Errores y excepciones"
S10, S11, S12, S13 = "Módulos e imports", "Trabajar con archivos", "Leer código y debuggear", "Python aplicado a datos"
SP = "Proyecto: mini sistema de análisis de ventas"

CONCEPTS = [
concept("py-variables", "Variables y tipos de datos", "variables · type() · int/float/str/bool/None",
    problem="Guardar un dato con un nombre para reutilizarlo, y saber **qué tipo** de dato es (número, texto, verdadero/falso, vacío). El tipo decide qué operaciones tienen sentido.",
    when="Siempre. Pero se vuelve crítico cuando los datos llegan de archivos o formularios: un precio puede venir como texto `'1200.50'` y no como número.",
    signals=["Un cálculo da un resultado absurdo (texto repetido, concatenado)", "Errores tipo `TypeError` o `unsupported operand`", "Datos leídos de CSV, Excel, APIs o input()"],
    can=["Guardar valores y resultados intermedios con nombres claros", "Preguntar el tipo con `type(x)`", "Convertir entre tipos: `int()`, `float()`, `str()`, `bool()`", "Representar 'dato ausente' con `None`"],
    cant=["Convertir automáticamente un texto como `'n/d'` a número (da error)", "Hacer cuentas entre texto y número sin convertir", "Adivinar el tipo correcto: lo decidís vos"],
    nomemo="No memorices todas las reglas de conversión. Recordá la idea: **si viene de afuera, verificá el tipo**. La sintaxis exacta la consultás.",
    ai="«Tengo una variable `precio` que viene de un CSV como texto, por ejemplo '1200.50'. ¿Cómo la convierto a número y qué pasa si viene vacía o con 'n/d'? Explicame antes de darme código.»",
    verify="Imprimí `type(variable)` y un caso de prueba que sepas calcular a mano.",
    example="""precio = "1200.50"        # str: llegó como texto
cantidad = 2              # int
print(type(precio))       # <class 'str'>
total = float(precio) * cantidad   # 2401.0""",
    check=("¿Qué devuelve `'25' * 3` en Python?", [
        ("`'252525'`: repite el texto tres veces", True, "Con un str, `*` repite. Por eso hay que convertir con int() o float() antes de calcular."),
        ("`75`", False, "Sería 75 si '25' fuera un número. Es un texto."),
        ("Un error", False, "No da error: `str * int` es válido (repite el texto), y por eso es un bug silencioso."),
    ])),

concept("py-numeros", "Números y operaciones", "+ - * / // % ** · round()",
    problem="Calcular métricas: totales, promedios, porcentajes, variaciones, descuentos, impuestos.",
    when="Cada vez que una pregunta de negocio se responde con una cuenta: ¿cuánto facturamos?, ¿qué porcentaje creció?",
    signals=["La pregunta pide un total, un promedio o un porcentaje", "Hay que aplicar un descuento, un impuesto o una tasa", "Hay que repartir en grupos (división entera y resto)"],
    can=["Aritmética básica y potencias", "División entera `//` y resto `%` (ej.: cajas completas y unidades sueltas)", "Redondear para mostrar: `round(x, 2)`"],
    cant=["Representar todos los decimales con exactitud: `0.1 + 0.2` da `0.30000000000000004`", "Dividir por cero (da `ZeroDivisionError`)"],
    nomemo="No memorices la precedencia de operadores: usá paréntesis para que la fórmula se lea sola.",
    ai="«Quiero calcular el precio final con 10% de descuento y después 21% de IVA. Explicame en qué orden se aplican y por qué, y después mostrame la fórmula en Python.»",
    verify="Calculá un caso a mano (o con calculadora) y compará. Redondeá solo al final para mostrar.",
    example="""entradas = 4 * 18.0              # 72.0
con_recargo = entradas * (1 + 0.05)  # +5%
final = round(con_recargo, 2)
cajas, sueltas = 47 // 12, 47 % 12   # 3 cajas, 11 sueltas""",
    check=("Tenés 47 unidades y cada caja lleva 12. ¿Qué operación da las cajas completas?", [
        ("`47 // 12`", True, "La división entera descarta los decimales: 3 cajas completas."),
        ("`47 / 12`", False, "Da 3.9166…: no son cajas completas."),
        ("`47 % 12`", False, "El resto (11) son las unidades que quedan sueltas."),
    ])),

concept("py-strings", "Strings (texto)", "str · .strip() .lower() .split() · f-strings",
    problem="Limpiar, normalizar, separar y armar texto: nombres escritos a mano, códigos, líneas de un archivo, reportes.",
    when="Cuando el mismo valor aparece escrito de varias formas ('ana', ' ANA ') o necesitás partir/armar un texto.",
    signals=["Espacios de más, mayúsculas mezcladas, tildes inconsistentes", "Un texto que contiene varios datos juntos (`'2024-03-01,Laptop,1'`)", "Hay que generar un mensaje o reporte con valores"],
    can=["Normalizar: `.strip()`, `.lower()`, `.title()`", "Separar: `.split(',')` → lista de textos", "Reemplazar: `.replace('$', '')`", "Armar mensajes: `f'{producto}: ${total:,.2f}'`"],
    cant=["Modificar un string en el lugar: los métodos **devuelven uno nuevo**", "Convertir automáticamente las partes de `split()` en números: siguen siendo texto"],
    nomemo="No memorices los ~40 métodos de str. Sabé que existen para limpiar, buscar, separar y reemplazar; el nombre exacto lo buscás.",
    ai="«Tengo nombres como '  carla GÓMEZ ' y quiero 'Carla Gómez'. ¿Qué métodos de string necesito y en qué orden? Explicá qué devuelve cada uno.»",
    verify="Probá con 2-3 ejemplos 'feos' (espacios, mayúsculas) y mirá el resultado con `repr()` para ver espacios ocultos.",
    example="""ciudad = "  buenos AIRES "
limpia = ciudad.strip().lower()     # 'buenos aires'
dia, sensor, valor = "lun;S3;21.5".split(";")
print(f"Sensor {sensor}: {float(valor):.1f} °C")  # Sensor S3: 21.5 °C""",
    check=("Después de `s = '  ana '` y `s.strip()`, ¿cuánto vale `s`?", [
        ("Sigue siendo `'  ana '`", True, "Los strings no se modifican: strip() devuelve un string nuevo. Hay que guardarlo: `s = s.strip()`."),
        ("`'ana'`", False, "Solo si hacés `s = s.strip()`."),
        ("`None`", False, "strip() devuelve un string, no None."),
    ])),

concept("py-listas", "Listas", "list · índices · slicing · append · len/sum/max",
    problem="Guardar una **colección ordenada** de valores (ventas de cada día, lecturas de un sensor) para recorrerla, resumirla o recortarla.",
    when="Tenés varios valores del mismo tipo, el orden importa y puede crecer.",
    signals=["'las ventas de cada día', 'las lecturas', 'los precios'", "Necesitás el primero/último, un tramo, el máximo o la suma", "Vas agregando resultados uno a uno"],
    can=["Acceder por posición: `x[0]`, `x[-1]`", "Recortar: `x[2:5]`, `x[-3:]`", "Agregar: `x.append(v)`", "Resumir con funciones: `len`, `sum`, `max`, `min`, `sorted`"],
    cant=["Buscar rápido por nombre (para eso: diccionario)", "Hacer cuentas vectorizadas: `[1,2] * 2` **repite** la lista, no multiplica (para eso: NumPy)"],
    nomemo="No memorices todos los métodos. Lo clave: posiciones empiezan en 0, el slicing excluye el final, y `.sort()` modifica en el lugar y devuelve None.",
    ai="«Tengo una lista con las ventas de 7 días. ¿Cómo obtengo los últimos 3 días y el promedio? Explicame cómo funcionan los índices negativos.»",
    verify="Verificá `len()` del resultado y compará con lo que esperás contar a mano.",
    example="""ventas = [1200, 950, 1430, 880]
ventas[0], ventas[-1]     # 1200, 880
ventas[-2:]               # [1430, 880]
ventas.append(1700)
promedio = sum(ventas) / len(ventas)""",
    check=("¿Qué devuelve `[10, 20, 30, 40][1:3]`?", [
        ("`[20, 30]`", True, "Empieza en la posición 1 e **incluye hasta la 2** (el 3 queda afuera)."),
        ("`[10, 20, 30]`", False, "La posición 0 no está incluida: el slice empieza en 1."),
        ("`[20, 30, 40]`", False, "El final del slice (3) no se incluye."),
    ])),

concept("py-tuplas-sets", "Tuplas y sets", "tuple (fija) · set (sin duplicados)",
    problem="**Tupla**: agrupar valores que van juntos y no deberían cambiar (un registro, varios resultados de una función). **Set**: quedarte con valores únicos y preguntar pertenencia rápido.",
    when="Tupla: devolver (mínimo, máximo) desde una función, coordenadas. Set: '¿cuántos clientes distintos?', '¿este código ya apareció?'.",
    signals=["'distintos', 'únicos', 'sin repetir' → set", "'¿está en…?' sobre muchos valores → set", "Un par/terna fija de datos → tupla"],
    can=["Eliminar duplicados: `set(lista)`", "Operaciones de conjuntos: unión `|`, intersección `&`, diferencia `-`", "Desempaquetar tuplas: `minimo, maximo = resumen`"],
    cant=["Mantener el orden en un set (no tiene orden; usá `sorted()` si lo necesitás)", "Modificar una tupla después de creada", "Acceder a un set por posición"],
    nomemo="Solo recordá la intención: tupla = registro fijo; set = únicos + pertenencia.",
    ai="«Tengo una lista de 50.000 categorías con repetidos. ¿Cuál es la forma más simple de saber cuáles son las distintas y cuántas hay? ¿Por qué?»",
    verify="Compará `len(lista)` vs `len(set(lista))`: la diferencia es la cantidad de repetidos.",
    example="""visitantes = ["ana", "luis", "ana", "eva"]
unicos = set(visitantes)          # {'ana', 'luis', 'eva'}
len(unicos)                       # 3
punto = (3.5, -1.2)               # tupla: no cambia
minimo, maximo = (880, 2100)      # desempaquetar""",
    check=("¿Qué estructura usarías para saber cuántos clientes **distintos** compraron?", [
        ("Un set", True, "El set elimina duplicados: `len(set(clientes))`."),
        ("Una tupla", False, "La tupla conserva duplicados y no los elimina."),
        ("Un string", False, "No sirve para contar elementos distintos."),
    ])),

concept("py-dict", "Diccionarios", "dict · clave → valor · .get() · .items()",
    problem="Buscar un valor **por su nombre** (clave) en lugar de por posición: precio por producto, total por cliente. También representar un registro con campos con nombre.",
    when="Necesitás asociar cosas (producto → precio) o acumular resultados por grupo (categoría → total).",
    signals=["'el precio de cada producto', 'el total por cliente'", "Buscás muchas veces por un identificador", "Agrupar/contar 'por algo' en Python puro"],
    can=["Buscar: `precios['Mouse']` o `precios.get('Webcam', 0)`", "Agregar/actualizar: `precios['Webcam'] = 60.0`", "Recorrer: `for clave, valor in d.items()`", "Acumular por grupo: `totales[cat] = totales.get(cat, 0) + monto`"],
    cant=["Tener claves repetidas", "Usar listas como claves", "Encontrar una clave mal escrita: `'mouse' ≠ 'Mouse'` (KeyError)"],
    nomemo="Lo esencial: `[]` falla si no existe la clave; `.get(clave, defecto)` no falla. `.items()` para recorrer pares.",
    ai="«Quiero contar cuántas ventas hay por categoría usando un diccionario en Python puro. Explicame el patrón de acumulador con .get() paso a paso.»",
    verify="Sumá todos los valores del diccionario (`sum(d.values())`) y compará con el total general.",
    example="""precios = {"Laptop": 1200.0, "Mouse": 25.5}
precios["Mouse"]                 # 25.5
precios.get("Webcam", 0)         # 0 (no existe, no falla)
votos = {}
for color in ["rojo", "azul", "rojo"]:
    votos[color] = votos.get(color, 0) + 1   # {'rojo': 2, 'azul': 1}""",
    check=("`precios = {'Mouse': 25.5}`. ¿Qué pasa con `precios['mouse']`?", [
        ("`KeyError`: la clave no existe", True, "Las claves distinguen mayúsculas: 'mouse' y 'Mouse' son distintas."),
        ("Devuelve 25.5", False, "No: las claves son sensibles a mayúsculas."),
        ("Devuelve None", False, "Eso pasaría con `.get('mouse')`, no con corchetes."),
    ])),

concept("py-bool", "Booleanos y comparaciones", "True/False · == != > < · and or not · in",
    problem="Hacer **preguntas** sobre los datos que se responden sí/no: ¿supera el umbral?, ¿es premium y de España?, ¿el producto está en el catálogo?",
    when="Antes de cualquier filtro o decisión. Las condiciones de pandas (`df[df['edad'] > 40]`) son esta misma idea aplicada a columnas.",
    signals=["'mayor que', 'igual a', 'entre', 'que no sea'", "Combinar criterios: 'y', 'o'", "'¿está en la lista…?'"],
    can=["Comparar: `==`, `!=`, `>`, `>=`, `<`, `<=`", "Combinar: `and`, `or`, `not`", "Pertenencia: `'Mouse' in precios`", "Rangos legibles: `20 <= t <= 25`"],
    cant=["Comparar `=` (asignar) con `==` (comparar): son distintos", "Usar `and`/`or` con columnas de pandas (allí van `&` y `|`)"],
    nomemo="Recordá que `0`, `''`, `[]` y `None` se comportan como False. El resto, como True.",
    ai="«Quiero marcar una venta como 'revisar' si el monto supera 1000 o si el cliente es nuevo y paga en efectivo. ¿Cómo escribo esa condición y cómo la pruebo?»",
    verify="Probá la condición con un caso que debería dar True y otro que debería dar False.",
    example="""monto, es_premium = 750, True
monto > 500 and es_premium      # True
"Mouse" in {"Mouse": 25.5}     # True (busca en las claves)
20 <= 22.5 <= 25               # True""",
    check=("¿Qué devuelve `5 > 3 and 2 > 4`?", [
        ("`False`", True, "`and` necesita que ambas sean True; 2 > 4 es False."),
        ("`True`", False, "Eso sería con `or`."),
        ("`2`", False, "Las comparaciones devuelven booleanos."),
    ])),

concept("py-if", "Condicionales", "if / elif / else",
    problem="Tomar **decisiones** distintas según los datos: clasificar montos en tramos, aplicar reglas de negocio, descartar valores inválidos.",
    when="La respuesta depende de una o más condiciones: 'si…, entonces…; si no…'.",
    signals=["'clasificar en', 'según el valor', 'si supera…'", "Reglas de negocio con casos", "Validaciones antes de calcular"],
    can=["Ramificar con `if/elif/else`", "Encadenar tramos ordenados de mayor a menor (o al revés)", "Escribir la versión corta: `'alta' if m >= 500 else 'normal'`"],
    cant=["Evaluar varias ramas a la vez: se ejecuta **solo la primera** que se cumple (el orden importa)", "Reemplazar lógica vectorizada en tablas grandes (en pandas: `np.where`, `pd.cut`)"],
    nomemo="Lo importante es diseñar los tramos (¿dónde corta cada uno?, ¿incluye el borde?). La sintaxis es siempre la misma.",
    ai="«Necesito clasificar montos en 'alta' (≥500), 'media' (≥100) y 'baja'. Antes del código, ayudame a verificar que los bordes (100, 500) caen en el tramo correcto.»",
    verify="Probá los **bordes** exactos (99.9, 100, 500) además de valores típicos.",
    example="""def estado_bateria(pct):
    if pct >= 80:
        return "llena"
    elif pct >= 20:
        return "normal"
    else:
        return "cargar\"""",
    check=("Con `if x > 10: ... elif x > 5: ...`, si `x = 20`, ¿qué ramas se ejecutan?", [
        ("Solo la primera (`x > 10`)", True, "En cuanto una condición se cumple, se ignoran las siguientes."),
        ("Las dos", False, "elif solo se evalúa si las anteriores fueron False."),
        ("Ninguna", False, "20 > 10 es True."),
    ])),

concept("py-for", "Loop for", "for · acumuladores · enumerate · zip",
    problem="Repetir la misma operación **para cada elemento** de una colección: calcular el ingreso de cada venta, acumular totales, construir resultados.",
    when="Tenés una colección y querés procesar todos sus elementos (o acumular algo a partir de ellos).",
    signals=["'para cada venta', 'de todas las filas', 'recorrer'", "Acumular: total, conteo, máximo hasta ahora", "Construir una lista o diccionario nuevo"],
    can=["Recorrer listas, strings, diccionarios (`.items()`), archivos línea por línea", "Patrón acumulador: inicializar **antes** del loop y actualizar adentro", "Obtener posición y valor: `enumerate(lista)`", "Recorrer dos listas en paralelo: `zip(a, b)`"],
    cant=["Ser rápido con millones de filas (para eso: pandas/NumPy vectorizados)", "Modificar una lista mientras la recorrés sin efectos raros"],
    nomemo="Lo que importa es el **patrón**: ¿qué inicializo antes?, ¿qué hago con cada elemento?, ¿qué devuelvo al final?",
    ai="«Tengo una lista de diccionarios con ventas (cantidad, precio). Quiero el total facturado. Explicame el patrón acumulador antes de escribir el for.»",
    verify="Probá el loop con una lista de 2 elementos donde sepas el resultado de memoria.",
    example="""horas = [7.5, 8.0, 6.5, 9.0]     # horas trabajadas por día
total = 0                       # 1) inicializar ANTES
for h in horas:                 # 2) para cada elemento…
    total += h                  # 3) acumular
print(total)                    # 4) usar el resultado DESPUÉS""",
    check=("En un acumulador, ¿dónde va `total = 0`?", [
        ("Antes del `for`", True, "Si va adentro, se reinicia en cada vuelta y solo queda el último valor."),
        ("Dentro del `for`", False, "Se reiniciaría en cada iteración: bug clásico."),
        ("Después del `for`", False, "El loop ya habría usado `total` sin inicializar."),
    ])),

concept("py-while", "Loop while", "while condición · contador · break",
    problem="Repetir **mientras** se cumpla una condición, cuando no sabés de antemano cuántas vueltas hacen falta.",
    when="Simulaciones ('¿cuántas semanas hasta que el stock baje de 30?'), reintentos, leer hasta que se acaben los datos.",
    signals=["'hasta que', 'mientras', '¿cuántas veces hace falta…?'", "Reintentar algo un máximo de N veces"],
    can=["Repetir hasta alcanzar una meta", "Contar iteraciones", "Cortar antes con `break`"],
    cant=["Terminar solo: si la condición nunca se vuelve False, es un **bucle infinito**", "Ser la mejor opción para recorrer una lista conocida (ahí va `for`)"],
    nomemo="Una regla: dentro del while algo tiene que **acercar** la condición a False (actualizar la variable que se evalúa).",
    ai="«Quiero simular cuántas semanas tarda un stock de 120 unidades en bajar de 30 si cae 15% por semana. Explicame cómo evitar un bucle infinito.»",
    verify="Imprimí la variable en cada vuelta las primeras veces para ver que efectivamente cambia.",
    example="""ahorro, meses = 1000, 0
while ahorro < 1500:
    ahorro = ahorro * 1.05      # algo cambia en cada vuelta
    meses += 1""",
    check=("¿Qué causa un bucle infinito en un `while`?", [
        ("Que la condición nunca se vuelva False", True, "Por ejemplo, si olvidás actualizar la variable que se evalúa."),
        ("Usar `break`", False, "break justamente corta el loop."),
        ("Recorrer una lista", False, "Eso es un for, que termina solo."),
    ])),

concept("py-func", "Funciones: parámetros y return", "def · parámetros · valores por defecto · return",
    problem="**Empaquetar** una lógica con un nombre para reutilizarla, probarla por separado y cambiarla en un solo lugar.",
    when="Repetís la misma lógica en varios lugares, o un paso de tu análisis merece un nombre propio (limpiar_precio, calcular_ingreso).",
    signals=["Copiaste y pegaste el mismo bloque 2+ veces", "Una regla que puede cambiar (tasa de IVA)", "Querés aplicar una transformación a cada fila (luego: `apply` en pandas)"],
    can=["Recibir datos por parámetros, con valores por defecto: `def f(precio, iva=0.21)`", "Devolver resultados con `return` (incluso varios, como tupla)", "Probar con casos chicos: `f(100) == 121`"],
    cant=["Devolver algo si no hay `return`: devuelve `None`", "`print` no es `return`: mostrar ≠ devolver"],
    nomemo="No hace falta memorizar *args/**kwargs ni decoradores para Data Science inicial. Sí: parámetros, defaults y return.",
    ai="«Quiero una función que aplique un descuento a un precio, con 10% por defecto. Antes del código, decime qué parámetros tendría, qué devolvería y 3 casos de prueba.»",
    verify="Escribí 2-3 llamadas de prueba con resultados conocidos: `aplicar_descuento(100) == 90`.",
    example="""def precio_final(precio, iva=0.21):
    return round(precio * (1 + iva), 2)

precio_final(100)          # 121.0
precio_final(100, iva=0.1) # 110.0""",
    check=("Una función hace `print(total)` pero no tiene `return`. ¿Qué vale `x = funcion()`?", [
        ("`None`", True, "Sin return, la función devuelve None aunque haya mostrado algo en pantalla."),
        ("El total", False, "print solo muestra; no devuelve."),
        ("Un error", False, "No falla: devuelve None silenciosamente (y el error aparece más adelante)."),
    ])),

concept("py-comp", "Comprensiones", "[expr for x in datos if cond] · {k: v for ...}",
    problem="Construir una lista o diccionario nuevo **transformando y/o filtrando** otro, en una línea legible.",
    when="El loop solo sirve para armar una colección nueva ('los ingresos de cada venta', 'los productos caros').",
    signals=["'una lista con … de cada …'", "'solo los que cumplen…'", "Un for de 3 líneas que solo hace append"],
    can=["Transformar: `[v * 1.21 for v in precios]`", "Filtrar: `[v for v in ventas if v > 1000]`", "Armar diccionarios: `{k: round(v, 2) for k, v in d.items()}`"],
    cant=["Mejorar la legibilidad si la lógica es larga (ahí, un for normal es mejor)", "Acumular un total (para eso: `sum(...)` o un for)"],
    nomemo="Leela como una oración: '**qué** guardo · **para cada** x en datos · **si** se cumple…'.",
    ai="«Tengo este for que arma una lista con append. ¿Cómo sería como comprensión? Explicame cómo leerla.»",
    verify="Compará con el for equivalente: deben dar la misma lista (`==`).",
    example="""celsius = [21.5, 30.0, 18.2]
fahrenheit = [c * 9 / 5 + 32 for c in celsius]
calurosos = [c for c in celsius if c > 25]
dobles = {k: v * 2 for k, v in {"a": 1, "b": 2}.items()}""",
    check=("¿Qué devuelve `[x * 2 for x in [1, 2, 3] if x > 1]`?", [
        ("`[4, 6]`", True, "Filtra primero (2 y 3) y luego transforma (×2)."),
        ("`[2, 4, 6]`", False, "El 1 no pasa el filtro x > 1."),
        ("`[1, 2, 3, 4, 6]`", False, "La comprensión arma una lista nueva solo con los transformados."),
    ])),

concept("py-errores", "Errores y excepciones", "traceback · try / except · raise",
    problem="**Leer** qué salió mal (el traceback te dice tipo de error y línea) y **manejar** datos inválidos sin que el programa se caiga.",
    when="Siempre que algo falla (leer el error) y cuando procesás datos externos que pueden venir rotos ('n/d', vacíos).",
    signals=["Aparece un traceback rojo", "Datos con valores inválidos que querés saltear o contar", "Conversión de tipos que puede fallar"],
    can=["Identificar el tipo de error: `KeyError`, `TypeError`, `ValueError`, `IndexError`…", "Capturar un error **específico**: `except ValueError:`", "Decidir qué hacer con el dato inválido (None, saltearlo, registrarlo)"],
    cant=["Arreglar el dato: `try/except` solo evita la caída", "Usar `except:` a secas sin esconder bugs reales (mala práctica)"],
    nomemo="No memorices la lista de excepciones. Aprendé a leer la **última línea** del traceback: tipo + mensaje.",
    ai="«Me aparece `ValueError: could not convert string to float: 'n/d'` en la línea 4. Explicame qué significa y qué opciones tengo para manejarlo, sin reescribir todo mi código.»",
    verify="Probá a propósito con un valor inválido y confirmá que el resultado es el que decidiste (None, se saltea, se cuenta).",
    example="""def edad_valida(texto):
    try:
        return int(texto)
    except ValueError:      # solo el error que esperamos
        return None

edad_valida("34"), edad_valida("sin dato")   # (34, None)""",
    check=("¿Qué parte del traceback conviene leer primero?", [
        ("La última línea: tipo de error y mensaje", True, "Ahí está el qué (KeyError: 'precio'). Las líneas de arriba dicen el dónde."),
        ("La primera línea", False, "Suele decir 'Traceback (most recent call last)', sin información útil."),
        ("Ninguna: conviene pedirle a la IA que lo arregle", False, "Primero entendé el error; después, si hace falta, pedí ayuda con contexto."),
    ])),

concept("py-imports", "Módulos e imports", "import x · from x import y · biblioteca estándar",
    problem="Usar código que ya existe (de Python o de otros) en lugar de escribirlo desde cero: estadística, fechas, archivos, pandas, NumPy.",
    when="Antes de programar algo genérico (mediana, fechas, leer JSON), preguntate: ¿ya existe un módulo?",
    signals=["La tarea es genérica y común", "Necesitás fechas, matemáticas, aleatoriedad, CSV/JSON", "Errores `ModuleNotFoundError` o `NameError: name 'pd' is not defined`"],
    can=["Importar módulos: `import statistics`", "Importar partes: `from datetime import date`", "Usar alias convencionales: `import pandas as pd`, `import numpy as np`"],
    cant=["Usar un módulo sin importarlo antes", "Usar un paquete no instalado (en tu PC: `pip install`)", "Saber de memoria qué hay en cada módulo (se consulta)"],
    nomemo="Recordá los alias estándar (`pd`, `np`, `plt`, `sns`) y que la biblioteca estándar trae mucho (statistics, datetime, csv, json, math, random).",
    ai="«¿Existe en la biblioteca estándar de Python algo para calcular la mediana? Mostrame cómo importarlo y usarlo con una lista.»",
    verify="Compará el resultado del módulo con un cálculo manual en un caso pequeño.",
    example="""import statistics
from datetime import date

statistics.median([3, 1, 100])      # 3 (robusta a valores extremos)
(date(2024, 3, 5) - date(2024, 3, 1)).days   # 4""",
    check=("Escribís `pd.DataFrame(...)` y aparece `NameError: name 'pd' is not defined`. ¿Qué falta?", [
        ("`import pandas as pd`", True, "El alias pd solo existe después del import."),
        ("Instalar Python de nuevo", False, "El error dice que el nombre no está definido, no que falte Python."),
        ("Usar `print`", False, "No tiene relación."),
    ])),

concept("py-archivos", "Trabajar con archivos", "open() · with · csv · json",
    problem="Leer datos guardados en archivos (CSV, JSON, texto) y escribir resultados.",
    when="Los datos no están en el código sino en un archivo, o querés guardar/compartir un resultado.",
    signals=["'Te pasan un archivo…'", "Configuración en JSON", "Exportar un reporte"],
    can=["Abrir con `with open(ruta, encoding='utf-8') as f:` (se cierra solo)", "Leer CSV con `csv.DictReader` (cada fila como diccionario)", "Leer/escribir JSON con `json.load` / `json.dump`"],
    cant=["Convertir tipos solo: **csv lee todo como texto**", "Leer Excel con la biblioteca estándar (usá pandas)", "Encontrar archivos si la ruta está mal (`FileNotFoundError`)"],
    nomemo="En Data Science, para tablas usarás `pd.read_csv`. Pero entender que un archivo es texto que hay que interpretar te evita muchos errores.",
    ai="«Tengo un CSV con columnas fecha,producto,cantidad,precio. ¿Cómo lo leo con el módulo csv para sumar cantidad × precio? Remarcá dónde hay que convertir tipos.»",
    verify="Contá las filas leídas y compará con el archivo; imprimí la primera fila para ver los tipos.",
    example="""import csv
with open("clientes.csv", encoding="utf-8") as f:   # (archivo de ejemplo)
    filas = list(csv.DictReader(f))
filas[0]   # {'nombre': 'Ana', 'edad': '34'} ← ¡la edad es texto!""",
    check=("Leés un CSV con `csv.DictReader`. ¿De qué tipo es el valor de `fila['cantidad']`?", [
        ("`str`, aunque se vea como número", True, "El módulo csv no convierte tipos: hay que usar int()/float()."),
        ("`int`", False, "Solo si lo convertís vos."),
        ("Depende del valor", False, "Siempre es texto con el módulo csv."),
    ])),

concept("py-leer", "Leer código y debuggear", "trazar · print() · casos chicos · aislar",
    problem="Entender qué hace un código (tuyo, de otra persona o de una IA) y encontrar por qué no hace lo que esperás.",
    when="Siempre que uses código que no escribiste vos, o que algo dé un resultado incorrecto **sin** error.",
    signals=["El código corre pero el resultado no tiene sentido", "Te dieron código y no sabés qué hace cada línea", "Un resultado es None o vacío inesperadamente"],
    can=["Trazar a mano: seguir el valor de cada variable línea por línea", "Imprimir valores intermedios y sus tipos", "Reducir el problema a un caso chico con respuesta conocida", "Cambiar una cosa por vez y observar"],
    cant=["Encontrar un bug lógico solo mirando por encima: hay que **verificar valores**", "Confiar en código que no ejecutaste ni probaste"],
    nomemo="El método importa más que cualquier herramienta: hipótesis → caso chico → observar → corregir → volver a probar.",
    ai="«Este código da 0 cuando esperaba 5359. No me lo arregles: haceme preguntas o sugerime qué imprimir para encontrar el error yo.»",
    verify="Tené siempre un caso de prueba con resultado conocido de antemano.",
    example="""total = 0
for v in ventas[:2]:                 # 1) caso chico
    ingreso = v["cantidad"] * v["precio"]
    print(v["producto"], ingreso, type(ingreso))   # 2) observar
    total += ingreso
print(total)                         # 3) ¿coincide con la cuenta a mano?""",
    check=("Tu código no da error pero el resultado es incorrecto. ¿Primer paso razonable?", [
        ("Probar con un caso chico conocido e imprimir valores intermedios", True, "Así aislás en qué paso se desvía el resultado."),
        ("Pedirle a la IA que lo reescriba completo", False, "Puede 'funcionar' sin que entiendas el error, y lo repetirás."),
        ("Agregar try/except", False, "No hay excepción: el problema es de lógica."),
    ])),

concept("py-datos", "Python aplicado a datos", "lista de dicts = tabla · agrupar · ordenar con key",
    problem="Responder preguntas de datos (totales por grupo, rankings, filtros) combinando las piezas de Python. Es exactamente lo que después pandas hace en una línea.",
    when="Datasets chicos, scripts de automatización, o para entender qué hace pandas por dentro.",
    signals=["'por producto', 'por categoría', 'top 3', 'el más vendido'", "Datos como lista de diccionarios (filas) o JSON de una API"],
    can=["Agrupar con un dict acumulador", "Ordenar por un campo: `sorted(items, key=lambda x: x[1], reverse=True)`", "Filtrar y transformar con comprensiones", "Pasar a pandas: `pd.DataFrame(ventas)`"],
    cant=["Escalar cómodamente a millones de filas o a joins complejos (ahí: pandas)", "Hacer gráficos sin librerías"],
    nomemo="Lo valioso es **diseñar el plan**: qué agrupo, qué agrego, cómo ordeno. Ese plan se traduce igual a pandas.",
    ai="«Quiero el top 3 de productos por ingreso a partir de una lista de diccionarios. Primero explicame el plan en pasos (agrupar, ordenar, cortar) y después el código.»",
    verify="La suma de los totales por grupo debe dar el total general.",
    example="""goles = [{"jugador": "Ana", "goles": 2}, {"jugador": "Eva", "goles": 1}, {"jugador": "Ana", "goles": 3}]
por_jugador = {}
for g in goles:
    por_jugador[g["jugador"]] = por_jugador.get(g["jugador"], 0) + g["goles"]
ranking = sorted(por_jugador.items(), key=lambda par: par[1], reverse=True)""",
    check=("Tenés `ventas` como lista de diccionarios. ¿Qué te da `pd.DataFrame(ventas)`?", [
        ("Una tabla: cada dict es una fila y cada clave una columna", True, "Lista de dicts = filas. Por eso esta estructura es el puente natural a pandas."),
        ("Una sola columna con diccionarios", False, "pandas reconoce las claves como columnas."),
        ("Un error", False, "Es una de las formas más comunes de crear un DataFrame."),
    ])),
]

EXERCISES = [
# ======================================================================== S1 Variables, tipos y números
A("py-a01", S1, "Un precio que llega como texto", 1, ["py-variables"],
  "Leíste un archivo y la columna `precio` llegó como `'1200.50'` (con comillas). Necesitás sumar todos los precios. **¿Qué tenés que resolver primero?**",
  [("Convertir el tipo: de texto (str) a número (float)", True, "Con texto, `+` concatena y `*` repite. Primero hay que convertir."),
   ("Ordenar los precios", False, "Ordenar no cambia el tipo: seguirían siendo textos."),
   ("Usar un loop while", False, "El problema no es cómo recorrer, sino el tipo de dato."),
   ("Guardarlos en un set", False, "Un set eliminaría precios repetidos y seguirían siendo texto.")],
  explain="Antes de cualquier cálculo con datos externos, preguntate **qué tipo** tiene cada valor. Un número entre comillas es texto."),

D("py-d01", S1, "¿Cuánto paga el cliente?", 2, ["py-numeros", "py-variables"],
  "Un cliente compró **3 mouse a $25.5** cada uno. Tiene un **10% de descuento** sobre el subtotal. Calculá cuánto paga en total y guardalo en `resultado`.",
  "precio_unitario = 25.5\ncantidad = 3\ndescuento = 0.10\n\nresultado = ",
  "precio_unitario = 25.5\ncantidad = 3\ndescuento = 0.10\n\nsubtotal = precio_unitario * cantidad\nresultado = subtotal * (1 - descuento)",
  hints=["Pensá el problema en dos pasos: primero cuánto sale sin descuento, después cuánto se descuenta.",
         "Subtotal = precio × cantidad. Pagar con 10% de descuento es pagar el 90% del subtotal.",
         "¿Cómo expresás 'el 90%' con la variable `descuento`? (pista: 1 − algo)"],
  explain="Se calcula el subtotal (precio × cantidad) y se aplica el descuento multiplicando por `(1 - descuento)`, que representa la parte que sí se paga.",
  pseudo="subtotal ← precio_unitario × cantidad\nresultado ← subtotal × (1 − descuento)",
  verify="A mano: 3 × 25.5 = 76.5; el 90% de 76.5 es 68.85."),

E("py-e01", S1, "El total que no tiene sentido", 2, ["py-variables"],
  "Este código debería calcular el total de 2 unidades de un producto, pero el resultado es rarísimo. Ejecutalo, mirá qué devuelve y corregilo.",
  "precio = \"1200.50\"   # llegó así desde un formulario\ncantidad = 2\n\nresultado = precio * cantidad",
  "precio = \"1200.50\"   # llegó así desde un formulario\ncantidad = 2\n\nresultado = float(precio) * cantidad",
  detect=("¿Cuál es el problema?", [
      ("`precio` es un texto, así que `*` repite el texto en vez de multiplicar", True, "`'1200.50' * 2` da `'1200.501200.50'`."),
      ("`cantidad` debería ser decimal", False, "Multiplicar por un int está bien; el problema es el otro operando."),
      ("Falta redondear", False, "El resultado ni siquiera es un número."),
  ]),
  why="En Python, `str * int` **repite** el texto. No hay error, por eso es un bug silencioso: el resultado es `'1200.501200.50'`. Hay que convertir `precio` a número con `float()` antes de calcular.",
  hints=["Ejecutá el código y mirá el resultado: ¿es un número?", "Fijate el tipo de cada variable. ¿Qué tipo tiene algo escrito entre comillas?", "¿Qué función convierte un texto con decimales a número?"],
  pseudo="convertir precio a número decimal\nresultado ← precio_numérico × cantidad"),

B("py-b01", S1, "Sí/No como texto o como booleano", 2, ["py-variables", "py-bool"],
  "Un dataset de clientes trae la columna `activo` con los textos `'Sí'` y `'No'`. Alguien propone convertirla a `True`/`False` antes de analizar. **¿Por qué conviene? ¿Qué podría salir mal si se deja como texto?** Explicalo con tus palabras.",
  model="Con booleanos se puede **filtrar** directamente (`if activo:`), **contar** (True suma 1, así que `sum(activos)` da la cantidad de activos) y calcular **proporciones** (`sum / len`). Como texto, cada comparación depende de que esté escrito exactamente igual: `'Sí'`, `'si'`, `'SI'` o `'Si '` serían valores distintos y los conteos darían mal. Además, `'No'` como texto es un string no vacío, que Python trata como True en un `if`: un bug silencioso.",
  checklist=["Mencioné que con booleanos se puede contar/sumar o filtrar fácil", "Mencioné el riesgo de variantes de escritura ('Sí', 'si', 'SI ')", "Mencioné que un texto no vacío como 'No' se evalúa como True en un if", "Propuse cómo convertir o validar los valores"],
  hints=["Pensá qué operaciones querrías hacer con esa columna (contar activos, filtrar…).", "¿Qué pasa si alguien escribió 'si' sin tilde o 'SI'?", "¿Cómo evalúa Python `if 'No':`? Probalo mentalmente: ¿es un texto vacío?"]),

# ======================================================================== S2 Strings
A("py-a02", S2, "El mismo cliente escrito de tres formas", 1, ["py-strings"],
  "En tu lista de clientes aparecen `'  ana  '`, `'ANA'` y `'Ana '`. Querés contarlos como la **misma persona**. ¿Qué necesitás?",
  [("Normalizar el texto: quitar espacios y unificar mayúsculas", True, "Con `.strip().lower()` (o `.title()`) las tres versiones quedan iguales."),
   ("Redondear los valores", False, "round() es para números."),
   ("Un diccionario de sinónimos escrito a mano", False, "Funcionaría, pero no escala: normalizar resuelve el caso general."),
   ("Ordenar alfabéticamente", False, "Ordenar no unifica las variantes.")]),

D("py-d02", S2, "Normalizar un nombre", 2, ["py-strings"],
  "El nombre de una clienta llegó como `'  carla GÓMEZ '`. Dejalo como `'Carla Gómez'` (sin espacios sobrantes, cada palabra con mayúscula inicial) y guardalo en `resultado`.",
  "nombre = \"  carla GÓMEZ \"\n\nresultado = ",
  "nombre = \"  carla GÓMEZ \"\n\nresultado = nombre.strip().title()",
  hints=["Hay dos problemas distintos en el texto. ¿Cuáles son?", "Uno son los espacios en los bordes; el otro, las mayúsculas mezcladas.", "¿Qué método quita espacios en los extremos y cuál pone mayúscula inicial a cada palabra? Se pueden encadenar."],
  explain="Se encadenan dos transformaciones: primero quitar los espacios de los extremos y después poner en formato título. Cada método devuelve un string nuevo, por eso se pueden encadenar.",
  pseudo="sin_espacios ← quitar espacios de los extremos de nombre\nresultado ← poner mayúscula inicial en cada palabra de sin_espacios"),

D("py-d03", S2, "Una línea de reporte", 3, ["py-strings", "py-numeros"],
  "Armá el texto de una línea de reporte con el formato exacto `'Monitor: $1,234.50'` a partir de las variables `producto` y `total` (separador de miles con coma y siempre 2 decimales). Guardalo en `resultado`.",
  "producto = \"Monitor\"\ntotal = 1234.5\n\nresultado = ",
  "producto = \"Monitor\"\ntotal = 1234.5\n\nresultado = f\"{producto}: ${total:,.2f}\"",
  hints=["Necesitás insertar valores de variables dentro de un texto. ¿Qué herramienta de strings sirve para eso?", "Los f-strings permiten escribir `f'{variable}'`. Además aceptan un formato después de `:`.", "Buscá (o pedile a la IA) el formato para 'separador de miles y 2 decimales' dentro de un f-string."],
  explain="Un f-string inserta variables en un texto. Dentro de las llaves, después de `:`, se indica el formato: `,` agrega separador de miles y `.2f` fija dos decimales.",
  pseudo="resultado ← texto con: producto + ': $' + total con separador de miles y 2 decimales",
  verify="Compará carácter por carácter con 'Monitor: $1,234.50'."),

F("py-f01", S2, "La IA parte una línea de CSV", 3, ["py-strings", "py-variables"],
  "Necesitás calcular el ingreso de una línea de texto tomada de un CSV: `'2024-03-01,Laptop,1,1200'` (fecha, producto, cantidad, precio). Le pediste ayuda a una IA y respondió con el código de abajo. **Antes de usarlo, tenés que entenderlo.**",
  prompt="Tengo una línea de texto de un CSV: '2024-03-01,Laptop,1,1200' (fecha, producto, cantidad, precio). Quiero calcular cantidad × precio en Python puro. Mostrame el código y explicame por qué cada conversión es necesaria.",
  bad_prompt="Haceme el ejercicio del CSV.",
  ai_code="linea = \"2024-03-01,Laptop,1,1200\"\n\npartes = linea.split(\",\")\nfecha, producto, cantidad, precio = partes\nresultado = int(cantidad) * float(precio)",
  questions=[
      ask("¿Qué devuelve `linea.split(',')`?", [("Una lista de 4 textos", True, "['2024-03-01', 'Laptop', '1', '1200']: todos str."), ("Una lista con números ya convertidos", False, "split no convierte tipos."), ("Una tupla", False, "Devuelve una lista.")]),
      ask("¿Por qué se usan `int()` y `float()`?", [("Porque las partes son texto y hay que convertirlas para multiplicar", True, "Sin convertir, '1' * '1200' daría TypeError."), ("Para redondear", False, "No redondean: convierten."), ("Son opcionales", False, "Sin ellas, el cálculo falla.")]),
      ask("¿Qué pasaría si la línea tuviera 5 campos en vez de 4?", [("`ValueError`: hay más valores que variables para desempaquetar", True, "`a, b, c, d = [5 elementos]` falla: too many values to unpack."), ("Ignora el quinto", False, "Python no ignora valores al desempaquetar."), ("Funciona igual", False, "Las cantidades deben coincidir.")]),
      ask("Si el archivo usara `;` como separador, ¿qué cambiarías y qué pasaría si no lo cambiás?", model="Habría que usar `split(';')`. Si se deja `split(',')`, la línea no se parte (queda una lista de 1 elemento) y el desempaquetado da `ValueError: not enough values to unpack`."),
  ],
  hints=["Leé el código de arriba hacia abajo y anotá el tipo de cada variable.", "Ejecutalo y agregá un `print(partes)` para ver qué contiene.", "Probá cambiar la línea por una con 5 campos y observá el error."],
  explain="`split` separa el texto por comas y devuelve una lista de strings. El desempaquetado asigna cada parte a una variable. Como todo es texto, hay que convertir cantidad y precio a números antes de multiplicar.",
  solution="linea = \"2024-03-01,Laptop,1,1200\"\n\npartes = linea.split(\",\")\nfecha, producto, cantidad, precio = partes\nresultado = int(cantidad) * float(precio)"),

# ======================================================================== S3 Listas, tuplas y sets
A("py-a03", S3, "Ventas de una semana", 1, ["py-listas"],
  "Tenés el total vendido de cada día de la semana, en orden. Querés el máximo, el promedio y poder agregar el día de hoy. ¿Qué estructura usarías?",
  [("Una lista", True, "Ordenada, admite agregar con append y funciona con sum, len y max."),
   ("Un set", False, "Perdería el orden y eliminaría días con el mismo total."),
   ("Una tupla", False, "No se puede agregar elementos a una tupla."),
   ("Un string", False, "Habría que partirlo y convertirlo cada vez.")]),

D("py-d04", S3, "Resumen de la semana", 2, ["py-listas", "py-numeros"],
  "Con `ventas_semana` (ya cargada: ventas de lunes a domingo), armá un resumen como **lista** con tres valores: `[máximo, mínimo, promedio redondeado a 2 decimales]`. Guardalo en `resultado`.",
  "print(ventas_semana)\n\nresultado = ",
  "maximo = max(ventas_semana)\nminimo = min(ventas_semana)\npromedio = round(sum(ventas_semana) / len(ventas_semana), 2)\nresultado = [maximo, minimo, promedio]",
  hints=["Separá el problema en tres cálculos independientes.", "Python trae funciones integradas para el máximo, el mínimo, la suma y la cantidad de elementos.", "El promedio es suma ÷ cantidad. ¿Qué función redondea a 2 decimales?"],
  explain="max() y min() devuelven los extremos. El promedio es la suma dividida por la cantidad de elementos; se redondea solo al final, para mostrar.",
  pseudo="máximo ← mayor valor de ventas_semana\nmínimo ← menor valor\npromedio ← redondear(suma / cantidad, 2)\nresultado ← [máximo, mínimo, promedio]"),

D("py-d05", S3, "Solo el fin de semana", 2, ["py-listas"],
  "Quedate con las ventas del **fin de semana** (los dos últimos días de `ventas_semana`) y guardalas en `resultado` como lista. Tu código debería seguir funcionando aunque la lista tuviera más semanas al principio.",
  "resultado = ",
  "resultado = ventas_semana[-2:]",
  hints=["Necesitás un **tramo** de la lista, no un solo elemento.", "Si contás desde el final, ¿en qué posición empieza el tramo?", "Los índices negativos cuentan desde el final. ¿Cómo se escribe 'desde el anteúltimo hasta el final' con slicing?"],
  explain="Con índices negativos se cuenta desde el final; `[-2:]` toma desde el anteúltimo hasta el final, sin importar el largo de la lista.",
  pseudo="resultado ← tramo de ventas_semana desde la posición −2 hasta el final"),

E("py-e02", S3, "El último día que no existe", 2, ["py-listas"],
  "Este código quiere obtener la venta del último día, pero falla. Encontrá el problema y corregilo **sin escribir el número de posición a mano**.",
  "ultimo = ventas_semana[len(ventas_semana)]\nresultado = ultimo",
  "ultimo = ventas_semana[-1]\nresultado = ultimo",
  detect=("¿Por qué falla?", [
      ("Las posiciones van de 0 a len−1: `len(lista)` se pasa por uno", True, "Con 7 elementos, las posiciones válidas son 0…6."),
      ("`len()` no funciona con listas", False, "len() funciona perfectamente con listas."),
      ("Falta convertir a int", False, "len() ya devuelve un int."),
  ]),
  why="Las posiciones empiezan en 0, así que el último elemento está en `len(lista) - 1`. `lista[len(lista)]` pide una posición inexistente → `IndexError: list index out of range`. La forma idiomática es `lista[-1]`.",
  hints=["Leé el mensaje de error: ¿qué tipo de error es?", "Si la lista tiene 7 elementos, ¿cuáles son sus posiciones válidas?", "Hay un índice especial que siempre apunta al último elemento."],
  pseudo="resultado ← último elemento de ventas_semana (índice −1)"),

A("py-a04", S3, "¿Cuántas categorías distintas?", 1, ["py-tuplas-sets"],
  "Tenés una lista con la categoría de cada una de **50.000 ventas** (con repetidos). Querés saber **cuántas categorías distintas** hay. ¿Qué herramienta es la más directa?",
  [("Convertirla a set y medir su largo", True, "`len(set(categorias))`: el set elimina duplicados."),
   ("Recorrerla con un for comparando cada elemento con todos los demás", False, "Funciona pero es lento y complejo para algo que el set resuelve directo."),
   ("Ordenarla", False, "Ordenar no elimina repetidos."),
   ("Una tupla", False, "Una tupla conserva los repetidos.")]),

D("py-d06", S3, "Categorías únicas y ordenadas", 2, ["py-tuplas-sets", "py-listas"],
  "A partir de `categorias_vendidas`, obtené la **lista** de categorías distintas **en orden alfabético**. Guardala en `resultado`.",
  "categorias_vendidas = [\"Audio\", \"Computación\", \"Audio\", \"Accesorios\", \"Computación\", \"Muebles\", \"Accesorios\"]\n\nresultado = ",
  "categorias_vendidas = [\"Audio\", \"Computación\", \"Audio\", \"Accesorios\", \"Computación\", \"Muebles\", \"Accesorios\"]\n\nresultado = sorted(set(categorias_vendidas))",
  hints=["Son dos necesidades: quitar repetidos y ordenar.", "Una estructura elimina repetidos pero no tiene orden; después hay que ordenar.", "¿Qué función devuelve una lista ordenada a partir de cualquier colección?"],
  explain="`set()` elimina los repetidos; como el set no tiene orden, `sorted()` lo convierte en una lista ordenada.",
  pseudo="únicas ← conjunto de categorias_vendidas (sin repetidos)\nresultado ← únicas ordenadas alfabéticamente (como lista)"),

A("py-a05", S3, "Devolver dos resultados juntos", 2, ["py-tuplas-sets", "py-func"],
  "Una función debe devolver el **mínimo y el máximo** de una serie de lecturas, juntos, y quien la usa no debería poder modificarlos por error. ¿Qué estructura es la más natural para devolverlos?",
  [("Una tupla: `return minimo, maximo`", True, "Agrupa valores fijos y se desempaqueta fácil: `mn, mx = f(datos)`."),
   ("Un set", False, "Si mínimo y máximo fueran iguales, quedaría uno solo, y no tiene orden."),
   ("Dos print()", False, "print muestra, no devuelve."),
   ("Una lista de listas", False, "Es más complicado de lo necesario.")]),

# ======================================================================== S4 Diccionarios
A("py-a06", S4, "Buscar precios rápido", 1, ["py-dict"],
  "Tenés un catálogo con **2.000 productos** y su precio, y durante el análisis necesitás buscar el precio de un producto **por su nombre** muchas veces. ¿Qué estructura conviene?",
  [("Un diccionario producto → precio", True, "Busca por clave directamente, sin recorrer todo."),
   ("Una lista de precios", False, "Tendrías que saber la posición de cada producto."),
   ("Una lista de tuplas (producto, precio)", False, "Para buscar, habría que recorrerla entera cada vez."),
   ("Un set de precios", False, "Perdés la relación con el nombre del producto.")]),

D("py-d07", S4, "Actualizar el catálogo", 2, ["py-dict"],
  "Actualizá el diccionario `precios`: agregá el producto `'Webcam'` a **60.0** y subí el precio del `'Mouse'` un **10%**. Guardá el diccionario actualizado en `resultado`.",
  "print(precios)\n\nresultado = precios",
  "precios[\"Webcam\"] = 60.0\nprecios[\"Mouse\"] = precios[\"Mouse\"] * 1.10\nresultado = precios",
  hints=["Son dos operaciones: una crea una clave nueva y otra modifica una existente.", "En un diccionario, asignar a una clave la crea si no existe o la reemplaza si existe.", "Para subir un 10%: ¿qué valor tenía el Mouse y por cuánto lo multiplicás?"],
  explain="Asignar a una clave nueva la agrega; asignar a una existente la reemplaza. Para el aumento, se lee el valor actual y se guarda multiplicado por 1.10.",
  pseudo="precios['Webcam'] ← 60.0\nprecios['Mouse'] ← precios['Mouse'] × 1.10\nresultado ← precios"),

E("py-e03", S4, "El precio que no aparece", 2, ["py-dict"],
  "Este código calcula el costo de 3 mouse, pero se rompe. Corregilo.",
  "costo = precios[\"mouse\"] * 3\nresultado = costo",
  "costo = precios[\"Mouse\"] * 3\nresultado = costo",
  detect=("¿Qué está mal?", [
      ("La clave está mal escrita: el diccionario tiene 'Mouse' con mayúscula", True, "Las claves distinguen mayúsculas."),
      ("No se puede multiplicar un valor de un diccionario", False, "Sí se puede: es un float."),
      ("Hay que usar un for", False, "No hace falta recorrer: se busca por clave."),
  ]),
  why="`KeyError: 'mouse'` significa que esa clave no existe. Las claves son sensibles a mayúsculas: el catálogo tiene `'Mouse'`. Con `print(precios.keys())` se ve rápido qué claves hay.",
  hints=["Leé el tipo de error y el valor que aparece entre comillas.", "Imprimí las claves del diccionario y comparalas con la que usás.", "¿'mouse' y 'Mouse' son la misma clave para Python?"],
  pseudo="costo ← precio de la clave exacta 'Mouse' × 3"),

C("py-c01", S4, "Plan: contar ventas por categoría (sin pandas)", 2, ["py-dict", "py-for"],
  "Querés saber **cuántas ventas hubo de cada categoría** a partir de la lista `ventas` (cada venta es un diccionario). Todavía no vas a escribir código: diseñá el plan.",
  [field("Datos que necesito de cada venta", "Solo la categoría.", ["La categoría", "El precio", "La fecha", "Todas las columnas"], 0),
   field("Estructura para guardar los conteos", "Un diccionario categoría → cantidad.", ["Un diccionario categoría → cantidad", "Una lista", "Un set", "Un string"], 0),
   field("Qué hago con cada venta", "Sumar 1 al contador de su categoría (empezando en 0 si es la primera vez).", ["Sumar 1 al contador de su categoría", "Sumar su precio", "Agregarla a una lista", "Nada"], 0),
   field("Resultado esperado", "Algo como {'Computación': 4, 'Accesorios': 3, 'Audio': 3}: un número por categoría que en total sume 10."),
   field("Cómo verifico", "La suma de todos los conteos debe ser igual a len(ventas)."),
  ],
  explain="Es el patrón **acumulador con diccionario**: recorrer, y por cada elemento incrementar el contador de su grupo. Es exactamente lo que después hace `value_counts()` o `groupby().size()` en pandas.",
  hints=["¿Qué dato de cada venta define a qué grupo pertenece?", "Necesitás una 'caja' por categoría donde ir contando.", "Cada vez que ves una venta, ¿qué le pasa al contador de su categoría?"],
  pseudo="conteo ← diccionario vacío\npara cada venta:\n    cat ← categoría de la venta\n    conteo[cat] ← conteo.get(cat, 0) + 1"),

# ======================================================================== S5 Condicionales
A("py-a07", S5, "Marcar ventas altas", 1, ["py-if"],
  "Cada venta debe quedar marcada como `'alta'` si supera los $500 y como `'normal'` en caso contrario. ¿Qué concepto necesitás?",
  [("Un condicional (if / else)", True, "La etiqueta depende de una condición."),
   ("Un set", False, "Sirve para valores únicos, no para decidir."),
   ("Un import", False, "No hace falta ningún módulo para esto."),
   ("Un while", False, "No hay que repetir hasta que algo pase; hay que decidir.")]),

D("py-d08", S5, "Clasificar montos en tramos", 3, ["py-if", "py-bool"],
  "Completá la función `clasificar_monto(monto)` para que devuelva:\n- `'alta'` si el monto es **500 o más**,\n- `'media'` si es **100 o más** (y menos de 500),\n- `'baja'` en otro caso.\n\nSe va a probar con varios montos, incluidos los bordes.",
  "def clasificar_monto(monto):\n    # tu lógica aquí\n    return \"baja\"",
  "def clasificar_monto(monto):\n    if monto >= 500:\n        return \"alta\"\n    elif monto >= 100:\n        return \"media\"\n    else:\n        return \"baja\"",
  hints=["Dibujá una recta numérica con los cortes 100 y 500: ¿qué tramo va a cada lado?", "Conviene preguntar primero por el tramo más alto; si no se cumple, por el siguiente.", "¿Con qué operador incluís el borde (500 es 'alta')?"],
  explain="Se evalúan las condiciones de la más exigente a la menos exigente. Como solo se ejecuta la primera que se cumple, la rama `media` ya sabe que el monto es menor a 500.",
  pseudo="si monto ≥ 500 → 'alta'\nsi no, si monto ≥ 100 → 'media'\nsi no → 'baja'",
  check={"custom": "clasificar_monto(750) == 'alta' and clasificar_monto(500) == 'alta' and clasificar_monto(499.9) == 'media' and clasificar_monto(100) == 'media' and clasificar_monto(99.99) == 'baja' and clasificar_monto(0) == 'baja'",
         "custom_msg": "Probé con 750, 500, 499.9, 100, 99.99 y 0 y algún caso no da lo esperado. Revisá los bordes (≥)."},
  verify="Probá los bordes: 500 → 'alta', 499.9 → 'media', 100 → 'media', 99.99 → 'baja'."),

E("py-e04", S5, "La rama que nunca se ejecuta", 3, ["py-if"],
  "Esta función debería devolver `'muy alta'` para montos de más de 1000, pero nunca lo hace. Corregila.",
  "def nivel(monto):\n    if monto > 500:\n        return \"alta\"\n    elif monto > 1000:\n        return \"muy alta\"\n    else:\n        return \"normal\"",
  "def nivel(monto):\n    if monto > 1000:\n        return \"muy alta\"\n    elif monto > 500:\n        return \"alta\"\n    else:\n        return \"normal\"",
  detect=("¿Por qué nunca devuelve 'muy alta'?", [
      ("Todo monto > 1000 también es > 500, y esa condición se evalúa primero", True, "La primera condición verdadera gana; la segunda nunca llega a evaluarse."),
      ("Falta un else", False, "Ya hay un else."),
      ("`elif` no existe en Python", False, "elif existe y funciona."),
  ]),
  why="En un `if/elif`, solo se ejecuta la **primera** rama verdadera. Con 1500, `monto > 500` ya es True y devuelve 'alta'. Las condiciones más restrictivas tienen que ir **primero**.",
  hints=["Probá mentalmente la función con 1500: ¿qué condición se evalúa primero?", "¿1500 > 500 es verdadero?", "¿Qué pasa si invertís el orden de las condiciones?"],
  check={"custom": "nivel(1500) == 'muy alta' and nivel(800) == 'alta' and nivel(1000) == 'alta' and nivel(200) == 'normal'",
         "custom_msg": "Probé con 1500, 1000, 800 y 200. 1500 debe ser 'muy alta', 1000 y 800 'alta', 200 'normal'."},
  pseudo="si monto > 1000 → 'muy alta'\nsi no, si monto > 500 → 'alta'\nsi no → 'normal'"),

B("py-b02", S5, "Lecturas confiables de un sensor", 3, ["py-if", "py-bool"],
  "La lista `lecturas` viene de un sensor de temperatura ambiente. Tiene valores `None` (sin lectura), `-999.0` (código de error del sensor) y un `85.3`. Antes de calcular el promedio, **¿qué condiciones revisarías para decidir si una lectura es válida?** Explicá cada una y por qué.",
  model="Una lectura es válida si: 1) **no es None** (no hay dato, no se puede promediar); 2) **no es el código de error -999** (es un valor centinela, no una temperatura real); 3) está en un **rango físicamente plausible** para temperatura ambiente (por ejemplo entre -30 y 60 °C): 85.3 probablemente sea un pico/error. Hay que decidir explícitamente qué hacer con las inválidas (descartarlas y **contarlas** para reportarlo). Promediar sin filtrar daría un valor sin sentido (el -999 lo hunde).",
  checklist=["Descarto los None", "Descarto el código de error -999", "Propongo un rango plausible para detectar valores extremos como 85.3", "Digo qué hacer con las inválidas (descartar, contar, reportar)", "Explico cómo afectaría al promedio no filtrarlas"],
  hints=["Mirá la lista: ¿cuántos tipos de 'valor raro' ves?", "¿Un -999 grados es una temperatura real?", "¿Qué rango de temperaturas tiene sentido para un ambiente?"]),

# ======================================================================== S6 Loops
A("py-a08", S6, "Ingreso de cada venta y total", 1, ["py-for"],
  "Tenés una lista de ventas (cada una con cantidad y precio). Necesitás calcular el ingreso de cada venta y el total facturado. ¿Qué necesitás?",
  [("Un loop for con un acumulador", True, "Recorrés cada venta y vas sumando al total."),
   ("Un while sin condición", False, "Sería un bucle infinito."),
   ("Un set", False, "No permite recorrer acumulando montos por venta de forma natural… ni conserva duplicados."),
   ("Un if", False, "Decidir no alcanza: hay que repetir el cálculo para cada venta.")]),

D("py-d09", S6, "Total facturado", 2, ["py-for", "py-dict"],
  "Calculá el **total facturado** (suma de `cantidad × precio` de cada venta) de la lista `ventas` y guardalo en `resultado`.",
  "print(ventas[0])   # mirá cómo es una venta\n\nresultado = ",
  "total = 0\nfor v in ventas:\n    total += v[\"cantidad\"] * v[\"precio\"]\nresultado = total",
  hints=["¿Qué cálculo hacés con cada venta y qué hacés con ese resultado?", "Necesitás una variable que vaya acumulando, inicializada antes de recorrer.", "Dentro del for, ¿cómo accedés a la cantidad y al precio de una venta (que es un diccionario)?"],
  explain="Patrón acumulador: `total` empieza en 0 antes del loop; en cada vuelta se suma el ingreso de esa venta.",
  pseudo="total ← 0\npara cada venta en ventas:\n    total ← total + cantidad × precio\nresultado ← total",
  verify="Calculá a mano las dos primeras ventas (1200 + 76.5) y verificá que el loop las suma bien."),

D("py-d10", S6, "Ventas por categoría", 3, ["py-for", "py-dict", "py-datos"],
  "Implementá el plan del ejercicio de planificación: contá **cuántas ventas** hay de cada `categoria` en `ventas`. Guardá un diccionario `{categoría: cantidad_de_ventas}` en `resultado`.",
  "conteo = {}\n# recorré las ventas y contá\n\nresultado = conteo",
  "conteo = {}\nfor v in ventas:\n    cat = v[\"categoria\"]\n    conteo[cat] = conteo.get(cat, 0) + 1\nresultado = conteo",
  hints=["Ya tenés el plan: un diccionario como contador por categoría.", "La primera vez que aparece una categoría todavía no está en el diccionario: ¿cómo evitás el KeyError?", "`.get(clave, 0)` devuelve 0 si la clave no existe. Sumale 1 y guardalo."],
  explain="Por cada venta, se lee su categoría y se incrementa su contador. `.get(cat, 0)` resuelve el caso de la primera aparición.",
  pseudo="conteo ← {}\npara cada venta:\n    cat ← venta['categoria']\n    conteo[cat] ← conteo.get(cat, 0) + 1",
  verify="sum(resultado.values()) debe ser 10 (la cantidad de ventas)."),

G("py-g01", S6, "Transferencia: unidades por categoría", 3, ["py-for", "py-dict", "py-datos"], "py-d10",
  "Antes contabas **ventas** por categoría. Ahora querés las **unidades vendidas** (la suma de `cantidad`) por categoría.",
  "Calculá la suma de `cantidad` por `categoria` en `ventas`. Guardá el diccionario `{categoría: unidades}` en `resultado`.",
  "unidades = {}\n\nresultado = unidades",
  "unidades = {}\nfor v in ventas:\n    cat = v[\"categoria\"]\n    unidades[cat] = unidades.get(cat, 0) + v[\"cantidad\"]\nresultado = unidades",
  hints=["Compará con el ejercicio anterior: ¿qué parte del patrón cambia?", "La estructura y el recorrido son iguales; lo que cambia es **cuánto** sumás.", "En lugar de sumar 1, ¿qué valor de la venta tenés que sumar?"],
  explain="Mismo patrón acumulador; en vez de sumar 1 (contar), se suma la cantidad de la venta (agregar). Contar y sumar son dos agregaciones distintas sobre el mismo agrupamiento.",
  pseudo="unidades ← {}\npara cada venta:\n    unidades[cat] ← unidades.get(cat, 0) + venta['cantidad']"),

E("py-e05", S6, "El total que solo cuenta la última venta", 2, ["py-for", "py-leer"],
  "Este loop debería dar el total facturado de todas las ventas, pero da un número demasiado chico. Encontrá el error.",
  "for v in ventas:\n    total = 0\n    total += v[\"cantidad\"] * v[\"precio\"]\nresultado = total",
  "total = 0\nfor v in ventas:\n    total += v[\"cantidad\"] * v[\"precio\"]\nresultado = total",
  detect=("¿Qué está pasando?", [
      ("`total = 0` está dentro del loop: se reinicia en cada vuelta", True, "Al final solo queda el ingreso de la última venta (240)."),
      ("`+=` no funciona con floats", False, "Funciona perfectamente."),
      ("Falta un return", False, "No es una función."),
  ]),
  why="El acumulador se inicializa **dentro** del for, así que en cada iteración vuelve a 0 y solo sobrevive el último ingreso (3 × 80 = 240). Hay que inicializarlo una vez, **antes** del loop.",
  hints=["Ejecutalo: ¿a qué venta corresponde el número que da?", "Seguí el valor de `total` vuelta por vuelta: ¿qué le pasa al empezar cada iteración?", "¿Dónde debería inicializarse un acumulador?"],
  pseudo="total ← 0  (una sola vez, antes)\npara cada venta: total ← total + ingreso"),

A("py-a09", S6, "Reintentar una descarga", 2, ["py-while"],
  "Querés intentar descargar un archivo **hasta que funcione**, con un máximo de 3 intentos. No sabés de antemano cuántas veces hará falta. ¿Qué tipo de loop encaja mejor?",
  [("while (con un contador de intentos)", True, "Se repite mientras no haya éxito y queden intentos."),
   ("for sobre la lista de ventas", False, "No hay una colección para recorrer."),
   ("Una comprensión de lista", False, "Sirve para construir listas, no para reintentar."),
   ("Un if solo", False, "Un if decide una vez; no repite.")]),

D("py-d11", S6, "¿Cuántas semanas hasta reponer?", 3, ["py-while", "py-numeros"],
  "Un depósito tiene **120 unidades**. Cada semana el stock baja un **15%** (el nuevo stock es `int(stock * 0.85)`, que descarta decimales). ¿Cuántas semanas pasan hasta que el stock queda **por debajo de 30**? Guardá la cantidad de semanas en `resultado`.",
  "stock = 120\nsemanas = 0\n\nresultado = semanas",
  "stock = 120\nsemanas = 0\nwhile stock >= 30:\n    stock = int(stock * 0.85)\n    semanas += 1\nresultado = semanas",
  hints=["No sabés cuántas semanas son: hay que simular semana a semana.", "¿Mientras qué condición se sigue simulando?", "En cada vuelta tienen que cambiar dos cosas: el stock y el contador de semanas."],
  explain="Se simula semana a semana con un while: mientras el stock sea ≥ 30, se aplica la baja y se cuenta una semana más. Cuando cae por debajo de 30, la condición es False y el loop termina.",
  pseudo="mientras stock ≥ 30:\n    stock ← int(stock × 0.85)\n    semanas ← semanas + 1",
  verify="Imprimí el stock en cada vuelta: 102, 86, 73… hasta el primer valor < 30."),

# ======================================================================== S7 Funciones
A("py-a10", S7, "La tasa que cambia", 1, ["py-func"],
  "En tu notebook calculás el IVA en 6 lugares distintos con la misma fórmula. Cada vez que cambia la tasa tenés que editar los 6 lugares (y ya te olvidaste uno). ¿Qué concepto resuelve esto?",
  [("Una función con la tasa como parámetro", True, "La lógica vive en un solo lugar y se reutiliza."),
   ("Un set", False, "No tiene relación con reutilizar lógica."),
   ("Copiar y pegar con más cuidado", False, "El problema de fondo sigue: la lógica está duplicada."),
   ("Un while", False, "No se trata de repetir en un loop.")]),

D("py-d12", S7, "Descuento con valor por defecto", 3, ["py-func"],
  "Escribí la función `aplicar_descuento(precio, porcentaje=10)` que devuelva el precio con el descuento aplicado, **redondeado a 2 decimales**. Si no se indica porcentaje, se usa 10.",
  "def aplicar_descuento(precio, porcentaje=10):\n    pass",
  "def aplicar_descuento(precio, porcentaje=10):\n    return round(precio * (1 - porcentaje / 100), 2)",
  hints=["Primero pensá la fórmula con un ejemplo: 200 con 25% de descuento, ¿cuánto queda?", "El porcentaje viene como 25 (no 0.25): hay que dividirlo por 100.", "La función tiene que **devolver** el valor (no imprimirlo) y redondearlo."],
  explain="Se convierte el porcentaje a proporción (÷100), se calcula la parte que se paga (1 − proporción) y se devuelve redondeado. El valor por defecto en la firma permite llamarla sin el segundo argumento.",
  pseudo="función aplicar_descuento(precio, porcentaje = 10):\n    devolver redondear(precio × (1 − porcentaje / 100), 2)",
  check={"custom": "aplicar_descuento(100) == 90 and aplicar_descuento(200, 25) == 150 and aplicar_descuento(19.99, 15) == 16.99",
         "custom_msg": "Probé aplicar_descuento(100) → 90, aplicar_descuento(200, 25) → 150 y aplicar_descuento(19.99, 15) → 16.99. Revisá la fórmula, el return y el redondeo."},
  verify="Probá aplicar_descuento(100) == 90 y aplicar_descuento(200, 25) == 150."),

D("py-d13", S7, "Una función de resumen reutilizable", 3, ["py-func", "py-tuplas-sets"],
  "Escribí `resumen(valores)` que devuelva una **tupla** `(mínimo, máximo, promedio)` con el promedio redondeado a 2 decimales. Después usala con `ventas_semana` y guardá el resultado en `resultado`.",
  "def resumen(valores):\n    pass\n\nresultado = resumen(ventas_semana)",
  "def resumen(valores):\n    promedio = round(sum(valores) / len(valores), 2)\n    return min(valores), max(valores), promedio\n\nresultado = resumen(ventas_semana)",
  hints=["Ya calculaste estas tres métricas antes. ¿Qué cambia al ponerlas en una función?", "La función no debe usar `ventas_semana` adentro: tiene que trabajar con su parámetro `valores`.", "Para devolver tres valores juntos: `return a, b, c` (eso ya es una tupla)."],
  explain="La función recibe cualquier lista por parámetro, calcula las tres métricas y las devuelve juntas como tupla. Al no depender de una variable global, sirve para cualquier dataset.",
  pseudo="función resumen(valores):\n    devolver (mínimo(valores), máximo(valores), redondear(promedio, 2))",
  check={"custom": "resumen([1, 2, 3]) == (1, 3, 2.0) and resultado == (880, 2100, 1451.43)",
         "custom_msg": "resumen([1, 2, 3]) debe devolver (1, 3, 2.0) y resumen(ventas_semana) (880, 2100, 1451.43)."}),

E("py-e06", S7, "La función que 'calcula' pero no devuelve", 2, ["py-func"],
  "La función muestra el número correcto en pantalla, pero `resultado` queda vacío. Corregila.",
  "def ingreso(venta):\n    print(venta[\"cantidad\"] * venta[\"precio\"])\n\nresultado = ingreso(ventas[0])",
  "def ingreso(venta):\n    return venta[\"cantidad\"] * venta[\"precio\"]\n\nresultado = ingreso(ventas[0])",
  detect=("¿Cuál es el problema?", [
      ("Usa print en lugar de return: muestra el valor pero devuelve None", True, "Mostrar ≠ devolver."),
      ("El parámetro está mal escrito", False, "`venta` se usa correctamente."),
      ("`ventas[0]` no existe", False, "Es la primera venta de la lista."),
  ]),
  why="`print` muestra un valor en pantalla, pero la función no lo **devuelve**: sin `return`, toda función devuelve `None`. Por eso `resultado` queda en None aunque se vea el número.",
  hints=["Mirá la salida: el número aparece. ¿Y qué vale resultado?", "¿Qué devuelve una función que no tiene return?", "¿Qué palabra clave hace que una función entregue un valor a quien la llamó?"],
  pseudo="función ingreso(venta): devolver cantidad × precio"),

F("py-f02", S7, "La IA arma totales por cliente", 3, ["py-func", "py-dict", "py-for"],
  "Pediste una función que calcule cuánto gastó cada cliente. La IA respondió esto. Leelo, ejecutalo y respondé las preguntas.",
  prompt="Necesito una función en Python puro que reciba una lista de ventas (diccionarios con 'cliente', 'cantidad' y 'precio') y devuelva un diccionario cliente → total gastado. Explicá cada línea.",
  ai_code="def total_por_cliente(ventas):\n    totales = {}\n    for v in ventas:\n        monto = v[\"cantidad\"] * v[\"precio\"]\n        totales[v[\"cliente\"]] = totales.get(v[\"cliente\"], 0) + monto\n    return totales\n\nresultado = total_por_cliente(ventas)",
  questions=[
      ask("¿Qué tipo de objeto devuelve la función?", [("Un diccionario cliente → total", True, "`totales` es un dict y es lo que se devuelve."), ("Una lista de totales", False, "No se usa ninguna lista."), ("Un número", False, "Devuelve un total por cliente, no uno solo.")]),
      ask("¿Para qué sirve `totales.get(v['cliente'], 0)`?", [("Devuelve el total acumulado del cliente, o 0 si todavía no aparece", True, "Evita el KeyError en la primera venta de cada cliente."), ("Borra al cliente", False, "get solo lee."), ("Ordena los clientes", False, "No ordena nada.")]),
      ask("¿Qué pasaría si una venta no tuviera la clave 'cliente'?", [("`KeyError: 'cliente'`", True, "Acceder con corchetes a una clave inexistente falla."), ("Se ignora esa venta", False, "No hay ninguna lógica que la ignore."), ("Se suma a un cliente llamado None", False, "Eso pasaría solo con .get('cliente').")]),
      ask("¿Cómo verificarías que los totales son correctos sin revisarlos uno por uno?", model="Sumando todos los valores del diccionario (`sum(resultado.values())`) y comparando con el total facturado general (5359.0). Si coinciden, no se perdió ni duplicó ninguna venta."),
  ],
  hints=["Seguí el loop con las dos primeras ventas y anotá cómo cambia `totales`.", "Agregá un print dentro del for para ver el diccionario en cada vuelta.", "¿Qué devuelve .get cuando la clave no está?"],
  explain="Es el patrón acumulador con diccionario aplicado a dinero: por cada venta se calcula el monto y se suma al total de su cliente.",
  solution="def total_por_cliente(ventas):\n    totales = {}\n    for v in ventas:\n        monto = v[\"cantidad\"] * v[\"precio\"]\n        totales[v[\"cliente\"]] = totales.get(v[\"cliente\"], 0) + monto\n    return totales\n\nresultado = total_por_cliente(ventas)"),

# ======================================================================== S8 Comprensiones
A("py-a11", S8, "Una lista transformada en una línea", 2, ["py-comp"],
  "Necesitás una lista nueva con el precio **con IVA** de cada producto del catálogo, y querés escribirla en una sola línea legible. ¿Qué herramienta encaja?",
  [("Una comprensión de lista", True, "`[p * 1.21 for p in precios.values()]`."),
   ("Un while", False, "No hace falta controlar una condición de corte."),
   ("try/except", False, "No hay errores que manejar."),
   ("Un set", False, "Perdería precios repetidos.")]),

D("py-d14", S8, "Ingresos de cada venta", 2, ["py-comp"],
  "Armá una lista con el **ingreso** (`cantidad × precio`) de cada venta de `ventas`, en el mismo orden. Guardala en `resultado`.",
  "resultado = ",
  "resultado = [v[\"cantidad\"] * v[\"precio\"] for v in ventas]",
  hints=["Es un 'para cada venta, calculá algo y guardalo en una lista'.", "Podés escribirlo como un for con append, o como comprensión.", "Estructura: `[QUÉ_GUARDO for v in ventas]`. ¿Qué va en QUÉ_GUARDO?"],
  explain="La comprensión se lee: 'guardá cantidad × precio, para cada venta v en ventas'. Construye la lista nueva sin append.",
  pseudo="resultado ← [cantidad × precio de v, para cada v en ventas]"),

D("py-d15", S8, "Solo las ventas grandes", 3, ["py-comp", "py-bool"],
  "Obtené la lista de **nombres de producto** de las ventas cuyo ingreso (`cantidad × precio`) sea **mayor a 200**, en el orden en que aparecen. Guardala en `resultado`.",
  "resultado = ",
  "resultado = [v[\"producto\"] for v in ventas if v[\"cantidad\"] * v[\"precio\"] > 200]",
  hints=["Hay una transformación (quedarte con el nombre) y un filtro (ingreso > 200).", "En una comprensión el filtro va al final con `if`.", "`[lo_que_guardo for v in ventas if condición]`."],
  explain="La comprensión filtra (`if ingreso > 200`) y transforma (se queda solo con el nombre del producto).",
  pseudo="resultado ← [producto de v, para cada v en ventas, si cantidad × precio > 200]"),

G("py-g02", S8, "Transferencia: un diccionario con IVA", 3, ["py-comp", "py-dict"], "py-d14",
  "Antes armaste una **lista** transformando cada venta. Ahora querés un **diccionario** transformando cada par del catálogo.",
  "Creá un diccionario `{producto: precio_con_iva}` a partir de `precios`, con el IVA del 21% y redondeado a 2 decimales. Guardalo en `resultado`.",
  "resultado = ",
  "resultado = {p: round(precio * 1.21, 2) for p, precio in precios.items()}",
  hints=["¿Qué cambia respecto de la comprensión de lista?", "Para recorrer clave y valor a la vez: `.items()`.", "Una comprensión de diccionario usa llaves y `clave: valor`."],
  explain="La comprensión de diccionario recorre los pares (producto, precio) con `.items()` y arma pares nuevos `producto: precio_con_iva`.",
  pseudo="resultado ← {producto: redondear(precio × 1.21, 2), para cada (producto, precio) en precios}"),

B("py-b03", S8, "¿Cuándo NO usar una comprensión?", 3, ["py-comp", "py-leer"],
  "Las comprensiones son compactas. **¿En qué situaciones es mejor un `for` normal?** Dá al menos dos casos concretos y explicá por qué.",
  model="Conviene un for normal cuando: 1) la lógica tiene **varios pasos** o condiciones anidadas (la comprensión se vuelve ilegible); 2) hay que **acumular** algo (un total, un diccionario por grupo con .get) en lugar de construir una lista; 3) hay **efectos** como imprimir, escribir archivos o manejar errores con try/except; 4) necesitás **debuggear** con prints intermedios. La regla: si no se puede leer en voz alta como una oración, usá un for.",
  checklist=["Mencioné lógica compleja o con varios pasos", "Mencioné acumular (totales, conteos)", "Mencioné efectos: print, archivos, try/except", "Mencioné la legibilidad o el debugging"],
  hints=["Pensá en qué es lo único que hace una comprensión: construir una colección.", "¿Cómo pondrías un try/except dentro de una comprensión?", "¿Y si querés imprimir valores intermedios para debuggear?"]),

# ======================================================================== S9 Errores
A("py-a12", S9, "Precios con 'n/d'", 2, ["py-errores"],
  "Leés 10.000 precios de un archivo. Algunos dicen `'n/d'`. No querés que el programa se caiga: querés convertir los válidos y marcar los inválidos como `None`. ¿Qué concepto usás?",
  [("try / except ValueError al convertir", True, "Intentás convertir; si falla, decidís qué hacer."),
   ("Un while", False, "No resuelve la conversión que falla."),
   ("import statistics", False, "No maneja errores de conversión."),
   ("`except:` sin tipo para atrapar todo", False, "Funcionaría, pero escondería otros errores reales: mejor capturar el error específico.")]),

D("py-d16", S9, "Convertir sin caerse", 3, ["py-errores", "py-for"],
  "Convertí cada texto de `precios_texto` a `float`. Los que no se puedan convertir deben quedar como `None`. Guardá la lista resultante (mismo orden y largo) en `resultado`.",
  "precios_texto = [\"1200\", \"25.5\", \"n/d\", \"45\", \"\", \"300.0\"]\n\nresultado = []",
  "precios_texto = [\"1200\", \"25.5\", \"n/d\", \"45\", \"\", \"300.0\"]\n\nresultado = []\nfor t in precios_texto:\n    try:\n        resultado.append(float(t))\n    except ValueError:\n        resultado.append(None)",
  hints=["¿Qué pasa si hacés float('n/d')? Probalo.", "Para cada texto: intentar convertir; si falla, guardar None.", "¿Qué tipo de error lanza float() con un texto inválido? Ese es el que hay que capturar."],
  explain="Por cada texto se **intenta** convertir; si float() lanza ValueError, se captura y se agrega None. Así el programa no se cae y el dato inválido queda marcado.",
  pseudo="resultado ← []\npara cada texto:\n    intentar: agregar float(texto)\n    si ValueError: agregar None"),

E("py-e07", S9, "El except que no atrapa nada", 3, ["py-errores"],
  "Este código intenta manejar los precios inválidos, pero igual se cae. ¿Por qué?",
  "precios_texto = [\"1200\", \"n/d\", \"45\"]\nresultado = []\nfor t in precios_texto:\n    try:\n        resultado.append(float(t))\n    except KeyError:\n        resultado.append(None)",
  "precios_texto = [\"1200\", \"n/d\", \"45\"]\nresultado = []\nfor t in precios_texto:\n    try:\n        resultado.append(float(t))\n    except ValueError:\n        resultado.append(None)",
  detect=("¿Qué está mal?", [
      ("Captura KeyError, pero float('n/d') lanza ValueError", True, "Solo se atrapan las excepciones del tipo indicado."),
      ("try no se puede usar dentro de un for", False, "Sí se puede."),
      ("append no acepta None", False, "Una lista acepta cualquier valor."),
  ]),
  why="`except KeyError` solo atrapa KeyError. Convertir `'n/d'` a float lanza **ValueError**, que no coincide, así que la excepción sigue de largo y el programa se cae. Hay que leer el traceback para saber qué tipo de error capturar.",
  hints=["Ejecutalo y leé la última línea del error: ¿qué tipo de excepción es?", "¿Coincide con el tipo que dice el except?", "Cambiá el except por el tipo correcto."],
  pseudo="intentar convertir; capturar ValueError (el tipo que realmente ocurre)"),

A("py-a13", S9, "Leer un error", 1, ["py-errores", "py-dict"],
  "Al ejecutar un análisis aparece: `KeyError: 'precio'`. ¿Qué significa?",
  [("Se intentó acceder a una clave (o columna) 'precio' que no existe", True, "Revisá cómo se llama realmente: ¿'Precio'?, ¿'precio '?"),
   ("El precio es negativo", False, "KeyError no habla de valores, sino de claves."),
   ("Falta instalar una librería", False, "Eso sería ModuleNotFoundError."),
   ("El precio es texto", False, "Eso daría TypeError al operar.")]),

B("py-b04", S9, "Explicar un TypeError", 2, ["py-errores", "py-variables"],
  "Un compañero te muestra: `TypeError: unsupported operand type(s) for +: 'int' and 'str'` en la línea `total = total + fila['monto']`. **Explicale qué significa y qué revisaría primero**, sin darle el código corregido.",
  model="El error dice que se intentó **sumar un int con un str**: `total` es un número, pero `fila['monto']` es texto (seguramente leído de un archivo, donde todo llega como string). Python no suma número + texto. Revisaría primero el **tipo** de `fila['monto']` (`print(type(fila['monto']), repr(fila['monto']))`) y después lo convertiría con `float()`, contemplando valores vacíos o inválidos.",
  checklist=["Expliqué que se suma un número con un texto", "Identifiqué que fila['monto'] probablemente es str (viene de un archivo)", "Sugerí inspeccionar el tipo con type() o repr()", "Sugerí convertir con float() y pensar en valores inválidos"],
  hints=["Leé el mensaje: menciona dos tipos. ¿Cuáles?", "¿Cuál de las dos variables es el texto?", "¿De dónde suele venir un valor numérico escrito como texto?"]),

# ======================================================================== S10 Imports
A("py-a14", S10, "La mediana sin reinventar", 1, ["py-imports"],
  "Necesitás la **mediana** de una lista de lecturas. ¿Qué hacés?",
  [("Importar el módulo `statistics` de la biblioteca estándar", True, "`statistics.median(lista)`: ya existe y está probado."),
   ("Escribir tu propio algoritmo de ordenamiento", False, "Es reinventar algo que ya existe."),
   ("Usar un set", False, "Perdería valores repetidos y el orden."),
   ("Calcular el promedio", False, "Media y mediana son medidas distintas.")]),

D("py-d17", S10, "Media vs mediana con un pico", 3, ["py-imports", "py-comp"],
  "Las lecturas válidas de un sensor tienen un pico extraño (85.3). Usando el módulo `statistics`, calculá la **media** (redondeada a 2) y la **mediana** de `validas`, y guardá `[media, mediana]` en `resultado`. Después mirá la diferencia: ¿cuál representa mejor la temperatura típica?",
  "validas = [21.5, 22.1, 23.4, 22.8, 24.0, 85.3, 23.1]\n\nresultado = ",
  "import statistics\n\nvalidas = [21.5, 22.1, 23.4, 22.8, 24.0, 85.3, 23.1]\n\nresultado = [round(statistics.mean(validas), 2), statistics.median(validas)]",
  hints=["Necesitás un módulo: ¿cuál se ocupa de estadística básica?", "Primero importalo; después buscá (en la documentación o con la IA) cómo se llaman sus funciones de media y mediana.", "Guardá ambas en una lista: [media redondeada, mediana]."],
  explain="Se importa `statistics` y se usan `mean` y `median`. La media se 'arrastra' hacia el pico (31.74), mientras que la mediana (23.1) no se ve afectada: es más robusta ante valores extremos.",
  pseudo="importar statistics\nmedia ← redondear(mean(validas), 2)\nmediana ← median(validas)\nresultado ← [media, mediana]"),

F("py-f03", S10, "La IA usa fechas", 3, ["py-imports"],
  "Querés saber cuántos días pasaron entre la primera y la última venta. La IA te dio este código con dos imports. Analizalo.",
  prompt="Tengo una lista de ventas con fechas en texto 'AAAA-MM-DD'. ¿Cómo calculo cuántos días hay entre la primera y la última venta? Explicame qué módulo usás y por qué.",
  ai_code="from datetime import date\n\nfechas = [date.fromisoformat(v[\"fecha\"]) for v in ventas]\ndias = (max(fechas) - min(fechas)).days\nresultado = dias",
  questions=[
      ask("¿Qué diferencia hay entre `import datetime` y `from datetime import date`?", [("El segundo trae solo `date` y se usa sin prefijo", True, "Con `import datetime` habría que escribir `datetime.date.fromisoformat(...)`."), ("Ninguna", False, "Cambia cómo se escribe el nombre al usarlo."), ("El primero es más rápido", False, "No es una cuestión de velocidad.")]),
      ask("¿Por qué se convierte el texto con `date.fromisoformat`?", [("Para poder restar fechas y comparar correctamente", True, "Restar textos no tiene sentido; restar fechas da un intervalo."), ("Para que se vea más lindo", False, "Es para operar, no para mostrar."), ("No hace falta", False, "Con textos no se puede restar.")]),
      ask("¿Qué tipo de objeto es `max(fechas) - min(fechas)`?", [("Un intervalo de tiempo (timedelta), del que `.days` extrae los días", True, "Restar dos fechas da un timedelta."), ("Un int", False, "Por eso se necesita `.days`."), ("Un string", False, "No.")]),
      ask("Si una fecha viniera como '01/03/2024', ¿qué pasaría y cómo lo resolverías?", model="`fromisoformat` fallaría con ValueError porque espera el formato AAAA-MM-DD. Habría que usar `datetime.strptime(texto, '%d/%m/%Y')` (o normalizar el formato antes), y verificar con una fecha conocida."),
  ],
  hints=["Ejecutalo y agregá print(fechas) para ver qué tipo de objetos contiene.", "Buscá qué devuelve restar dos fechas.", "Probá cambiar una fecha por '01/03/2024' y observá el error."],
  explain="Las fechas en texto se convierten a objetos `date` para poder compararlas (max/min) y restarlas; la resta da un timedelta y `.days` extrae los días.",
  solution="from datetime import date\n\nfechas = [date.fromisoformat(v[\"fecha\"]) for v in ventas]\ndias = (max(fechas) - min(fechas)).days\nresultado = dias"),

# ======================================================================== S11 Archivos
A("py-a15", S11, "Procesar un CSV con Python puro", 1, ["py-archivos"],
  "Te pasan `ventas.csv` y necesitás procesarlo fila por fila en un script, **sin pandas**. ¿Qué herramientas usás?",
  [("`open()` con `with` + el módulo `csv`", True, "csv.DictReader te da cada fila como diccionario."),
   ("Copiar los datos a mano en una lista", False, "No escala y es propenso a errores."),
   ("Un set", False, "No lee archivos."),
   ("`input()`", False, "Lee lo que escribe el usuario, no un archivo.")]),

D("py-d18", S11, "Total desde un archivo CSV", 3, ["py-archivos", "py-for", "py-variables"],
  "El archivo en `RUTA_VENTAS` tiene las columnas `fecha,producto,cantidad,precio`. Leelo con el módulo `csv` y calculá el total facturado (suma de cantidad × precio). Guardalo en `resultado`.",
  "import csv\n\ntotal = 0\n# abrí el archivo y recorré las filas\n\nresultado = total",
  "import csv\n\ntotal = 0\nwith open(RUTA_VENTAS, encoding=\"utf-8\") as f:\n    for fila in csv.DictReader(f):\n        total += int(fila[\"cantidad\"]) * float(fila[\"precio\"])\n\nresultado = total",
  hints=["Primero abrí el archivo e imprimí una fila para ver cómo llega.", "csv.DictReader da cada fila como diccionario… ¿de qué tipo son sus valores?", "Convertí cantidad y precio antes de multiplicar y acumulá."],
  explain="Se abre el archivo con `with` (se cierra solo), DictReader entrega cada fila como diccionario de **textos**, y por eso hay que convertir cantidad y precio antes de acumular.",
  pseudo="total ← 0\nabrir archivo:\n    para cada fila del CSV:\n        total ← total + int(cantidad) × float(precio)",
  verify="El archivo tiene 5 filas: 1200 + 76.5 + 600 + 25.5 + 90."),

D("py-d19", S11, "Configuración en JSON", 2, ["py-archivos", "py-dict"],
  "La configuración del análisis está en un archivo JSON (`RUTA_CONFIG`). Leela y calculá el precio final del `'Monitor'` (de `precios`) aplicando el IVA que indica la configuración. Redondeá a 2 decimales y guardalo en `resultado`.",
  "import json\n\nresultado = ",
  "import json\n\nwith open(RUTA_CONFIG, encoding=\"utf-8\") as f:\n    config = json.load(f)\n\nresultado = round(precios[\"Monitor\"] * (1 + config[\"iva\"]), 2)",
  hints=["Abrí el archivo e imprimí lo que cargues: ¿qué estructura de Python obtenés?", "json.load convierte el archivo en un diccionario. ¿Qué clave tiene el IVA?", "Precio final = precio × (1 + iva)."],
  explain="`json.load` convierte el JSON en un diccionario de Python. Se lee la tasa con `config['iva']` y se aplica al precio del catálogo. Así la tasa no queda escrita en el código.",
  pseudo="config ← cargar JSON de RUTA_CONFIG\nresultado ← redondear(precios['Monitor'] × (1 + config['iva']), 2)"),

E("py-e08", S11, "El CSV que no se deja sumar", 2, ["py-archivos", "py-errores"],
  "Este código lee el CSV pero falla al calcular. Corregilo.",
  "import csv\n\ntotal = 0\nwith open(RUTA_VENTAS, encoding=\"utf-8\") as f:\n    for fila in csv.DictReader(f):\n        total += fila[\"cantidad\"] * fila[\"precio\"]\nresultado = total",
  "import csv\n\ntotal = 0\nwith open(RUTA_VENTAS, encoding=\"utf-8\") as f:\n    for fila in csv.DictReader(f):\n        total += int(fila[\"cantidad\"]) * float(fila[\"precio\"])\nresultado = total",
  detect=("¿Por qué falla?", [
      ("El módulo csv entrega todo como texto: hay que convertir a número", True, "'1' * '1200' → TypeError: can't multiply sequence by non-int of type 'str'."),
      ("La ruta del archivo está mal", False, "El archivo se abre bien; el error es al multiplicar."),
      ("DictReader no devuelve diccionarios", False, "Sí los devuelve."),
  ]),
  why="csv.DictReader **no convierte tipos**: cada valor es un string. Multiplicar dos strings da `TypeError: can't multiply sequence by non-int of type 'str'`. Hay que convertir con `int()` y `float()`.",
  hints=["Leé el error: ¿qué operación falla y con qué tipos?", "Imprimí `type(fila['cantidad'])`.", "¿Con qué funciones se convierte un texto a número entero y a decimal?"],
  pseudo="para cada fila: total ← total + int(cantidad) × float(precio)"),

# ======================================================================== S12 Leer código y debuggear
A("py-a16", S12, "Trazar un loop a mano", 2, ["py-leer", "py-for", "py-if"],
  "Sin ejecutarlo: ¿cuánto vale `x` al final?\n\n```python\nx = 0\nfor v in [3, 5, 2, 8]:\n    if v > 2:\n        x += v\n```",
  [("16", True, "Se suman 3, 5 y 8 (el 2 no cumple v > 2): 3 + 5 + 8 = 16."),
   ("18", False, "Eso sumaría también el 2, que no cumple la condición."),
   ("13", False, "Revisá: ¿3 > 2?"),
   ("8", False, "8 es solo el último valor; x acumula.")]),

B("py-b05", S12, "Explicar código ajeno línea por línea", 3, ["py-leer", "py-func", "py-dict"],
  "Leé este código **sin ejecutarlo** y explicá qué hace cada parte y qué devuelve con la lista `ventas`:\n\n```python\ndef ticket_promedio(ventas):\n    montos, compras = {}, {}\n    for v in ventas:\n        c = v[\"cliente\"]\n        montos[c] = montos.get(c, 0) + v[\"cantidad\"] * v[\"precio\"]\n        compras[c] = compras.get(c, 0) + 1\n    return {c: round(montos[c] / compras[c], 2) for c in montos}\n```",
  model="La función calcula el **ticket promedio por cliente**. Usa dos diccionarios acumuladores: `montos` suma lo que gastó cada cliente y `compras` cuenta cuántas compras hizo. En el loop, por cada venta se identifica al cliente y se actualizan ambos. Al final, una comprensión de diccionario divide monto ÷ compras para cada cliente y redondea a 2. Devuelve un dict cliente → gasto promedio por compra (por ejemplo Ana: (1200 + 80 + 450) / 3 = 576.67).",
  checklist=["Dije que calcula el gasto promedio por compra de cada cliente", "Expliqué los dos acumuladores (suma de montos y conteo de compras)", "Expliqué qué hace .get(c, 0)", "Expliqué la comprensión final (división y redondeo)", "Dije qué tipo de objeto devuelve (diccionario)"],
  hints=["Empezá por el return: ¿qué estructura devuelve?", "¿Qué guarda cada uno de los dos diccionarios?", "Probá mentalmente con Ana: ¿cuántas compras tiene y cuánto suma?"]),

E("py-e09", S12, "La lista ordenada que desapareció", 2, ["py-leer", "py-listas"],
  "Querés las ventas de la semana ordenadas de mayor a menor, pero `resultado` queda en `None`.",
  "ordenadas = ventas_semana.sort(reverse=True)\nresultado = ordenadas",
  "ordenadas = sorted(ventas_semana, reverse=True)\nresultado = ordenadas",
  detect=("¿Por qué da None?", [
      ("`.sort()` ordena la lista en el lugar y devuelve None", True, "Para obtener una lista nueva ordenada se usa sorted()."),
      ("reverse=True no existe", False, "Sí existe."),
      ("Las listas no se pueden ordenar", False, "Sí se pueden."),
  ]),
  why="`lista.sort()` modifica la lista original y **devuelve None**. Al guardar su resultado en una variable, se guarda None. `sorted(lista)` en cambio devuelve una lista nueva y no toca la original.",
  hints=["Imprimí `ordenadas` y también `ventas_semana` después de la línea 1.", "¿Qué devuelve el método `.sort()`?", "Existe una función integrada que devuelve una lista nueva ordenada."],
  pseudo="resultado ← nueva lista con ventas_semana ordenada de mayor a menor"),

A("py-a17", S12, "Estrategia de debugging", 2, ["py-leer"],
  "Tu función de totales no da error pero devuelve un número que no cierra. ¿Qué hacés primero?",
  [("Probarla con un caso chico de resultado conocido e imprimir los valores intermedios", True, "Así ubicás en qué paso se desvía."),
   ("Pedirle a una IA que la reescriba completa", False, "Puede 'arreglarse' sin que entiendas el error, y lo vas a repetir."),
   ("Agregar try/except", False, "No hay excepción: es un error de lógica."),
   ("Borrarla y empezar de cero", False, "Perdés la oportunidad de entender el error.")]),

# ======================================================================== S13 Python aplicado a datos
A("py-a18", S13, "Del Python puro a pandas", 1, ["py-datos"],
  "Tus datos son una **lista de diccionarios** (cada diccionario es una venta con las mismas claves). ¿A qué estructura de pandas se parece?",
  [("A un DataFrame: cada dict es una fila y cada clave una columna", True, "`pd.DataFrame(ventas)` lo convierte directamente."),
   ("A una Series", False, "Una Series es una sola columna."),
   ("A un array de NumPy", False, "Los arrays no tienen columnas con nombre."),
   ("A un gráfico", False, "No.")]),

C("py-c02", S13, "Plan: el producto más vendido en unidades", 3, ["py-datos", "py-dict"],
  "Querés saber **qué producto vendió más unidades** a partir de `ventas`. Diseñá el plan antes de programar.",
  [field("Datos que necesito", "El producto y la cantidad de cada venta.", ["Producto y cantidad", "Producto y precio", "Solo el producto", "Cliente y fecha"], 0),
   field("Operación", "Sumar cantidades por producto.", ["Sumar cantidades por producto", "Contar ventas por producto", "Promediar precios", "Ordenar por fecha"], 0),
   field("¿Necesito agrupar?", "Sí, por producto (el Mouse aparece en dos ventas).", ["Sí, por producto", "No"], 0),
   field("¿Cómo encuentro el mayor?", "Ordenar los totales de mayor a menor y tomar el primero, o usar max con key.", ["Ordenar los totales o usar max con key", "Tomar la primera venta de la lista", "Usar un set"], 0),
   field("Resultado esperado y verificación", "Un nombre de producto (o par producto, unidades). Verifico sumando a mano las unidades del candidato: Mouse = 3 + 5 = 8."),
  ],
  explain="El plan es: agrupar por producto sumando cantidades (acumulador con dict) y elegir el máximo. Notá la diferencia con 'contar ventas': el Mouse tiene 2 ventas pero 8 unidades.",
  hints=["¿'Más vendido' se mide en cantidad de ventas o en unidades?", "Un mismo producto aparece en varias ventas: ¿qué implica?", "Una vez que tenés un total por producto, ¿cómo elegís el mayor?"],
  pseudo="unidades ← {}\npara cada venta: unidades[producto] += cantidad\nresultado ← producto con mayor valor en unidades"),

D("py-d20", S13, "Top 3 productos por ingreso", 4, ["py-datos", "py-dict", "py-listas"],
  "Obtené el **top 3 de productos por ingreso total** (sumando `cantidad × precio` de todas sus ventas). Guardá una lista de tuplas `(producto, ingreso)` ordenada de mayor a menor en `resultado`.",
  "totales = {}\n\nresultado = ",
  "totales = {}\nfor v in ventas:\n    totales[v[\"producto\"]] = totales.get(v[\"producto\"], 0) + v[\"cantidad\"] * v[\"precio\"]\n\nresultado = sorted(totales.items(), key=lambda par: par[1], reverse=True)[:3]",
  hints=["Son tres pasos: agrupar, ordenar, cortar.", "Para agrupar ya conocés el patrón acumulador con dict. `.items()` da pares (producto, total).", "sorted acepta `key=` para indicar por qué ordenar (por el segundo elemento del par) y `reverse=True`. Después, slicing."],
  explain="Primero se agrupa el ingreso por producto con un diccionario. Después `sorted(totales.items(), key=…, reverse=True)` ordena los pares por el total (segundo elemento) de mayor a menor, y `[:3]` se queda con los tres primeros.",
  pseudo="totales ← ingreso acumulado por producto\npares ← ordenar totales.items() por ingreso, de mayor a menor\nresultado ← primeros 3 pares",
  verify="La Laptop debería encabezar: 1×1200 + 2×1200 = 3600."),

F("py-f04", S13, "La IA te propone pandas", 3, ["py-datos", "py-imports"],
  "Le pediste a una IA las unidades por categoría y, en lugar del loop que vos hiciste, te propuso **pandas**. Comparalo con tu solución en Python puro.",
  prompt="Tengo una lista de diccionarios 'ventas' con claves categoria y cantidad. Ya lo resolví con un for y un diccionario. ¿Cómo sería con pandas? Explicame la equivalencia con mi loop.",
  ai_code="import pandas as pd\n\ndf = pd.DataFrame(ventas)\nresultado = df.groupby(\"categoria\")[\"cantidad\"].sum()",
  questions=[
      ask("¿Qué hace `pd.DataFrame(ventas)`?", [("Convierte la lista de diccionarios en una tabla", True, "Cada dict es una fila; cada clave, una columna."), ("Ordena las ventas", False, "No ordena."), ("Suma las cantidades", False, "Solo crea la tabla.")]),
      ask("¿A qué parte de tu loop equivale `groupby('categoria')`?", [("A usar la categoría como clave del diccionario acumulador", True, "Agrupar = decidir a qué 'caja' va cada fila."), ("Al `total = 0`", False, "Eso es la inicialización."), ("Al import", False, "No.")]),
      ask("¿Qué tipo de objeto queda en `resultado`?", [("Una Series de pandas con las categorías como índice", True, "No es un dict: es una Series (aunque se parece)."), ("Un diccionario", False, "Para eso habría que agregar .to_dict()."), ("Una lista", False, "No.")]),
      ask("¿Cuándo preferirías la versión con pandas y cuándo la de Python puro?", model="Pandas: datasets medianos/grandes, varias agregaciones, código más corto y menos propenso a errores, y cuando el resultado sigue en un análisis con tablas. Python puro: scripts muy chicos sin dependencias, o para entender/explicar qué pasa por dentro."),
  ],
  hints=["Ejecutalo y compará el resultado con el de tu ejercicio de transferencia de unidades por categoría.", "Mirá el tipo con type(resultado).", "Relacioná cada parte de la línea de pandas con una parte de tu loop."],
  explain="`groupby('categoria')['cantidad'].sum()` hace en una línea lo mismo que tu loop: agrupar por categoría y sumar la cantidad. Es el puente al módulo de Pandas.",
  solution="import pandas as pd\n\ndf = pd.DataFrame(ventas)\nresultado = df.groupby(\"categoria\")[\"cantidad\"].sum()"),

# ======================================================================== Proyecto
C("py-p1", SP, "Fase 1 · Planificar el reporte", 3, ["py-datos", "py-archivos"],
  "**Contexto:** te pasan `ventas_sucio.csv` (ruta en `RUTA_VENTAS_SUCIO`) y te piden un mini reporte: total facturado, ingreso por producto y el producto top. El archivo tiene filas con problemas (cantidades vacías, 'n/d', negativas). Diseñá el plan completo antes de escribir código.",
  [field("Paso 1: cargar", "Abrir el CSV con csv.DictReader y obtener las filas como diccionarios de texto.", ["Abrir con csv.DictReader", "Escribir los datos a mano", "Usar input()"], 0),
   field("Paso 2: limpiar", "Convertir cantidad y precio con try/except; descartar filas con cantidad inválida (vacía, 'n/d') o ≤ 0, y contar cuántas se descartaron."),
   field("Paso 3: calcular", "Total = suma de cantidad × precio; ingreso por producto con un dict acumulador; top = producto con mayor ingreso."),
   field("Paso 4: verificar", "La suma de ingresos por producto debe ser igual al total; filas válidas + descartadas = filas del archivo."),
   field("¿Dónde ayuda la IA y dónde no?", "Puede ayudar con sintaxis de csv o de sorted con key, o a revisar mi código; el plan, las reglas de limpieza y la verificación las decido yo."),
  ],
  explain="Un buen plan separa **cargar → limpiar → calcular → verificar**, define reglas explícitas para los datos inválidos y deja claro cómo comprobar que el resultado es correcto.",
  hints=["Abrí el archivo mentalmente: ¿qué tipos de filas problemáticas hay?", "¿Qué harías con una fila con cantidad -1?", "¿Qué dos sumas deberían coincidir si todo salió bien?"],
  pseudo="filas ← leer CSV\nválidas, descartadas ← limpiar(filas)\nreporte ← calcular(válidas)\nverificar(reporte)"),

D("py-p2", SP, "Fase 2 · Cargar y limpiar", 4, ["py-archivos", "py-errores", "py-for"],
  "Leé `RUTA_VENTAS_SUCIO` y construí `limpias`: una lista de diccionarios `{'producto': str, 'cantidad': int, 'precio': float}` solo con las filas **válidas** (cantidad convertible a int y mayor que 0). Contá las descartadas en `descartadas`. Guardá `limpias` en `resultado`.",
  "import csv\n\nlimpias = []\ndescartadas = 0\n\nresultado = limpias",
  "import csv\n\nlimpias = []\ndescartadas = 0\nwith open(RUTA_VENTAS_SUCIO, encoding=\"utf-8\") as f:\n    for fila in csv.DictReader(f):\n        try:\n            cantidad = int(fila[\"cantidad\"])\n            precio = float(fila[\"precio\"])\n        except ValueError:\n            descartadas += 1\n            continue\n        if cantidad <= 0:\n            descartadas += 1\n            continue\n        limpias.append({\"producto\": fila[\"producto\"], \"cantidad\": cantidad, \"precio\": precio})\n\nresultado = limpias",
  hints=["Seguí tu plan: abrir, recorrer, convertir con protección, validar, guardar.", "Hay dos motivos para descartar: que la conversión falle (ValueError) o que la cantidad sea ≤ 0.", "`continue` salta a la siguiente fila del loop. Usalo después de contar una descartada."],
  explain="Por cada fila se intenta convertir; si falla (vacío, 'n/d') se descarta. Si convierte pero la cantidad no es positiva, también se descarta. Las válidas se guardan con los tipos correctos, listas para calcular.",
  pseudo="para cada fila:\n    intentar convertir cantidad e importe\n    si falla o cantidad ≤ 0: descartadas += 1; seguir\n    agregar fila limpia",
  verify="El archivo tiene 8 filas: 5 válidas y 3 descartadas (n/d, vacío, -1)."),

D("py-p3", SP, "Fase 3 · Calcular el reporte", 4, ["py-func", "py-datos", "py-dict"],
  "Escribí la función `reporte(filas)` que reciba una lista de ventas limpias y devuelva un diccionario con:\n- `'total'`: total facturado,\n- `'por_producto'`: diccionario producto → ingreso,\n- `'top'`: el producto de mayor ingreso.\n\nUsala con las filas de `limpias` (ya cargadas en el código inicial) y guardá el resultado en `resultado`.",
  "limpias = [\n    {\"producto\": \"Laptop\", \"cantidad\": 1, \"precio\": 1200.0},\n    {\"producto\": \"Mouse\", \"cantidad\": 3, \"precio\": 25.5},\n    {\"producto\": \"Auriculares\", \"cantidad\": 2, \"precio\": 80.0},\n    {\"producto\": \"Laptop\", \"cantidad\": 2, \"precio\": 1200.0},\n    {\"producto\": \"Tablet\", \"cantidad\": 1, \"precio\": 450.0},\n]\n\ndef reporte(filas):\n    pass\n\nresultado = reporte(limpias)",
  "limpias = [\n    {\"producto\": \"Laptop\", \"cantidad\": 1, \"precio\": 1200.0},\n    {\"producto\": \"Mouse\", \"cantidad\": 3, \"precio\": 25.5},\n    {\"producto\": \"Auriculares\", \"cantidad\": 2, \"precio\": 80.0},\n    {\"producto\": \"Laptop\", \"cantidad\": 2, \"precio\": 1200.0},\n    {\"producto\": \"Tablet\", \"cantidad\": 1, \"precio\": 450.0},\n]\n\ndef reporte(filas):\n    por_producto = {}\n    for f in filas:\n        por_producto[f[\"producto\"]] = por_producto.get(f[\"producto\"], 0) + f[\"cantidad\"] * f[\"precio\"]\n    total = sum(por_producto.values())\n    top = max(por_producto, key=por_producto.get)\n    return {\"total\": total, \"por_producto\": por_producto, \"top\": top}\n\nresultado = reporte(limpias)",
  hints=["Empezá por el ingreso por producto: con eso, el total y el top salen casi solos.", "El total puede calcularse sumando los valores del diccionario por producto.", "Para el top: `max` acepta `key=` (por ejemplo `key=por_producto.get`) o podés ordenar los pares."],
  explain="La función agrupa ingresos por producto, deriva el total sumando esos ingresos (lo que además garantiza coherencia) y elige el top con `max(..., key=...)`. Devuelve todo junto en un diccionario.",
  pseudo="función reporte(filas):\n    por_producto ← ingreso acumulado por producto\n    total ← suma de por_producto\n    top ← producto con mayor ingreso\n    devolver {total, por_producto, top}",
  check={"custom": "isinstance(resultado, dict) and abs(resultado.get('total', 0) - 4286.5) < 1e-6 and resultado.get('top') == 'Laptop' and abs(resultado.get('por_producto', {}).get('Mouse', 0) - 76.5) < 1e-6 and len(resultado.get('por_producto', {})) == 4",
         "custom_msg": "El reporte debe tener 'total' (4286.5), 'por_producto' con 4 productos y 'top' == 'Laptop'."}),

E("py-p4", SP, "Fase 4 · Verificar: el promedio sospechoso", 3, ["py-leer", "py-func"],
  "Agregaste al reporte el **ticket promedio** (ingreso total ÷ cantidad de ventas), pero da un valor que no cierra. Encontrá el error verificando con un caso conocido.",
  "filas = [\n    {\"producto\": \"Laptop\", \"cantidad\": 1, \"precio\": 1200.0},\n    {\"producto\": \"Mouse\", \"cantidad\": 3, \"precio\": 25.5},\n    {\"producto\": \"Auriculares\", \"cantidad\": 2, \"precio\": 80.0},\n]\n\ndef ticket_promedio(filas):\n    total = 0\n    for f in filas:\n        total += f[\"cantidad\"] * f[\"precio\"]\n    return total / sum(f[\"cantidad\"] for f in filas)\n\nresultado = round(ticket_promedio(filas), 2)",
  "filas = [\n    {\"producto\": \"Laptop\", \"cantidad\": 1, \"precio\": 1200.0},\n    {\"producto\": \"Mouse\", \"cantidad\": 3, \"precio\": 25.5},\n    {\"producto\": \"Auriculares\", \"cantidad\": 2, \"precio\": 80.0},\n]\n\ndef ticket_promedio(filas):\n    total = 0\n    for f in filas:\n        total += f[\"cantidad\"] * f[\"precio\"]\n    return total / len(filas)\n\nresultado = round(ticket_promedio(filas), 2)",
  detect=("¿Qué está mal?", [
      ("Divide por el total de unidades en lugar de por la cantidad de ventas", True, "Ticket promedio = ingreso / número de ventas (filas)."),
      ("El acumulador está mal inicializado", False, "total = 0 está antes del loop: correcto."),
      ("round() cambia el resultado", False, "Solo redondea al final."),
  ]),
  why="El 'ticket promedio' es el ingreso medio **por venta**: total ÷ cantidad de ventas (`len(filas)` = 3). El código divide por la suma de unidades (6), que mide otra cosa (precio medio por unidad). Verificándolo a mano: (1200 + 76.5 + 160) / 3 = 478.83.",
  hints=["Calculá a mano el ticket promedio de estas 3 ventas.", "¿El código divide por 3? Imprimí el divisor.", "¿Qué representa la suma de cantidades?"],
  pseudo="ticket ← ingreso total / número de ventas"),

B("py-p5", SP, "Fase 5 · Explicar tus decisiones", 3, ["py-datos", "py-errores", "py-leer"],
  "Escribí un breve informe (4-6 líneas) como si se lo explicaras a quien te pidió el reporte: **qué hiciste con las filas inválidas, por qué, cómo verificaste que los números son correctos y qué limitaciones tiene tu reporte.**",
  model="Leí el CSV con 8 filas. Descarté 3 que tenían cantidad inválida ('n/d', vacía o negativa) porque no se puede calcular su ingreso de forma confiable; no las inventé ni las rellené. Con las 5 válidas calculé el total, el ingreso por producto y el top (Laptop). Verifiqué que la suma de ingresos por producto coincide con el total y que válidas + descartadas = 8. Limitaciones: si las filas descartadas eran ventas reales, el total está subestimado; convendría revisar el origen de esos errores.",
  checklist=["Dije cuántas filas descarté y por qué motivo", "Justifiqué no inventar ni rellenar datos", "Expliqué al menos una verificación (sumas que coinciden, conteo de filas)", "Mencioné una limitación del resultado"],
  hints=["¿Qué haría alguien que lee tu reporte si no le contás que faltan filas?", "¿Qué dos verificaciones hiciste en las fases anteriores?", "¿El total final puede estar subestimado? ¿Por qué?"]),
]

QUIZ = [
Q("q-py-01", ["py-dict"], "Tenés códigos de producto y necesitás obtener su descripción muchas veces durante un script.",
  [("Diccionario código → descripción", True, "Búsqueda directa por clave."), ("Lista", False, "Habría que recorrerla."), ("Set", False, "No guarda la descripción."), ("Tupla", False, "No busca por clave.")]),
Q("q-py-02", ["py-tuplas-sets"], "Querés saber si un email ya está registrado entre 200.000 emails.",
  [("Set de emails y el operador `in`", True, "La pertenencia en un set es inmediata."), ("Ordenar la lista cada vez", False, "Innecesario y lento."), ("Un while", False, "No es lo adecuado."), ("Un f-string", False, "Sirve para armar textos.")]),
Q("q-py-03", ["py-strings"], "Los nombres de ciudad llegan como 'madrid', 'Madrid ' y 'MADRID'.",
  [("Normalizar strings (strip + title/lower)", True, "Unifica variantes."), ("try/except", False, "No hay error."), ("Un set directamente", False, "Las variantes seguirían siendo distintas."), ("round()", False, "Es para números.")]),
Q("q-py-04", ["py-for"], "Necesitás calcular el ingreso de cada una de las 500 ventas de una lista y sumarlos.",
  [("Loop for con acumulador", True, "Patrón básico de agregación."), ("Condicional if", False, "No repite."), ("import json", False, "No aplica."), ("Tupla", False, "No procesa.")]),
Q("q-py-05", ["py-while"], "Simular cuántos meses tarda un ahorro en llegar a una meta con interés mensual.",
  [("while hasta alcanzar la meta", True, "No se sabe cuántas vueltas."), ("for sobre una lista fija", False, "No hay lista conocida."), ("Un set", False, "No."), ("split()", False, "No.")]),
Q("q-py-06", ["py-func"], "Aplicás la misma limpieza de texto en 4 columnas y 3 notebooks.",
  [("Una función reutilizable", True, "Lógica en un solo lugar."), ("Copiar y pegar", False, "Duplica errores."), ("Un while", False, "No."), ("Un set", False, "No.")]),
Q("q-py-07", ["py-errores"], "Algunos registros tienen la edad como 'desconocida' y no querés que el script se caiga.",
  [("try/except ValueError al convertir", True, "Manejás el caso inválido."), ("Ignorar el error", False, "El script se cae."), ("Usar un dict", False, "No resuelve la conversión."), ("sorted()", False, "No.")]),
Q("q-py-08", ["py-comp"], "Querés una lista con los precios mayores a 100 multiplicados por 1.21.",
  [("Comprensión de lista con if", True, "Filtra y transforma en una línea."), ("while", False, "No."), ("Un import", False, "No."), ("Un traceback", False, "No.")]),
Q("q-py-09", ["py-archivos"], "La configuración del proyecto (tasas, umbrales) está en un archivo `config.json`.",
  [("open + json.load → diccionario", True, "JSON se mapea a dicts de Python."), ("csv.DictReader", False, "Es para CSV."), ("input()", False, "Es para teclado."), ("Escribir los valores en el código", False, "Pierde la ventaja del archivo de configuración.")]),
Q("q-py-10", ["py-imports"], "Necesitás números aleatorios para simular datos de prueba.",
  [("Importar el módulo random (o NumPy)", True, "No hay que reinventarlo."), ("Escribir un generador propio", False, "Innecesario."), ("Un set", False, "No."), ("Un if", False, "No.")]),
Q("q-py-11", ["py-leer"], "La IA te dio una función que 'funciona', pero no entendés una de sus líneas.",
  [("Ejecutarla con un caso chico e imprimir los valores de esa línea, o preguntarle qué hace", True, "Entender antes de aceptar."), ("Usarla igual", False, "Si falla, no vas a saber por qué."), ("Borrar la línea", False, "Puede ser necesaria."), ("Pedirle otra versión sin preguntar", False, "No resolvés tu duda.")]),
Q("q-py-12", ["py-if"], "Asignar una categoría de cliente según su gasto anual en 4 tramos.",
  [("if / elif / else con tramos ordenados", True, "Una decisión por tramos."), ("Un for", False, "No alcanza solo."), ("Un set", False, "No."), ("json", False, "No.")]),
Q("q-py-13", ["py-variables"], "Una suma de importes da '100200300' en lugar de 600.",
  [("Los importes son texto: hay que convertirlos a número", True, "Con str, + concatena."), ("Falta redondear", False, "No es el problema."), ("Hay que usar un while", False, "No."), ("Es un error de Python", False, "Es el comportamiento esperado con texto.")]),
Q("q-py-14", ["py-datos"], "Necesitás el total de ventas por vendedor a partir de una lista de diccionarios, sin pandas.",
  [("Diccionario acumulador vendedor → total", True, "Agrupar en Python puro."), ("Una lista de totales", False, "Perdés a qué vendedor pertenece cada total."), ("Un set de vendedores", False, "No guarda totales."), ("Una tupla", False, "No acumula.")]),
]

PROJECT = project(
    "Mini sistema de análisis de ventas (Python puro)",
    "Te pasan un archivo de ventas con errores de carga. Antes de usar pandas, tenés que demostrar que podés resolverlo con Python: leer, limpiar, calcular, verificar y explicar.",
    "Un reporte confiable (total, ingreso por producto y producto top) junto con una explicación de tus decisiones sobre los datos inválidos.",
    [("Planificar", "Diseñá los pasos y las reglas de limpieza antes de programar.", ["py-p1"]),
     ("Cargar y limpiar", "Leé el CSV y quedate con filas válidas, contando las descartadas.", ["py-p2"]),
     ("Calcular", "Encapsulá las métricas en una función reutilizable.", ["py-p3"]),
     ("Verificar", "Encontrá un error de lógica comparando con un cálculo a mano.", ["py-p4"]),
     ("Explicar", "Escribí qué hiciste, por qué y qué limitaciones tiene.", ["py-p5"])],
    ["Lista limpia de ventas y conteo de filas descartadas", "Función reporte(filas) probada", "Verificación: suma por producto = total", "Informe breve con decisiones y limitaciones"],
    ["Podés pedirle a la IA sintaxis (csv, sorted con key) o que revise tu código, pero no el plan ni las reglas de limpieza.",
     "Si la IA te da código, explicá cada línea antes de usarlo.",
     "Al terminar, rehacé la fase 3 sin IA para comprobar que la entendiste."],
)

MODULE = module(
    "m00", "00", "Python para Ciencia de Datos", "🐍", "#3b82f6",
    "El Python que necesitás para leer, escribir, modificar y debuggear código de datos. La base de todo lo que sigue.",
    learn=["Reconocer qué estructura de datos necesita cada problema (lista, dict, set, tupla)",
           "Transformar, filtrar y agrupar datos con loops, condicionales y comprensiones",
           "Empaquetar lógica en funciones probables",
           "Leer tracebacks, manejar datos inválidos y debuggear con método",
           "Leer archivos CSV/JSON y entender qué hace pandas por dentro"],
    why="Pandas, NumPy y scikit-learn **son Python**. Cuando una IA te genera `df.groupby(...).apply(lambda x: ...)`, para entenderlo necesitás saber qué es una función, un diccionario o una comprensión. Sin esta base, cada error es un muro; con ella, es una pista.\n\nNo vas a aprender *todo* Python: solo el que te permite **pensar, leer y verificar** código de datos.",
    ai="Usá la IA para **sintaxis** y para **revisar** tu razonamiento, no para pensar por vos. Antes de pedir código, escribí el plan en pasos. Si la IA te da código, explicá cada línea y probalo con un caso chico. Al final, rehacé el ejercicio sin ayuda.",
    concepts=CONCEPTS, exercises=EXERCISES, quiz=QUIZ, project=PROJECT,
    setup=PY_SETUP, tables=["ventas", "precios", "ventas_semana", "lecturas"], file="analisis.py",
)
