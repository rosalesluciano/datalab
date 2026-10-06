# -*- coding: utf-8 -*-
"""Constructores del contenido educativo.

Metodología: CONCEPTO → PROBLEMA → RAZONAMIENTO → ESTRATEGIA → IMPLEMENTACIÓN → VERIFICACIÓN.

Tipos de ejercicio
  A  Reconocimiento   elegir la herramienta/concepto para un problema
  B  Razonamiento     explicar con palabras cómo se resolvería (sin código)
  C  Plan             completar un plan de solución por campos
  D  Código           implementar (con fases Pensar → Planificar → Implementar → Verificar)
  E  Debugging        detectar, explicar y corregir un error
  F  IA copiloto      leer y explicar código generado por una IA
  G  Transferencia    resolver una variante de un ejercicio ya hecho

Cada ejercicio declara `concepts` (ids de fichas) y tres pistas propias (`hints`). Los niveles 4-6
de la escalera de pistas (concepto, ejemplo, solución) se arman automáticamente con la ficha del
concepto, la documentación del ejercicio y `explain` → `pseudo` → `solution`.
"""
import re

TYPES = {
    "A": "Reconocimiento", "B": "Razonamiento", "C": "Plan de solución", "D": "Código",
    "E": "Debugging", "F": "IA copiloto", "G": "Transferencia",
}
LEVELS = {1: "Muy fácil", 2: "Fácil", 3: "Medio", 4: "Difícil", 5: "Desafío"}
CODE_TYPES = {"D", "E", "G"}

POOL = {}  # ejercicios de código heredados (build/pool), por id


def register_pool(exercises):
    for ex in exercises:
        assert ex["id"] not in POOL, ex["id"]
        POOL[ex["id"]] = ex


# ------------------------------------------------------------------ voseo para la documentación heredada
_VOS = [
    ("puedes", "podés"), ("Puedes", "Podés"), ("tienes", "tenés"), ("Tienes", "Tenés"),
    ("quieres", "querés"), ("Quieres", "Querés"), ("necesitas", "necesitás"), ("Necesitas", "Necesitás"),
    ("sabes", "sabés"), ("eres", "sos"), ("usas", "usás"), ("escribes", "escribís"), ("indicas", "indicás"),
    ("pones", "ponés"), ("pasas", "pasás"), ("comparas", "comparás"), ("obtienes", "obtenés"),
    ("haces", "hacés"), ("conviertes", "convertís"), ("aplicas", "aplicás"), ("agrupas", "agrupás"),
    ("ordenas", "ordenás"), ("filtras", "filtrás"), ("escribiste", "escribiste"), ("dibujas", "dibujás"),
    ("entrenas", "entrenás"), ("divides", "dividís"), ("eliges", "elegís"), ("cambias", "cambiás"),
    ("Usa", "Usá"), ("Guarda", "Guardá"), ("Revisa", "Revisá"), ("Escribe", "Escribí"), ("Calcula", "Calculá"),
    ("Recuerda", "Recordá"), ("Fíjate", "Fijate"), ("Piénsalo", "Pensalo"), ("Úsalo", "Usalo"), ("Mira", "Mirá"),
    ("Ten en cuenta", "Tené en cuenta"), ("Imagina", "Imaginá"), ("Prueba a", "Probá a"), ("Elige", "Elegí"),
    ("Evita", "Evitá"), ("Asegúrate", "Asegurate"), ("Recuérdalo", "Recordalo"), ("tú", "vos"),
]
_VOS_RE = [(re.compile(r"(?<![\wáéíóúñ])" + re.escape(a) + r"(?![\wáéíóúñ])"), b) for a, b in _VOS]


def voseo(text):
    if not text:
        return text
    out = []
    for i, seg in enumerate(text.split("```")):
        if i % 2 == 0:  # fuera de bloques de código
            for rx, b in _VOS_RE:
                seg = rx.sub(b, seg)
        out.append(seg)
    return "```".join(out)


# ------------------------------------------------------------------ helpers
def opt(text, ok=False, why=""):
    return {"t": text, "ok": bool(ok), "why": why}


