"""Valida todo el contenido.

- Ejercicios de código (D, E, G y F ejecutable): la solución pasa su propio corrector y la plantilla
  (o el código con bug, en E) falla.
- Estructura: conceptos existentes, opciones correctas, pistas, campos de plan, proyectos.

Uso:  python tests/test_content.py [-v] [m00 m01 ...]
"""
import os
import re
import sys
import warnings

os.environ["MPLBACKEND"] = "Agg"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "build"))
sys.path.insert(0, os.path.join(ROOT, "py"))

warnings.simplefilter("ignore")

from content import MODULES  # noqa: E402  (importarlo ya ejecuta framework.validate)
from pq_core import pq_check, pq_prepare  # noqa: E402

RUNNABLE = {"D", "E", "G"}


def strip_comments(code):
    return "\n".join(re.sub(r"#.*$", "", line) for line in code.splitlines())


def run(setup, code):
    ns = {}
    exec(setup, ns)
    pq_prepare()
    ns["_pq_code"] = strip_comments(code)
    exec(code, ns)
    return ns


def check_structure(m):
    errs = []
    for c in m["concepts"]:
        if not any(o["ok"] for o in c["check"]["options"]):
            errs.append(f"{c['id']}: la pregunta de la ficha no tiene opción correcta")
    for e in m["exercises"]:
        t = e["type"]
        if t == "A" and not any(o["ok"] for o in e["options"]):
            errs.append(f"{e['id']}: sin opción correcta")
        if t == "B" and (len(e["checklist"]) < 2 or not e["model"]):
            errs.append(f"{e['id']}: razonamiento sin modelo o checklist")
        if t == "C":
            for f in e["fields"]:
                if f["kind"] == "choice" and not (0 <= f["answer"] < len(f["options"])):
                    errs.append(f"{e['id']}: campo {f['label']} con respuesta inválida")
        if t == "E" and not any(o["ok"] for o in e["detect"]["options"]):
            errs.append(f"{e['id']}: detección sin opción correcta")
        if t == "F":
            if not e["questions"]:
                errs.append(f"{e['id']}: IA copiloto sin preguntas")
            for q in e["questions"]:
                if q["kind"] == "choice" and not any(o["ok"] for o in q["options"]):
                    errs.append(f"{e['id']}: pregunta sin opción correcta")
    return errs


def main():
    verbose = "-v" in sys.argv
    only = [a for a in sys.argv[1:] if not a.startswith("-")]
    fails, total, ran = 0, 0, 0
    for m in MODULES:
        if only and m["id"] not in only:
            continue
        for err in check_structure(m):
            fails += 1
            print("FALLA", err)
        setup = m["setup"]
        for ex in m["exercises"]:
            total += 1
            runnable = ex["type"] in RUNNABLE or (ex["type"] == "F" and ex.get("solution"))
            if not runnable:
                continue
            ran += 1
            opts = ex.get("check", {})

            def expected(setup=setup, sol=ex["solution"]):
                return run(setup, sol)

            try:
                exp_ns = run(setup, ex["solution"])
                ok, msg = pq_check(exp_ns, expected, opts)
            except Exception as err:  # noqa: BLE001
                ok, msg = False, f"{type(err).__name__}: {err}"
            if not ok:
                fails += 1
                print(f"FALLA solución {ex['id']}: {msg}")
            if ex["type"] != "F":
                try:
                    st_ns = run(setup, ex["starter"])
                    ok2, _ = pq_check(st_ns, expected, opts)
                except Exception:  # noqa: BLE001
                    ok2 = False
                if ok2:
                    fails += 1
                    print(f"FALLA plantilla {ex['id']}: la plantilla ya pasa el ejercicio")
            if verbose and "resultado" in exp_ns:
                print(f"--- {ex['id']} {ex['title']}\n{exp_ns['resultado']}\n")
    print(f"{len(MODULES)} módulos, {total} ejercicios ({ran} ejecutables), {fails} fallos")
    return fails


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
