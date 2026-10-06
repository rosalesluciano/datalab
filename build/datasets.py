# -*- coding: utf-8 -*-
"""Datos de cada módulo. Cada cadena se ejecuta antes del código del ejercicio (web, Colab y tests)."""

PY_SETUP = r'''import os, json, tempfile

# Ventas de una tienda: cada diccionario es una fila
ventas = [
    {"id": 1, "fecha": "2024-03-01", "producto": "Laptop", "categoria": "Computación", "cantidad": 1, "precio": 1200.0, "cliente": "Ana"},
    {"id": 2, "fecha": "2024-03-01", "producto": "Mouse", "categoria": "Accesorios", "cantidad": 3, "precio": 25.5, "cliente": "Bruno"},
    {"id": 3, "fecha": "2024-03-02", "producto": "Monitor", "categoria": "Computación", "cantidad": 2, "precio": 300.0, "cliente": "Carla"},
    {"id": 4, "fecha": "2024-03-02", "producto": "Auriculares", "categoria": "Audio", "cantidad": 1, "precio": 80.0, "cliente": "Ana"},
    {"id": 5, "fecha": "2024-03-03", "producto": "Teclado", "categoria": "Accesorios", "cantidad": 2, "precio": 45.0, "cliente": "Diego"},
    {"id": 6, "fecha": "2024-03-03", "producto": "Laptop", "categoria": "Computación", "cantidad": 2, "precio": 1200.0, "cliente": "Elena"},
    {"id": 7, "fecha": "2024-03-04", "producto": "Mouse", "categoria": "Accesorios", "cantidad": 5, "precio": 25.5, "cliente": "Carla"},
    {"id": 8, "fecha": "2024-03-04", "producto": "Micrófono", "categoria": "Audio", "cantidad": 1, "precio": 95.0, "cliente": "Bruno"},
    {"id": 9, "fecha": "2024-03-05", "producto": "Tablet", "categoria": "Computación", "cantidad": 1, "precio": 450.0, "cliente": "Ana"},
    {"id": 10, "fecha": "2024-03-05", "producto": "Auriculares", "categoria": "Audio", "cantidad": 3, "precio": 80.0, "cliente": "Diego"},
]

# Catálogo: producto -> precio
precios = {"Laptop": 1200.0, "Mouse": 25.5, "Teclado": 45.0, "Monitor": 300.0,
           "Auriculares": 80.0, "Tablet": 450.0, "Micrófono": 95.0}

# Ventas totales de cada día de una semana (lun a dom)
ventas_semana = [1200, 950, 1430, 880, 1700, 2100, 1900]

# Lecturas de un sensor de temperatura: None = sin lectura, -999.0 = error del sensor
lecturas = [21.5, 22.1, None, 23.4, -999.0, 22.8, None, 24.0, 85.3, 23.1]

# Archivos de ejemplo (rutas guardadas en variables, como en un proyecto real)
RUTA_VENTAS = os.path.join(tempfile.gettempdir(), "pq_ventas.csv")
with open(RUTA_VENTAS, "w", encoding="utf-8") as _f:
    _f.write("""fecha,producto,cantidad,precio
2024-03-01,Laptop,1,1200
2024-03-01,Mouse,3,25.5
2024-03-02,Monitor,2,300
2024-03-02,Mouse,1,25.5
2024-03-03,Teclado,2,45
""")

RUTA_VENTAS_SUCIO = os.path.join(tempfile.gettempdir(), "pq_ventas_sucio.csv")
with open(RUTA_VENTAS_SUCIO, "w", encoding="utf-8") as _f:
    _f.write("""fecha,producto,cantidad,precio
2024-03-01,Laptop,1,1200
2024-03-01,Mouse,3,25.5
2024-03-02,Monitor,n/d,300
2024-03-02,Auriculares,2,80
2024-03-03,Teclado,,45
2024-03-03,Laptop,2,1200
2024-03-04,Mouse,-1,25.5
2024-03-04,Tablet,1,450
""")

RUTA_CONFIG = os.path.join(tempfile.gettempdir(), "pq_config.json")
with open(RUTA_CONFIG, "w", encoding="utf-8") as _f:
    json.dump({"moneda": "USD", "iva": 0.21, "umbral_alerta": 1000, "tiendas": ["Centro", "Norte"]}, _f)
del _f
'''