def _opts(options):
    out = []
    for o in options:
        if isinstance(o, dict):
            out.append(o)
        else:
            t, ok, *rest = o
            out.append(opt(t, ok, rest[0] if rest else ""))
    assert any(o["ok"] for o in out), "al menos una opción correcta"
    return out


def concept(id, title, tool, problem, when, signals, can, cant, nomemo, ai, verify, example, check):
    """Ficha de concepto: responde qué problema resuelve, cuándo, cómo reconocerlo, qué puedo y qué NO,
    qué no memorizar, cómo pedírselo a la IA y cómo verificar."""
    q, options = check
    return dict(id=id, title=title, tool=tool, problem=problem, when=when, signals=list(signals),
                can=list(can), cant=list(cant), nomemo=nomemo, ai=ai, verify=verify,
                example=example.strip("\n"), check={"q": q, "options": _opts(options)})


def Q(id, concepts, scenario, options):
    """Pregunta rápida para '¿Sé esto?' y las evaluaciones: escenario → herramienta."""
    return dict(id=id, concepts=list(concepts), scenario=scenario, options=_opts(options))


def _base(type_, id, sec, title, level, concepts, problem, hints, explain="", pseudo=""):
    assert type_ in TYPES
    assert level in LEVELS, (id, level)
    assert concepts, f"{id}: sin conceptos"
    return dict(id=id, type=type_, sec=sec, title=title, level=level, concepts=list(concepts),
                problem=problem.strip("\n"), hints=list(hints or []), explain=explain.strip("\n"),
                pseudo=pseudo.strip("\n"))


def A(id, sec, title, level, concepts, problem, options, explain="", hints=(), multi=False):
    ex = _base("A", id, sec, title, level, concepts, problem, hints, explain)
    ex.update(options=_opts(options), multi=multi)
    return ex


def B(id, sec, title, level, concepts, problem, model, checklist, hints=(), explain=""):
    ex = _base("B", id, sec, title, level, concepts, problem, hints, explain or model)
    ex.update(model=model.strip("\n"), checklist=list(checklist))
    return ex


def field(label, model, options=None, answer=None):
    """Campo de un plan (tipo C). Con `options` es de opción múltiple y se corrige solo."""
    f = {"label": label, "model": model}
    if options:
        f.update(kind="choice", options=list(options), answer=answer)
        assert answer is not None and 0 <= answer < len(options)
    else:
        f["kind"] = "text"
    return f


def C(id, sec, title, level, concepts, problem, fields, explain="", hints=(), pseudo=""):
    ex = _base("C", id, sec, title, level, concepts, problem, hints, explain, pseudo)
    ex.update(fields=list(fields))
    return ex


def D(id, sec, title, level, concepts, problem, starter, solution, hints, explain, pseudo,
      check=None, doc="", sql="", verify=""):
    ex = _base("D", id, sec, title, level, concepts, problem, hints, explain, pseudo)
    ex.update(starter=starter, solution=solution, check=check or {}, doc=doc, sql=sql, verify=verify)
    return ex


def E(id, sec, title, level, concepts, problem, buggy, solution, detect, why, hints, explain="",
      pseudo="", check=None, doc=""):
    """Debugging. `detect` = (pregunta, opciones). `why` = explicación modelo de por qué falla."""
    q, options = detect
    ex = _base("E", id, sec, title, level, concepts, problem, hints, explain or why, pseudo)
    ex.update(starter=buggy, solution=solution, check=check or {}, doc=doc,
              detect={"q": q, "options": _opts(options)}, why=why)
    return ex


def ask(q, options=None, model=""):
    """Pregunta de comprensión para F (con opciones = se corrige sola; sin opciones = abierta)."""
    if options:
        return {"q": q, "kind": "choice", "options": _opts(options)}
    return {"q": q, "kind": "open", "model": model}


