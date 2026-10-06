"""PandasQuest - motor de corrección.

Se usa igual en el navegador (Pyodide), en los notebooks de Colab y en los tests.
Compara el `resultado` del alumno contra el de la solución oficial con tolerancia
a diferencias irrelevantes (tipos int/float, nombres de índice, dtype string, etc.).
"""
import math

import numpy as np
import pandas as pd


def _norm_s(s):
    dt = s.dtype
    if isinstance(dt, pd.CategoricalDtype) or pd.api.types.is_string_dtype(dt):
        s = s.astype(object)
    elif pd.api.types.is_extension_array_dtype(dt):
        if pd.api.types.is_numeric_dtype(dt) and not pd.api.types.is_bool_dtype(dt):
            s = s.astype("float64")
        else:
            s = s.astype(object)
    if s.dtype == object:
        s = s.where(s.notna(), None)
    return s


def _norm_index(idx):
    if isinstance(idx, pd.MultiIndex):
        return idx
    if isinstance(idx, pd.CategoricalIndex) or pd.api.types.is_string_dtype(idx.dtype):
        return pd.Index(list(idx), dtype=object)
    return idx


def _norm(o):
    if isinstance(o, pd.Series):
        o = _norm_s(o.copy())
    else:
        cols = list(o.columns)
        o = pd.DataFrame({i: _norm_s(o.iloc[:, i]) for i in range(o.shape[1])}, index=o.index)
        o.columns = _norm_index(pd.Index(cols))
    o.index = _norm_index(o.index)
    return o


def _sort(o, ignore_index):
    if ignore_index:
        o = o.reset_index(drop=True)
        try:
            if isinstance(o, pd.Series):
                o = o.sort_values(kind="mergesort")
            else:
                o = o.sort_values(by=list(o.columns), kind="mergesort")
        except TypeError:
            key = o.astype(str) if isinstance(o, pd.Series) else o.astype(str).agg("|".join, axis=1)
            o = o.iloc[np.argsort(key.to_numpy(), kind="mergesort")]
        return o.reset_index(drop=True)
    try:
        return o.sort_index()
    except TypeError:
        return o


def _tipo(x):
    nombres = {pd.DataFrame: "un DataFrame", pd.Series: "una Series", list: "una lista", dict: "un diccionario",
               tuple: "una tupla", set: "un set", str: "un texto (str)", int: "un entero (int)",
               float: "un decimal (float)", bool: "un booleano (bool)", type(None): "None (nada)",
               np.ndarray: "un array de NumPy"}
    return nombres.get(type(x), f"un {type(x).__name__}")


def _scalar_eq(u, e):
    if isinstance(e, (np.generic,)):
        e = e.item()
    if isinstance(u, (np.generic,)):
        u = u.item()
    if isinstance(e, float) or isinstance(u, float):
        try:
            u, e = float(u), float(e)
        except (TypeError, ValueError):
            return False
        if math.isnan(e):
            return math.isnan(u)
        return math.isclose(u, e, rel_tol=1e-6, abs_tol=1e-6)
    if isinstance(e, (list, tuple)) and isinstance(u, (list, tuple, np.ndarray, pd.Index)):
        u = list(u)
        return len(u) == len(e) and all(_scalar_eq(a, b) for a, b in zip(u, e))
    if isinstance(e, dict):
        return (isinstance(u, dict) and set(map(str, u)) == set(map(str, e))
                and all(_scalar_eq(u[k] if k in u else u[str(k)], v) for k, v in e.items()))
    if isinstance(e, (set, frozenset)):
        return isinstance(u, (set, frozenset)) and u == e
    try:
        return bool(u == e)
    except Exception:
        return False


def _array_compare(u, e):
    if isinstance(u, (pd.DataFrame, pd.Series)):
        u = u.to_numpy()
    try:
        ua = np.asarray(u)
    except Exception:
        return False, f"Se esperaba un array de NumPy y tu resultado es {_tipo(u)}."
    if not isinstance(u, np.ndarray) and not isinstance(u, (list, tuple)):
        return False, f"Se esperaba un array de NumPy y tu resultado es {_tipo(u)}."
    if ua.shape != e.shape:
        return False, f"Forma distinta: tu array tiene shape {ua.shape} y se esperaba {e.shape}."
    num = np.issubdtype(e.dtype, np.number) or e.dtype == bool
    try:
        if num and (np.issubdtype(ua.dtype, np.number) or ua.dtype == bool):
            ok = np.allclose(ua.astype(float), e.astype(float), rtol=1e-6, atol=1e-6, equal_nan=True)
        else:
            ok = ua.tolist() == e.tolist()
    except Exception:
        ok = False
    return (True, "") if ok else (False, "La forma es correcta pero los valores no coinciden. Revisa el cálculo.")


