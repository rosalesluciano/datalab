# 🧪 DataLab (PandasQuest)

Laboratorio personal de **Ciencia de Datos con método**: aprender a reconocer problemas, diseñar soluciones, usar la IA como copiloto, debuggear y verificar. Sin memorizar sintaxis.

👉 **Web:** https://rosalesluciano.github.io/datalab/

```
CONCEPTO → PROBLEMA → RAZONAMIENTO → ESTRATEGIA → IMPLEMENTACIÓN → VERIFICACIÓN
```

## Ruta

| # | Módulo | Enfoque |
|---|---|---|
| 00 | 🐍 Python para Ciencia de Datos | Estructuras, control, funciones, errores, archivos, leer y debuggear código |
| 01 | 🐼 Pandas | Reconocer la operación: inspeccionar, filtrar, limpiar, agrupar, ordenar, combinar |
| 02 | 📋 DataFrames | Intuición sobre la forma: índice, loc/iloc, ejes, agregar vs transformar, relaciones |
| 03 | 🔢 NumPy | Cuándo usar arrays, shape/dtype, broadcasting, estadística por ejes |
| 04 | 📈 Matplotlib | Qué gráfico responde cada pregunta, legibilidad, dashboards |
| 05 | 🎨 Seaborn | Pregunta → tipo de dato → visualización → interpretación |
| 06 | 🤖 Intro a Machine Learning | ¿Es ML? ¿De qué tipo? Features/target, split, baseline, métricas, overfitting, leakage |

Cada módulo tiene: **Inicio** (qué voy a aprender, por qué importa, uso de IA), **Conceptos** (fichas), **Práctica**, **Proyecto**, **Evaluación** y **Repaso**.

## Siete tipos de ejercicio

| Tipo | Qué entrena |
|---|---|
| 🎯 A · Reconocimiento | Elegir la herramienta para un problema |
| 💭 B · Razonamiento | Explicar la solución con palabras (autoevaluación con checklist) |
| 🧭 C · Plan de solución | Datos, operación, agrupación, resultado esperado, verificación |
| ⌨️ D · Código | Pensar → planificar (obligatorio) → implementar → verificar |
| 🐞 E · Debugging | Detectar, explicar y corregir |
| 🤖 F · IA copiloto | Leer y explicar código generado por una IA |
| 🔁 G · Transferencia | Resolver una variante de un ejercicio ya hecho |

- **Escalera de pistas** de 6 niveles (pensá → dirección → herramienta → concepto → ejemplo → solución). La solución se muestra en 3 etapas: idea → pseudocódigo → código, y solo después de un intento.
- **Regla de oro**: si marcás que usaste IA para el código, tenés que explicarlo antes de que cuente como resuelto. El botón *🤖 Pedir ayuda* arma prompts progresivos con tu problema, tu plan y tu código.
- **Progreso por concepto** con 8 indicadores: conocido, practicado, comprendido, reconocer, resolver, debuggear, explicar y transferir. Completar no es dominar.
- **¿Sé esto?**: problemas aleatorios de reconocimiento; los que fallás vuelven más seguido.
- Python, pandas, matplotlib, seaborn y scikit-learn corren **en el navegador** (Pyodide). Cada módulo tiene además un notebook de **Google Colab** con los ejercicios de código.
- El progreso se guarda en el navegador (con exportar/importar en *Progreso*).

## Estructura

| Ruta | Qué es |
|---|---|
| `build/datasets.py` | Datos de cada módulo |
| `build/framework.py` | Constructores: fichas de concepto, ejercicios A-G, preguntas, proyectos y validación |
| `build/modules/m0X_*.py` | Contenido de cada módulo |
| `build/pool/` | Ejercicios de código de la versión anterior, reutilizados como tipo D |
| `build/build.py` | Genera `js/data.js` y `notebooks/*.ipynb` |
| `py/pq_core.py` | Motor de corrección (web, Colab y tests) |
| `py/pq_web.py`, `js/worker.js` | Ejecución de Python en el navegador |
| `js/core.js` | Estado, dominio por concepto, Python y UI común |
| `js/views.js` | Inicio, módulo, concepto, método IA y progreso |
| `js/exercise.js` | Página de ejercicio (tipos A-G, pistas, ayuda IA) |
| `js/quiz.js` | ¿Sé esto? y evaluaciones |
| `tests/` | Tests de contenido y end-to-end en navegador |

## Desarrollo

```bash
pip install pandas numpy matplotlib seaborn scikit-learn
python build/build.py                 # regenerar datos y notebooks
python tests/test_content.py          # valida todo el contenido (soluciones pasan, plantillas fallan)
python -m http.server 8765            # servir la web en local
python tests/test_browser.py          # E2E en Chromium (requiere playwright)
```

Para agregar un ejercicio: escribilo con los constructores de `framework.py` en el módulo correspondiente, ejecutá `build.py` y `test_content.py`.
