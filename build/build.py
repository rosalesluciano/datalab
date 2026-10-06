"""Genera js/data.js y notebooks/*.ipynb a partir de content.py.

Uso:  python build/build.py
"""
import base64
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "build"))

from content import LEVELS, MODULES, TYPES  # noqa: E402

REPO = "rosalesluciano/datalab"
SITE = "https://rosalesluciano.github.io/datalab/"
RUNNABLE = {"D", "E", "G"}


def colab_url(mid):
    return f"https://colab.research.google.com/github/{REPO}/blob/main/notebooks/{mid}.ipynb"


def is_runnable(ex):
    return ex["type"] in RUNNABLE or (ex["type"] == "F" and bool(ex.get("solution")))


def build_data():
    mods = []
    for m in MODULES:
        d = dict(m)
        d["colab"] = colab_url(m["id"])
        mods.append(d)
    data = {"modules": mods, "types": TYPES, "levels": {str(k): v for k, v in LEVELS.items()}}
    out = os.path.join(ROOT, "js", "data.js")
    with open(out, "w", encoding="utf-8") as f:
        f.write("// Generado por build/build.py - no editar a mano\n")
        f.write("window.PQ = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n")
    return out


def md_cell(src):
    return {"cell_type": "markdown", "metadata": {}, "source": src}


def code_cell(src, form=False):
    meta = {"cellView": "form"} if form else {}
    return {"cell_type": "code", "execution_count": None, "metadata": meta, "outputs": [], "source": src}


NB_HELPERS = r'''
import base64 as _b64, json as _json, re as _re, warnings as _w
_w.simplefilter("ignore")
_SOL = _json.loads(_b64.b64decode(_SOL_B64).decode("utf-8"))

def reiniciar_datos():
    """Vuelve a cargar todos los datos limpios (cada ejercicio empieza de cero)."""
    globals().pop("resultado", None)
    exec(_SETUP, globals())
    pq_prepare()

def _codigo_celda():
    try:
        src = get_ipython().history_manager.input_hist_raw[-1]
    except Exception:
        return ""
    src = "\n".join(l for l in src.splitlines() if "comprobar(" not in l)
    return "\n".join(_re.sub(r"#.*$", "", l) for l in src.splitlines())

def comprobar(ej):
    info = _SOL[ej]
    def esperado():
        exp_ns = {}
        exec(_SETUP, exp_ns)
        exec(info["solution"], exp_ns)
        return exp_ns
    g = globals()
    g["_pq_code"] = _codigo_celda()
    ok, msg = pq_check(g, esperado, info["check"])
    from IPython.display import HTML, display
    import html as _h
    if ok:
        display(HTML('<div style="padding:12px 16px;border-radius:12px;background:#0f9d6e;color:#fff;'
                     'font:600 15px system-ui">✅ Verificado. Ahora explicá con tus palabras por qué funciona '
                     'y probá una variante.</div>'))
    else:
        display(HTML('<div style="padding:12px 16px;border-radius:12px;background:#b4235a;color:#fff;'
                     'font:500 15px system-ui">Todavía no. ' + _h.escape(msg) + '</div>'))
    if "resultado" in g:
        return g["resultado"]

def ver_pista(ej, nivel=1):
    """Pistas progresivas (1-3). Pedí la siguiente solo si la anterior no alcanzó."""
    pistas = _SOL[ej]["hints"]
    print(f"Pista {nivel}/{len(pistas)}: {pistas[min(nivel, len(pistas)) - 1]}")

def ver_solucion(ej):
    """Último recurso: primero la idea, después el pseudocódigo y al final el código."""
    info = _SOL[ej]
    print("💡 Idea:\n" + info["explain"] + "\n")
    print("🧭 Pseudocódigo:\n" + info["pseudo"] + "\n")
    print("🧑‍💻 Código:\n" + info["solution"])

reiniciar_datos()
print("✅ Datos cargados:", ", ".join(_TABLAS))
'''