def pq_compare(u, e, ordered=True, ignore_index=False):
    """Devuelve (ok, mensaje)."""
    if isinstance(e, np.ndarray):
        return _array_compare(u, e)
    if isinstance(e, (pd.DataFrame, pd.Series)):
        if not isinstance(u, type(e)):
            extra = ""
            if isinstance(e, pd.Series) and isinstance(u, pd.DataFrame):
                extra = " Pista: con una sola columna usa df['col'] (corchetes simples)."
            if isinstance(e, pd.DataFrame) and isinstance(u, pd.Series):
                extra = " Pista: usa doble corchete df[['col']] o .reset_index() / .to_frame()."
            return False, f"Tu resultado es {_tipo(u)}, pero se esperaba {_tipo(e)}.{extra}"
        if isinstance(e, pd.DataFrame):
            uc, ec = [str(c) for c in u.columns], [str(c) for c in e.columns]
            if uc != ec:
                if sorted(uc) == sorted(ec):
                    return False, f"Tienes las columnas correctas pero en otro orden. Se esperaba: {ec}"
                faltan = [c for c in ec if c not in uc]
                sobran = [c for c in uc if c not in ec]
                msg = "Las columnas no coinciden."
                if faltan:
                    msg += f" Faltan: {faltan}."
                if sobran:
                    msg += f" Sobran: {sobran}."
                return False, msg
        if u.shape != e.shape:
            return False, f"Forma distinta: tu resultado tiene {u.shape} y se esperaba {e.shape} (filas, columnas)."
        u2, e2 = _norm(u), _norm(e)
        if not ordered:
            u2, e2 = _sort(u2, ignore_index), _sort(e2, ignore_index)
        elif ignore_index:
            u2, e2 = u2.reset_index(drop=True), e2.reset_index(drop=True)
        kw = dict(check_dtype=False, check_names=False, check_index_type=False,
                  check_exact=False, rtol=1e-6, atol=1e-6)
        try:
            if isinstance(e2, pd.DataFrame):
                pd.testing.assert_frame_equal(u2, e2, check_column_type=False, check_freq=False, **kw)
            else:
                pd.testing.assert_series_equal(u2, e2, check_freq=False, **kw)
        except AssertionError as err:
            txt = str(err)
            if "index" in txt.lower() and "values are different" in txt.lower() and "iloc" not in txt:
                return False, "Los valores parecen correctos pero el índice no coincide. ¿Hace falta ordenar o usar reset_index()?"
            if ordered and not ignore_index:
                try:
                    pd.testing.assert_frame_equal(
                        u2.to_frame() if isinstance(u2, pd.Series) else u2,
                        e2.to_frame() if isinstance(e2, pd.Series) else e2,
                        check_like=True, **kw)
                except AssertionError:
                    pass
                else:
                    return False, "Mismos datos, pero en otro orden. Revisa cómo ordenas las filas."
            return False, "Los valores no coinciden con lo esperado. Revisa la lógica y vuelve a intentarlo."
        return True, ""
    if isinstance(u, (pd.DataFrame, pd.Series)):
        return False, f"Tu resultado es {_tipo(u)}, pero se esperaba un valor simple ({type(e).__name__}). ¿Te falta .iloc[0], .sum() o similar?"
    if _scalar_eq(u, e):
        return True, ""
    if u is None:
        return False, ("Tu resultado es None. ¿Te falta un `return` en la función, o guardaste lo que devuelve "
                       "un método que modifica en el lugar (como `.sort()` o `.append()`)?")
    contenedores = (list, tuple, dict, set, str)
    if isinstance(e, contenedores) and not isinstance(u, type(e)) and not (
            isinstance(e, (list, tuple)) and isinstance(u, (list, tuple))):
        return False, f"Tu resultado es {_tipo(u)}, pero se esperaba {_tipo(e)}."
    if isinstance(e, (list, tuple)) and isinstance(u, (list, tuple)) and len(u) != len(e):
        return False, f"Tu resultado tiene {len(u)} elementos y se esperaban {len(e)}."
    if isinstance(e, dict) and isinstance(u, dict) and set(map(str, u)) != set(map(str, e)):
        faltan = [k for k in e if str(k) not in set(map(str, u))]
        sobran = [k for k in u if str(k) not in set(map(str, e))]
        msg = "Las claves del diccionario no coinciden."
        if faltan:
            msg += f" Faltan: {faltan}."
        if sobran:
            msg += f" Sobran: {sobran}."
        return False, msg
    txt = repr(u)
    return False, f"Tu resultado es {txt[:300] + ('…' if len(txt) > 300 else '')}, pero no es el valor esperado."


# ---------------------------------------------------------------- gráficos
def _plt():
    import matplotlib.pyplot as plt
    return plt


def _fig():
    plt = _plt()
    return plt.gcf() if plt.get_fignums() else None