SETUP = '''import pandas as pd
import numpy as np

clientes = pd.DataFrame({
    "cliente_id": range(1, 13),
    "nombre": ["Ana", "Bruno", "Carla", "Diego", "Elena", "Facundo",
               "Gabriela", "Hugo", "Inés", "Julián", "Karina", "Lucas"],
    "ciudad": ["Madrid", "Buenos Aires", "CDMX", "Bogotá", "Madrid", "Lima",
               "Buenos Aires", "CDMX", "Santiago", "Bogotá", "Madrid", "Lima"],
    "pais": ["España", "Argentina", "México", "Colombia", "España", "Perú",
             "Argentina", "México", "Chile", "Colombia", "España", "Perú"],
    "edad": [34, 28, 45, 23, 51, 39, 30, 27, 42, 36, 25, 48],
    "segmento": ["Premium", "Básico", "Premium", "Básico", "Premium", "Estándar",
                 "Estándar", "Básico", "Premium", "Estándar", "Básico", "Estándar"],
    "email": ["ana@mail.com", None, "carla@mail.com", "diego@mail.com", None, "facu@mail.com",
              "gabi@mail.com", None, "ines@mail.com", "julian@mail.com", "kari@mail.com", "lucas@mail.com"],
    "fecha_registro": pd.to_datetime([
        "2023-01-15", "2023-02-03", "2023-02-20", "2023-03-11", "2023-04-02", "2023-05-19",
        "2023-06-07", "2023-07-23", "2023-08-30", "2023-09-14", "2023-10-05", "2023-11-28"]),
})

productos = pd.DataFrame({
    "producto_id": range(1, 11),
    "producto": ["Laptop", "Mouse", "Teclado", "Monitor", "Auriculares",
                 "Webcam", "Silla gamer", "Escritorio", "Tablet", "Micrófono"],
    "categoria": ["Computación", "Accesorios", "Accesorios", "Computación", "Audio",
                  "Accesorios", "Muebles", "Muebles", "Computación", "Audio"],
    "precio": [1200.0, 25.5, 45.0, 300.0, 80.0, 60.0, 250.0, 180.0, 450.0, 95.0],
    "stock": [5, 150, 80, 20, 60, 0, 12, 7, 15, 0],
})

_estados = ["entregado", "enviado", "entregado", "cancelado", "entregado", "pendiente"]
pedidos = pd.DataFrame({
    "pedido_id": range(1001, 1031),
    "cliente_id": [(i * 7) % 11 + 1 for i in range(29)] + [99],
    "producto_id": [(i * 3) % 10 + 1 for i in range(30)],
    "cantidad": [(i % 4) + 1 for i in range(30)],
    "fecha": pd.date_range("2024-01-03", periods=30, freq="5D"),
    "estado": [_estados[i % 6] for i in range(30)],
})

empleados = pd.DataFrame({
    "emp_id": range(1, 11),
    "nombre": ["Marta", "Pablo", "Sofía", "Tomás", "Valeria",
               "Andrés", "Lucía", "Martín", "Paula", "Ramiro"],
    "depto": ["Dirección", "Ventas", "Ventas", "Ventas", "IT",
              "IT", "IT", "Marketing", "Marketing", "Ventas"],
    "salario": [9000, 4200, 3900, 4000, 5200, 4800, 6100, 3700, 4100, 3500],
    "jefe_id": pd.array([None, 1, 2, 2, 1, 5, 5, 1, 8, 2], dtype="Int64"),
    "fecha_ingreso": pd.to_datetime([
        "2015-03-01", "2018-06-15", "2019-01-10", "2020-09-01", "2017-11-20",
        "2021-02-01", "2016-08-08", "2022-04-18", "2019-07-07", "2023-01-09"]),
})

_i = np.arange(90)
_f = pd.date_range("2024-01-01", periods=90, freq="D")
_v = 1000 + 8 * _i + 250 * (_f.dayofweek >= 5) + ((_i * 37) % 11) * 20
_v = np.where(np.isin(_i, [20, 55, 77]), _v + 1500, _v)
ventas_diarias = pd.DataFrame({
    "fecha": _f,
    "ventas": _v.astype(float),
    "visitas": (300 + (_i * 13) % 97 + 2 * _i).astype(int),
})

sucio = pd.DataFrame({
    "id": [1, 2, 2, 3, 4, 5, 6, 7],
    "nombre": ["  ana ", "BRUNO", "BRUNO", "carla", None, "Diego  ", "elena", "facundo"],
    "edad": ["34", "28", "28", "n/d", "23", "51", None, "39"],
    "ciudad": ["madrid", "Buenos Aires", "Buenos Aires", " santiago", "bogotá", "Madrid ", "madrid", "LIMA"],
    "monto": ["$1,200.50", "$300", "$300", "$45.00", None, "$80.5", "$99", "$1,000"],
})
del _i, _f, _v, _estados
'''

