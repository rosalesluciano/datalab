"""Ejecutor para el navegador (Pyodide). Requiere pq_core ya cargado en el mismo namespace."""
import base64
import html
import io
import json
import os
import re
import sys
import traceback
import warnings

os.environ["MPLBACKEND"] = "Agg"  # sin ventana: los gráficos se devuelven como imagen

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from pyodide.code import eval_code  # noqa: E402

warnings.simplefilter("ignore")
pd.set_option("display.max_columns", 30)


def _strip_comments(code):
    return "\n".join(re.sub(r"#.*$", "", line) for line in code.splitlines())


def _render(val):
    if isinstance(val, pd.DataFrame):
        extra = f'<div class="shape">{val.shape[0]} filas × {val.shape[1]} columnas</div>'
        return '<div class="table-wrap">' + val.head(50).to_html(border=0, classes="df", na_rep="NaN") + "</div>" + extra
    if isinstance(val, pd.Series):
        name = "" if val.name is None else f" · nombre: {html.escape(str(val.name))}"
        extra = f'<div class="shape">Series · {len(val)} valores · dtype: {val.dtype}{name}</div>'
        return ('<div class="table-wrap">' + val.head(50).to_frame().to_html(border=0, classes="df", na_rep="NaN", header=val.name is not None)
                + "</div>" + extra)
    if isinstance(val, np.ndarray):
        with np.printoptions(precision=4, suppress=True, threshold=200):
            body = html.escape(repr(val))
        return f'<pre class="val">{body}</pre><div class="shape">ndarray · shape {val.shape} · dtype {val.dtype}</div>'
    if type(val).__module__.startswith(("matplotlib", "seaborn")):
        return ""
    return f'<pre class="val">{html.escape(repr(val))}</pre>'


def _figures():
    if "matplotlib.pyplot" not in sys.modules:
        return []
    plt = sys.modules["matplotlib.pyplot"]
    imgs = []
    for num in plt.get_fignums()[:4]:
        buf = io.BytesIO()
        plt.figure(num).savefig(buf, format="png", dpi=96, bbox_inches="tight")
        imgs.append(base64.b64encode(buf.getvalue()).decode())
    return imgs


def _reset_mpl():
    if "matplotlib.pyplot" in sys.modules:
        plt = sys.modules["matplotlib.pyplot"]
        plt.close("all")
        plt.rcdefaults()


def _format_error(err):
    tb = traceback.extract_tb(err.__traceback__)
    line = None
    for fr in tb:
        if fr.filename == "<exec>":
            line = fr.lineno
    if isinstance(err, SyntaxError):
        line = err.lineno
    msg = f"{type(err).__name__}: {err}"
    return {"msg": msg, "line": line, "tip": pq_error_tip(msg)}  # noqa: F821


def pq_run(setup, code, solution, opts_json, check=True):
    opts = json.loads(opts_json)
    out = io.StringIO()
    res = {"stdout": "", "display": "", "images": [], "error": None, "passed": False, "msg": "", "checked": False}
    _reset_mpl()
    ns = {}
    exec(setup, ns)
    pq_prepare()  # noqa: F821
    ns["_pq_code"] = _strip_comments(code)
    old = sys.stdout, sys.stderr
    sys.stdout = sys.stderr = out
    val = None
    try:
        val = eval_code(code, ns)
    except BaseException as err:  # noqa: BLE001
        res["error"] = _format_error(err)
    finally:
        sys.stdout, sys.stderr = old
    res["stdout"] = out.getvalue()[-15000:]
    try:
        res["images"] = _figures()
    except Exception as err:  # noqa: BLE001
        res["stdout"] += f"\n(No se pudo dibujar el gráfico: {err})"
    if res["error"]:
        _reset_mpl()
        return json.dumps(res)
    try:
        if val is not None:
            res["display"] = _render(val)
        elif ns.get("resultado") is not None:
            res["display"] = _render(ns["resultado"])
    except Exception as err:  # noqa: BLE001
        res["display"] = f"<pre class='val'>No se pudo mostrar: {html.escape(str(err))}</pre>"
    if check:
        def expected():
            exp_ns = {}
            old_out = sys.stdout
            sys.stdout = io.StringIO()  # los print de la solución oficial no deben verse
            try:
                exec(setup, exp_ns)
                exec(solution, exp_ns)
            finally:
                sys.stdout = old_out
            return exp_ns
        try:
            ok, msg = pq_check(ns, expected, opts)  # noqa: F821
        except Exception as err:  # noqa: BLE001
            ok, msg = False, f"No se pudo comparar tu resultado ({type(err).__name__}: {err})"
        res.update(passed=bool(ok), msg=msg, checked=True)
    _reset_mpl()
    return json.dumps(res)


def pq_tables(setup, names_json):
    ns = {}
    exec(setup, ns)
    out = {}
    for n in json.loads(names_json):
        v = ns[n]
        if isinstance(v, pd.DataFrame):
            dtypes = " · ".join(f"{c}: {t}" for c, t in v.dtypes.astype(str).items())
            out[n] = {"html": '<div class="table-wrap">' + v.head(15).to_html(border=0, classes="df", na_rep="NaN") + "</div>",
                      "info": f"DataFrame · {v.shape[0]} filas × {v.shape[1]} columnas", "dtypes": dtypes}
        elif isinstance(v, np.ndarray):
            with np.printoptions(precision=4, suppress=True):
                body = html.escape(repr(v))
            out[n] = {"html": f'<pre class="val">{body}</pre>', "info": f"ndarray · shape {v.shape}", "dtypes": f"dtype: {v.dtype}"}
        else:
            out[n] = {"html": f'<pre class="val">{html.escape(repr(v))}</pre>', "info": type(v).__name__,
                      "dtypes": f"{len(v)} elementos" if hasattr(v, "__len__") else ""}
    _reset_mpl()
    return json.dumps(out)