def F(id, sec, title, level, concepts, problem, prompt, ai_code, questions, hints=(), explain="",
      bad_prompt="", solution="", check=None):
    """IA copiloto. Si se da `solution`, el código de la IA (o el tuyo) se puede ejecutar y verificar."""
    ex = _base("F", id, sec, title, level, concepts, problem, hints, explain)
    ex.update(prompt=prompt.strip("\n"), bad_prompt=bad_prompt, ai_code=ai_code.strip("\n"),
              questions=list(questions), starter=ai_code.strip("\n"), solution=solution,
              check=check or {})
    return ex


def G(id, sec, title, level, concepts, origin, change, problem, starter, solution, hints, explain,
      pseudo, check=None, doc=""):
    """Transferencia: misma idea que `origin` con una condición distinta (`change`)."""
    ex = _base("G", id, sec, title, level, concepts, problem, hints, explain, pseudo)
    ex.update(origin=origin, change=change, starter=starter, solution=solution, check=check or {}, doc=doc)
    return ex


_OLD_LEVEL = {1: 2, 2: 3, 3: 4, 4: 5}


def P(id, sec, concepts, hints, explain, pseudo, problem=None, level=None, title=None, starter=None,
      verify=""):
    """Reutiliza un ejercicio de código del pool heredado como tipo D, agregando la capa metodológica.
    Su teoría original pasa a ser documentación de consulta (nivel 4-5 de pistas)."""
    src = POOL[id]
    return D(id, sec, title or src["title"], level or _OLD_LEVEL[src["level"]], concepts,
             problem or src["task"], starter if starter is not None else src["starter"], src["solution"],
             hints, explain, pseudo, check=src.get("check", {}), doc=voseo(src["theory"]),
             sql=src.get("sql", ""), verify=verify)


def project(title, story, goal, phases, deliverable, ai_rules):
    """Proyecto integrador. phases = [(nombre, descripción, [ids de ejercicios])]."""
    return dict(title=title, story=story, goal=goal,
                phases=[{"name": n, "desc": d, "ids": list(ids)} for n, d, ids in phases],
                deliverable=list(deliverable), ai_rules=list(ai_rules))


def module(id, num, title, icon, color, desc, learn, why, ai, concepts, exercises, quiz, project,
           setup="", packages=(), micropip=(), tables=(), file="ejercicio.py"):
    return dict(id=id, num=num, title=title, icon=icon, color=color, desc=desc, learn=list(learn),
                why=why, ai=ai, concepts=list(concepts), exercises=list(exercises), quiz=list(quiz),
                project=project, setup=setup, packages=list(packages), micropip=list(micropip),
                tables=list(tables), file=file)


# ------------------------------------------------------------------ validación
def validate(modules):
    ids, cids, qids = set(), {}, set()
    for m in modules:
        for c in m["concepts"]:
            assert c["id"] not in cids, f"concepto repetido {c['id']}"
            cids[c["id"]] = m["id"]
    errors = []
    for m in modules:
        ex_ids = {e["id"] for e in m["exercises"]}
        for e in m["exercises"]:
            if e["id"] in ids:
                errors.append(f"id repetido {e['id']}")
            ids.add(e["id"])
            for c in e["concepts"]:
                if c not in cids:
                    errors.append(f"{e['id']}: concepto inexistente {c}")
            if e["type"] != "A" and len(e["hints"]) < 3:
                errors.append(f"{e['id']}: necesita 3 pistas")
            if e["type"] in CODE_TYPES and not e["explain"]:
                errors.append(f"{e['id']}: falta explain")
            if e["type"] in CODE_TYPES and not e["pseudo"]:
                errors.append(f"{e['id']}: falta pseudocódigo")
            if e["type"] == "G" and e["origin"] not in ex_ids:
                errors.append(f"{e['id']}: origen {e['origin']} no está en el módulo")
        for q in m["quiz"]:
            if q["id"] in qids:
                errors.append(f"pregunta repetida {q['id']}")
            qids.add(q["id"])
            for c in q["concepts"]:
                if c not in cids:
                    errors.append(f"{q['id']}: concepto inexistente {c}")
        for ph in m["project"]["phases"]:
            for i in ph["ids"]:
                if i not in ex_ids:
                    errors.append(f"{m['id']} proyecto: ejercicio {i} no existe")
    assert not errors, "\n".join(errors)
    return True