TABLES = ["clientes", "productos", "pedidos", "empleados", "ventas_diarias", "sucio"]

DF_SETUP = '''
import sqlite3
conn = sqlite3.connect(":memory:")
clientes.to_sql("clientes", conn, index=False)
productos.to_sql("productos", conn, index=False)
pedidos.to_sql("pedidos", conn, index=False)

trimestral = pd.DataFrame({
    "tienda": ["Centro", "Norte", "Sur"],
    "Q1": [100, 80, 60],
    "Q2": [120, 95, 70],
    "Q3": [130, 90, 85],
})
'''

NUMPY_SETUP = '''
temperaturas = np.array([21.5, 23.0, 19.8, 25.1, 27.3, 22.4, 18.9])   # una semana, en °C
notas = np.array([[7, 8, 6],
                  [9, 5, 8],
                  [6, 7, 9],
                  [8, 9, 10],
                  [5, 6, 7]])                                          # 5 alumnos x 3 exámenes
precios = productos["precio"].to_numpy()

_rng = np.random.default_rng(3)
sensores = np.round(22 + _rng.normal(0, 1.5, size=(7, 4)), 1)   # 7 días x 4 sensores (°C)
sensores[2, 1] = 41.0                                            # falla del sensor 1 el día 2
del _rng
'''

PLT_SETUP = '''
import matplotlib.pyplot as plt

meses = ["Ene", "Feb", "Mar", "Abr", "May", "Jun"]
ingresos = [12.5, 14.1, 13.8, 16.2, 18.9, 21.3]   # miles
gastos = [10.2, 11.0, 11.5, 12.1, 13.0, 13.4]     # miles
'''

SNS_SETUP = '''
import matplotlib.pyplot as plt
import seaborn as sns

_rng = np.random.default_rng(7)
_n = 120
propinas = pd.DataFrame({
    "cuenta": np.round(_rng.gamma(4, 5, _n) + 5, 2),
    "dia": _rng.choice(["Jue", "Vie", "Sáb", "Dom"], _n, p=[0.2, 0.2, 0.35, 0.25]),
    "momento": _rng.choice(["Almuerzo", "Cena"], _n, p=[0.35, 0.65]),
    "fumador": _rng.choice(["Sí", "No"], _n, p=[0.4, 0.6]),
    "personas": _rng.integers(1, 7, _n),
})
propinas["propina"] = np.round(propinas["cuenta"] * _rng.uniform(0.08, 0.22, _n) + 0.5, 2)
del _rng, _n
'''

ML_SETUP = '''
_rng = np.random.default_rng(42)
_n = 200
_m2 = _rng.integers(35, 220, _n)
_hab = np.clip(_m2 // 35 + _rng.integers(-1, 2, _n), 1, 6)
_ant = _rng.integers(0, 60, _n)
_barrio = _rng.choice(["Centro", "Norte", "Sur"], _n)
_extra = np.select([_barrio == "Centro", _barrio == "Norte"], [40000, 15000], 0)
casas = pd.DataFrame({
    "m2": _m2, "habitaciones": _hab, "antiguedad": _ant, "barrio": _barrio,
    "precio": np.round(30000 + _m2 * 1800 + _hab * 5000 - _ant * 900 + _extra
                       + _rng.normal(0, 15000, _n), -2),
})
_n = 300
churn = pd.DataFrame({
    "meses_cliente": _rng.integers(1, 72, _n),
    "cargo_mensual": np.round(_rng.uniform(15, 120, _n), 2),
    "reclamos": _rng.poisson(1.2, _n),
    "contrato": _rng.choice(["Mensual", "Anual"], _n, p=[0.6, 0.4]),
})
_logit = (-1.0 - 0.05 * churn["meses_cliente"] + 0.03 * churn["cargo_mensual"]
          + 0.6 * churn["reclamos"] + np.where(churn["contrato"] == "Mensual", 1.2, -0.8))
churn["abandona"] = (_rng.uniform(0, 1, _n) < 1 / (1 + np.exp(-_logit))).astype(int)
del _rng, _n, _m2, _hab, _ant, _barrio, _extra, _logit
'''

