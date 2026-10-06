# -*- coding: utf-8 -*-
"""Fuente única de contenido.

Ruta: 00 Python · 01 Pandas · 02 DataFrames · 03 NumPy · 04 Matplotlib · 05 Seaborn · 06 Machine Learning

- build/datasets.py      datos de cada módulo
- build/framework.py     constructores de conceptos, ejercicios (tipos A-G), preguntas y proyectos
- build/pool/            ejercicios de código heredados que se reutilizan como tipo D
- build/modules/         un archivo por módulo

build.py genera js/data.js (web) y notebooks/*.ipynb (Colab).
tests/test_content.py valida que cada solución pase y cada plantilla o código con bug falle.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
for sub in ("", "pool", "modules"):
    sys.path.insert(0, os.path.join(HERE, sub))

from framework import LEVELS, TYPES, register_pool, validate  # noqa: E402

import pool_dataframes  # noqa: E402
import pool_matplotlib  # noqa: E402
import pool_ml  # noqa: E402
import pool_numpy  # noqa: E402
import pool_pandas  # noqa: E402
import pool_seaborn  # noqa: E402

for _p in (pool_pandas, pool_dataframes, pool_numpy, pool_matplotlib, pool_seaborn, pool_ml):
    register_pool(_p.EXERCISES)

from m00_python import MODULE as M00  # noqa: E402
from m01_pandas import MODULE as M01  # noqa: E402
from m02_dataframes import MODULE as M02  # noqa: E402
from m03_numpy import MODULE as M03  # noqa: E402
from m04_matplotlib import MODULE as M04  # noqa: E402
from m05_seaborn import MODULE as M05  # noqa: E402
from m06_ml import MODULE as M06  # noqa: E402

MODULES = [M00, M01, M02, M03, M04, M05, M06]

validate(MODULES)

__all__ = ["MODULES", "TYPES", "LEVELS"]