def _ax(i=0):
    f = _fig()
    if f is None or len(f.axes) <= i:
        raise LookupError("no hay ningún gráfico dibujado")
    return f.axes[i]


def _legend(ax=None):
    ax = ax or _ax()
    lg = ax.get_legend()
    return [t.get_text() for t in lg.get_texts()] if lg else []


def _heights(ax=None):
    return [round(float(p.get_height()), 6) for p in (ax or _ax()).patches]


def _widths(ax=None):
    return [round(float(p.get_width()), 6) for p in (ax or _ax()).patches]


def _xticks(ax=None):
    return [t.get_text() for t in (ax or _ax()).get_xticklabels()]


def _hex(color):
    import matplotlib.colors as mcolors
    return mcolors.to_hex(color)


_HELPERS = {"_fig": _fig, "_ax": _ax, "_legend": _legend, "_heights": _heights,
            "_widths": _widths, "_xticks": _xticks, "_hex": _hex}


def pq_prepare():
    """Deja matplotlib limpio antes de ejecutar código (si está cargado)."""
    import sys
    if "matplotlib.pyplot" in sys.modules:
        plt = sys.modules["matplotlib.pyplot"]
        plt.close("all")
        plt.show = lambda *a, **k: None


def pq_check(ns, get_expected, opts):
    """Evalúa el ejercicio.

    ns = namespace del alumno. get_expected = función que devuelve el namespace de la
    solución (solo se ejecuta si hace falta, para no pisar los gráficos del alumno).
    """
    custom = opts.get("custom")
    if custom:
        if opts.get("plot") and _fig() is None:
            return False, "Todavía no hay ningún gráfico. ¡Dibuja algo! 🎨"
        env = dict(_HELPERS)
        env.update(ns)
        try:
            ok = bool(eval(custom, env))
        except Exception as err:
            return False, f"{opts.get('custom_msg', 'Todavía no es correcto.')} ({type(err).__name__}: {err})"
        return ok, "" if ok else opts.get("custom_msg", "Todavía no es correcto. ¡Sigue intentándolo!")
    if "resultado" not in ns:
        return False, "Guarda tu respuesta en la variable `resultado`."
    exp_ns = get_expected() if callable(get_expected) else get_expected
    return pq_compare(ns["resultado"], exp_ns["resultado"],
                      ordered=opts.get("ordered", True),
                      ignore_index=opts.get("ignore_index", False))


_ERR_TIPS = [
    ("truth value of a Series is ambiguous", "Para combinar condiciones usá & (y), | (o) y poné cada condición entre paréntesis."),
    ("can't multiply sequence", "Estás multiplicando un texto (str). ¿El número llegó como texto? Convertilo con int() o float()."),
    ("can only concatenate str", "Estás sumando texto con otra cosa. Convertí con str() para unir textos, o con float() para hacer cuentas."),
    ("unsupported operand type", "Los dos lados de la operación tienen tipos incompatibles (por ejemplo, int + str o None + float). Revisá type() de cada valor."),
    ("could not convert string to float", "Hay un texto que no representa un número (por ejemplo 'n/d' o ''). Filtralo o capturá el ValueError con try/except."),
    ("invalid literal for int", "Hay un texto que no representa un entero. Revisá el valor o usá try/except ValueError."),
    ("index out of range", "Pediste una posición que no existe. Recordá: las posiciones van de 0 a len()-1, y -1 es el último."),
    ("values to unpack", "La cantidad de variables a la izquierda no coincide con la cantidad de valores que llegan."),
    ("ZeroDivisionError", "Dividiste por cero. ¿La lista o el divisor pueden estar vacíos? Verificalo antes de dividir."),
    ("'NoneType' object", "Un valor es None. Suele pasar con una función sin return o con métodos como .sort() que devuelven None."),
    ("KeyError", "Esa clave o columna no existe. Revisá mayúsculas, tildes y espacios; con dicts podés usar .get()."),
    ("NameError", "Usás una variable que no existe (todavía). ¿Error de tipeo o la definiste más abajo?"),
    ("IndentationError", "Revisá la sangría: el contenido de if, for, def, etc. va con 4 espacios."),
    ("SyntaxError", "Error de sintaxis: revisá paréntesis, comillas, dos puntos (:) al final de if/for/def y que cada línea esté completa."),
    ("AttributeError", "Ese método o atributo no existe para este tipo de objeto. Revisá el nombre y qué tipo tiene la variable."),
    ("MergeError", "Revisá las columnas que usás para unir (on / left_on / right_on)."),
    ("TypeError", "Algún tipo de dato no encaja con la operación. Revisá type() de las variables involucradas."),
    ("ValueError", "El tipo es correcto pero el valor no es válido para esta operación."),
]


def pq_error_tip(msg):
    for key, tip in _ERR_TIPS:
        if key in msg:
            return tip
    return ""
