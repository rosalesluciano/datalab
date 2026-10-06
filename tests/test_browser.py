"""Prueba end-to-end en Chromium real (Pyodide).

1. Recorre todas las vistas y verifica que no haya errores de consola ni desborde horizontal (escritorio y móvil).
2. Ejecuta en el worker de Pyodide la solución de cada ejercicio ejecutable (debe aprobar) y su
   plantilla / código con bug (no debe aprobar).
3. Recorre por la interfaz un ejercicio de código completo: bloqueo → plan → error → solución → crédito.

Uso:  python -m http.server 8765  (en la raíz)  y luego  python tests/test_browser.py [url]
Requiere: pip install playwright && playwright install chromium
"""
import sys

from playwright.sync_api import sync_playwright

URL = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8765/"

ROUTES = ["#/", "#/m/m00", "#/m/m01/practica", "#/m/m02/conceptos", "#/m/m03/proyecto", "#/m/m04/evaluacion",
          "#/m/m05/repaso", "#/m/m06", "#/c/pd-groupby", "#/e/py-a01", "#/e/py-b01", "#/e/py-c01", "#/e/py-d01",
          "#/e/py-e01", "#/e/py-f01", "#/e/py-g01", "#/quiz", "#/ia", "#/progreso"]

RUN_ALL = """async () => {
  const A = window.__pq.A, fails = []; let n = 0;
  const run = (e, code) => A.py(Object.assign({type: 'run', setup: e.mod.setup, code, solution: e.solution,
      check: e.check || {}, doCheck: true}, A.libMsg(e.mod)), 240000);
  for (const m of A.MODS) {
    await A.ensureMod(m);
    for (const e of m.exercises) {
      if (!(['D', 'E', 'G'].includes(e.type) || (e.type === 'F' && e.solution))) continue;
      n++;
      const r = await run(e, e.solution);
      if (!(r.checked && r.passed)) fails.push(e.id + ': ' + ((r.error && r.error.msg) || r.msg));
      if (e.type !== 'F') { const r2 = await run(e, e.starter); if (r2.checked && r2.passed) fails.push(e.id + ': la plantilla aprueba'); }
    }
  }
  return {n, fails};
}"""

OVERFLOW = """() => [...document.querySelectorAll('#app *, .topbar *')].filter(el => {
  const r = el.getBoundingClientRect();
  return r.width > 0 && r.right > innerWidth + 1 && !el.closest('.CodeMirror, .table-wrap, .md-table, .matrix, .mtabs, pre, .tabs');
}).length"""


def main():
    errors, fails = [], []
    with sync_playwright() as p:
        b = p.chromium.launch()
        page = b.new_page(viewport={"width": 1400, "height": 900})
        page.on("pageerror", lambda e: errors.append(f"pageerror: {e}"))
        page.on("console", lambda m: m.type == "error" and errors.append(f"console: {m.text}"))
        page.goto(URL)
        page.wait_for_selector(".py-status.ready", timeout=180000)

        for vw in (1400, 375):
            page.set_viewport_size({"width": vw, "height": 900})
            for r in ROUTES:
                page.goto(URL + r)
                page.wait_for_timeout(350)
                if page.is_visible("#gateGo"):
                    page.click("#gateGo")
                n = page.evaluate(OVERFLOW)
                if n:
                    fails.append(f"{r} @ {vw}px: {n} elementos desbordan")
        page.set_viewport_size({"width": 1400, "height": 900})

        # flujo completo de un ejercicio de código por la interfaz
        page.goto(URL + "#/e/py-d01")
        page.wait_for_selector("#impl.locked")
        page.fill("#planText", "Calculo el subtotal y después aplico el descuento del 10 por ciento")
        page.click(".tpick >> text=Números y operaciones")
        page.click("#planGo")
        page.wait_for_selector("#impl:not(.locked)")
        page.evaluate("document.querySelector('#codeHost .CodeMirror').CodeMirror.setValue('resultado = precio * 3')")
        page.click("[data-act=run]")
        page.wait_for_selector(".out-body .verdict.bad", timeout=60000)
        sol = page.evaluate("window.__pq.A.EX_BY['py-d01'].solution")
        page.evaluate(f"document.querySelector('#codeHost .CodeMirror').CodeMirror.setValue({sol!r})")
        page.click("[data-act=run]")
        page.wait_for_selector(".out-body .verdict.ok", timeout=60000)
        st = page.evaluate("window.__pq.state.ex['py-d01'].status")
        if st != "done":
            fails.append(f"py-d01 no quedó completado ({st})")

        res = page.evaluate(RUN_ALL)
        print("ejercicios ejecutables:", res["n"])
        fails += res["fails"]
        b.close()
    for e in errors + fails:
        print("FALLA", e)
    print("OK" if not (errors or fails) else f"{len(errors) + len(fails)} problemas")
    return 1 if (errors or fails) else 0


if __name__ == "__main__":
    sys.exit(main())