def build_notebooks():
    core = open(os.path.join(ROOT, "py", "pq_core.py"), encoding="utf-8").read()
    os.makedirs(os.path.join(ROOT, "notebooks"), exist_ok=True)
    paths = []
    for m in MODULES:
        exs = [e for e in m["exercises"] if is_runnable(e)]
        sols = {e["id"]: {"solution": e["solution"], "check": e.get("check", {}), "hints": e["hints"],
                          "explain": e["explain"], "pseudo": e["pseudo"]} for e in exs}
        b64 = base64.b64encode(json.dumps(sols, ensure_ascii=False).encode("utf-8")).decode()
        tablas = m["tables"] + (["conn (SQLite)"] if "sqlite3" in m["packages"] else [])
        setup_cell = (
            "#@title ⚙️ 1) Ejecutá esta celda primero (datos y verificador) { display-mode: \"form\" }\n"
            + core + "\n\n_SETUP = " + repr(m["setup"]) + "\n_SOL_B64 = " + repr(b64)
            + "\n_TABLAS = " + repr(tablas) + "\n" + NB_HELPERS
        )
        conceptos = "\n".join(f"- **{c['title']}**: {c['problem']}" for c in m["concepts"])
        cells = [
            md_cell(f"# {m['icon']} Módulo {m['num']} · {m['title']}\n\n{m['desc']}\n\n"
                    f"Versión web con conceptos, reconocimiento, razonamiento y proyecto: [{SITE}]({SITE}#/m/{m['id']})\n\n"
                    "## Cómo trabajar este notebook\n"
                    "1. Ejecutá la celda ⚙️ (carga datos y verificador).\n"
                    "2. **Antes de escribir código**, escribí en un comentario cómo lo vas a resolver.\n"
                    "3. Implementá y guardá tu respuesta en `resultado` (o lo que pida el ejercicio).\n"
                    "4. `comprobar()` verifica. Si te trabás: `ver_pista(\"id\", 1)`, después 2 y 3.\n"
                    "5. `ver_solucion(\"id\")` es el último recurso: muestra idea → pseudocódigo → código.\n\n"
                    f"## Conceptos del módulo\n{conceptos}"),
            code_cell(setup_cell, form=True),
        ]
        prev_sec = None
        for n, ex in enumerate(exs, 1):
            if ex["sec"] != prev_sec:
                cells.append(md_cell(f"---\n# 📌 {ex['sec']}"))
                prev_sec = ex["sec"]
            md = (f"## {n}. {ex['title']}\n`{TYPES[ex['type']]}` · `{LEVELS[ex['level']]}`\n\n{ex['problem']}")
            if ex["type"] == "G":
                md += f"\n\n> 🔁 **Qué cambia:** {ex['change']}"
            if ex["type"] == "E":
                md += "\n\n> 🐞 El código tiene un error: ejecutalo, leé el mensaje, explicá la causa en un comentario y corregilo."
            if ex["type"] == "F":
                md += f"\n\n> 🤖 Prompt usado:\n> {ex['prompt']}\n\nAntes de ejecutarlo, explicá en comentarios qué hace cada línea."
            cells.append(md_cell(md))
            plan = "# Mi plan (con mis palabras, antes de programar):\n# \n\n" if ex["type"] in ("D", "G") else ""
            cells.append(code_cell(f"reiniciar_datos()  # datos limpios\n\n{plan}{ex['starter']}\n\ncomprobar(\"{ex['id']}\")"))
        cells.append(md_cell(f"---\n# 🏁 Fin del notebook\nVolvé a la [plataforma]({SITE}) para los ejercicios de "
                             "reconocimiento, razonamiento y el modo **¿Sé esto?**."))
        nb = {"cells": cells, "metadata": {
            "colab": {"provenance": [], "name": f"{m['id']}.ipynb"},
            "kernelspec": {"display_name": "Python 3", "name": "python3"},
            "language_info": {"name": "python"}}, "nbformat": 4, "nbformat_minor": 0}
        p = os.path.join(ROOT, "notebooks", f"{m['id']}.ipynb")
        with open(p, "w", encoding="utf-8") as f:
            json.dump(nb, f, ensure_ascii=False, indent=1)
        paths.append(p)
    return paths


if __name__ == "__main__":
    print(build_data())
    for p in build_notebooks():
        print(p)
