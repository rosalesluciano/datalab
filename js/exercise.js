/* DataLab · página de ejercicio: tipos A-G, escalera de pistas, ejecución y verificación */
(() => {
  "use strict";
  const A = window.PQA;
  const { $, $$, esc, md, inline, EX_BY, CON_BY } = A;
  const app = () => $("#app");
  const RUNNABLE = (e) => e.type === "D" || e.type === "E" || e.type === "G" || (e.type === "F" && !!e.solution);
  let editors = [];
  A.clearEditors = () => { editors = []; };

  /* ------------------------------------------------------------------ helpers */
  const plain = (s) => String(s || "").replace(/`/g, "").replace(/\*\*/g, "");
  const minLen = (s, n) => (s || "").trim().length >= n;
  function counter(ta, n, out) {
    const upd = () => { const l = ta.value.trim().length; out.textContent = l >= n ? "✓" : `${l}/${n}`; out.classList.toggle("ok", l >= n); };
    ta.addEventListener("input", upd); upd();
  }
  function moduleOrder(e) { return e.mod.exercises; }

  A.conceptModal = (c) => {
    A.markSeen([c.id]);
    A.modal(`<div class="modal-top"><h2>${esc(c.title)}</h2><button class="btn small" data-close>Cerrar</button></div>
      <code class="tool">${esc(c.tool)}</code>
      <div class="md" style="margin-top:12px"><p><b>Qué problema resuelve:</b> ${inline(c.problem)}</p><p><b>Cuándo:</b> ${inline(c.when)}</p></div>
      <h4>Señales</h4><ul class="signals">${c.signals.map((s) => `<li>${inline(s)}</li>`).join("")}</ul>
      <div class="callout tip">${inline(c.nomemo)}</div>
      <a class="btn small" href="#/c/${c.id}" data-close>Ver ficha completa →</a>`, "wide");
  };

  /* ------------------------------------------------------------------ editor */
  function makeEditor(host, value, { onChange, onRun, readOnly = false } = {}) {
    const cm = CodeMirror(host, {
      value, mode: "python", lineNumbers: true, indentUnit: 4, tabSize: 4, readOnly,
      matchBrackets: true, autoCloseBrackets: true, viewportMargin: Infinity,
      extraKeys: {
        "Ctrl-Enter": () => onRun && onRun(), "Cmd-Enter": () => onRun && onRun(),
        "Ctrl-/": "toggleComment", "Cmd-/": "toggleComment",
        Tab: (c) => (c.somethingSelected() ? c.indentSelection("add") : c.replaceSelection("    ")),
      },
    });
    let tmr;
    if (onChange) cm.on("change", () => { clearTimeout(tmr); tmr = setTimeout(() => onChange(cm.getValue()), 350); });
    setTimeout(() => cm.refresh(), 30);
    editors.push(cm);
    return cm;
  }

  /* ------------------------------------------------------------------ ejecución */
  async function runCode(e, code, ui) {
    const m = e.mod;
    ui.btn.disabled = true;
    ui.btn.innerHTML = A.pyReady ? "⏳ Ejecutando…" : "⏳ Cargando Python…";
    ui.bar.className = "running-bar";
    if ((m.packages.length || m.micropip.length) && !A.libsReady.has(m.id)) {
      ui.btn.innerHTML = "⏳ Cargando librerías…";
      const lr = await A.ensureMod(m);
      if (lr.error) { done(); return { error: lr.error }; }
    }
    const t0 = performance.now();
    const r = await A.py(Object.assign({ type: "run", setup: m.setup, code, solution: e.solution || "", check: e.check || {}, doCheck: !!e.solution }, A.libMsg(m)), 90000);
    if (ui.info) ui.info.textContent = `${Math.round(performance.now() - t0)} ms`;
    done();
    return r;
    function done() { ui.btn.disabled = false; ui.btn.innerHTML = '▶ Ejecutar <span class="kbd">Ctrl+Enter</span>'; ui.bar.className = ""; }
  }

  function renderOutput(out, r, cm, extraOk = "") {
    let verdict = "", status = "nocheck";
    if (r.error) {
      status = "error";
      if (r.error.line && cm) { const ln = r.error.line - 1; cm.addLineClass(ln, "background", "cm-err-line"); cm.__err = ln; }
      verdict = `<div class="verdict bad"><span class="emo">🐞</span><div class="grow"><h4>Error${r.error.line ? ` en la línea ${r.error.line}` : ""}</h4>
        <p><code>${esc(r.error.msg)}</code></p>${r.error.tip ? `<p class="tip">💡 ${esc(r.error.tip)}</p>` : ""}
        <p class="tip">Leé la <b>última línea</b> del error: tipo + mensaje. ¿Qué valor o tipo no es el que esperabas?</p></div></div>`;
    } else if (r.checked && r.passed) {
      status = "pass";
      verdict = `<div class="verdict ok"><span class="emo">✅</span><div class="grow"><h4>Verificado: el resultado coincide</h4><p>Que coincida no alcanza: ¿podrías explicar por qué funciona y qué pasaría si cambian los datos?</p>${extraOk}</div></div>`;
    } else if (r.checked) {
      status = "fail";
      verdict = `<div class="verdict bad"><span class="emo">🤔</span><div class="grow"><h4>Todavía no</h4><p>${inline(r.msg || "El resultado no coincide.")}</p><p class="tip">Compará tu resultado (abajo) con lo que esperabas obtener según tu plan.</p></div></div>`;
    }
    let body = verdict;
    if (r.stdout) body += `<p class="label">Salida (print)</p><pre class="stdout">${esc(r.stdout)}</pre>`;
    if (r.images && r.images.length) body += `<p class="label">Gráfico</p>${r.images.map((b) => `<div class="plot"><img alt="Gráfico generado por el código" src="data:image/png;base64,${b}"></div>`).join("")}`;
    if (r.display) body += `<p class="label">Resultado</p>${r.display}`;
    if (!body) body = '<div class="placeholder">Sin salida. ¿Guardaste algo en <code>resultado</code>?</div>';
    out.innerHTML = body;
    return status;
  }

  // bloque editor + salida reutilizable
  function codeArea(e, host, { initial, file, onPass, onAttempt, toolbarExtra = "" }) {
    host.innerHTML = `<div class="panel editor-card">
        <div class="editor-head">
          <span class="file-tab"><i></i>${esc(file)}</span>
          <div class="editor-actions">${toolbarExtra}
            <button class="btn small ghost" data-act="reset" title="Volver al código inicial">↺ Reiniciar</button>
            <button class="btn small run" data-act="run">▶ Ejecutar <span class="kbd">Ctrl+Enter</span></button>
          </div>
        </div>
        <div class="editor-host"></div>
      </div>
      <div class="panel output">
        <div class="out-head"><span>Resultado</span><span class="out-info"></span></div>
        <div class="run-bar"></div>
        <div class="out-body"><div class="placeholder"><span class="big">🧪</span>Ejecutá con <b>▶</b> o <b>Ctrl + Enter</b>.${e.type !== "F" ? " Guardá tu respuesta en <code>resultado</code> (o lo que pida el ejercicio)." : ""}</div></div>
      </div>`;
    const btn = $("[data-act=run]", host);
    const ui = { btn, bar: $(".run-bar", host), info: $(".out-info", host) };
    const out = $(".out-body", host);
    let running = false;
    const run = async () => {
      if (running) return;
      running = true;
      const code = cm.getValue();
      if (cm.__err != null) { cm.removeLineClass(cm.__err, "background", "cm-err-line"); cm.__err = null; }
      A.S.code[e.id] = code; A.save();
      const r = await runCode(e, code, ui);
      running = false;
      if (!host.isConnected) return;
      if (onAttempt) onAttempt(r);
      const status = renderOutput(out, r, cm);
      if (status === "pass" && onPass) onPass(out, r);
    };
    const cm = makeEditor($(".editor-host", host), initial, { onRun: run, onChange: (v) => { A.S.code[e.id] = v; A.save(); } });
    btn.addEventListener("click", run);
    $("[data-act=reset]", host).addEventListener("click", () => { cm.setValue(e.starter); delete A.S.code[e.id]; A.save(); cm.focus(); });
    return { cm, run, out };
  }

  /* ------------------------------------------------------------------ escalera de pistas */
  const LADDER = ["Pensá", "Dirección", "Herramienta", "Concepto", "Ejemplo", "Solución"];
  function renderLadder(e, el, onChange) {
    const st = () => A.peekEx(e.id);
    const concepts = e.concepts.map((c) => CON_BY[c]);
    const level = (i) => {
      if (i < 3) return `<p>${inline(e.hints[i] || "")}</p>`;
      if (i === 3) return concepts.map((c) => `<div class="mini-concept"><b>${esc(c.title)}</b> <code>${esc(c.tool)}</code><p>${inline(c.problem)}</p><p class="muted small">${inline(c.nomemo)}</p></div>`).join("");
      if (i === 4) {
        if (e.doc) return `<details class="reveal" open><summary>Documentación y ejemplo resuelto similar</summary><div class="md">${md(e.doc)}</div></details>`;
        return concepts.map((c) => `<p class="small"><b>${esc(c.title)}</b> (otros datos):</p>${A.codeBlock(c.example, "python")}`).join("");
      }
      return "";
    };
    const draw = () => {
      const s = st(), h = s.hint || 0, stage = s.solStage || 0;
      const runnable = RUNNABLE(e);
      let html = `<div class="ladder"><div class="ladder-head"><b>Escalera de ayuda</b><span class="muted small">${h}/6</span></div><div class="steps-row">${LADDER.map((n, i) => `<span class="lstep ${i < h ? "on" : ""}">${i + 1}</span>`).join("")}</div>`;
      for (let i = 0; i < Math.min(h, 5); i++) html += `<div class="hint-box"><div class="hl">Nivel ${i + 1} · ${LADDER[i]}</div>${level(i)}</div>`;
      if (h >= 6) {
        html += `<div class="hint-box sol"><div class="hl">Nivel 6 · Solución</div>`;
        html += `<p class="small muted">En tres etapas: primero la idea, después el pseudocódigo y al final el código.</p>`;
        if (stage >= 1) html += `<h5>💡 Idea</h5><div class="md">${md(e.explain || e.model || "")}</div>`;
        if (stage >= 2 && e.pseudo) html += `<h5>🧭 Pseudocódigo</h5>${A.pre(e.pseudo)}`;
        if (stage >= 3) html += solutionBody(e);
        const nextStage = stage < 1 ? "Ver la idea" : stage < 2 && e.pseudo ? "Ver el pseudocódigo" : stage < 3 ? (runnable ? "Ver el código" : "Ver la respuesta modelo") : null;
        if (nextStage) html += `<button class="btn small" data-stage>${nextStage}</button>`;
        html += `</div>`;
      }
      if (h < 6) {
        const needAttempt = h === 5 && runnable && !(s.attempts > 0);
        html += `<button class="btn small ${h >= 4 ? "ghost" : ""}" data-next ${needAttempt ? "disabled" : ""}>💡 ${h === 0 ? "Pedir una pista" : `Siguiente: ${LADDER[h]}`}</button>`;
        if (needAttempt) html += `<p class="muted small">La solución se habilita después de al menos un intento. Probá algo, aunque sea incompleto: el error también enseña.</p>`;
        else if (h >= 3) html += `<p class="muted small">Los niveles 4-6 reducen el peso de este ejercicio como evidencia de dominio.</p>`;
      }
      html += `</div>`;
      el.innerHTML = html;
      const nb = $("[data-next]", el);
      if (nb) nb.addEventListener("click", () => {
        const go = () => { const x = A.exState(e.id); x.hint = Math.min(6, (x.hint || 0) + 1); A.save(); draw(); onChange && onChange(); };
        if (st().hint === 5) A.modal(`<span class="big-emoji">🤔</span><h2>¿Ir a la solución?</h2><p>Antes, probá el botón <b>🤖 Pedir ayuda</b> con un prompt de pista o de concepto. Si igual querés verla, se muestra primero como idea y pseudocódigo.</p><div class="hero-cta center"><button class="btn primary" data-close>Lo intento otra vez</button><button class="btn" id="goSol">Ver la solución por etapas</button></div>`, "center", (card) => $("#goSol", card).addEventListener("click", () => { A.closeModal(); go(); }));
        else go();
      });
      const sb = $("[data-stage]", el);
      if (sb) sb.addEventListener("click", () => {
        const x = A.exState(e.id);
        x.solStage = Math.min(3, (x.solStage || 0) + (x.solStage === 1 && !e.pseudo ? 2 : 1));
        A.save(); draw(); onChange && onChange();
      });
    };
    draw();
    return draw;
  }
  function solutionBody(e) {
    if (RUNNABLE(e)) return `<h5>🧑‍💻 Código</h5>${A.codeBlock(e.solution, "python")}<p class="muted small">Leelo, cerralo y escribilo con tus palabras. Después hacé la transferencia.</p>`;
    if (e.type === "B") return `<h5>📝 Respuesta modelo</h5><div class="md">${md(e.model)}</div>`;
    if (e.type === "C") return `<h5>🧭 Plan modelo</h5><ol class="plan-model">${e.fields.map((f) => `<li><b>${esc(f.label)}:</b> ${inline(f.model)}</li>`).join("")}</ol>`;
    return "";
  }

  /* ------------------------------------------------------------------ página */
  A.renderExercise = (e) => {
    A.clearEditors();
    const m = e.mod, order = moduleOrder(e), idx = order.indexOf(e);
    const prev = order[idx - 1], next = order[idx + 1] || (A.MODS[m.mi + 1] && A.MODS[m.mi + 1].exercises[0]);
    const secItems = order.filter((x) => x.sec === e.sec);
    document.title = `${e.title} · DataLab`;
    A.markSeen(e.concepts);
    const st = A.peekEx(e.id);
    const origin = e.type === "G" ? EX_BY[e.origin] : null;
    const hasLadder = e.type !== "A";
    app().innerHTML = `<div class="ex-page page-enter t-${e.type}">
      <aside class="panel lesson">
        <div class="crumbs"><a href="#/">Ruta</a> / <a href="#/m/${m.id}/practica">${m.icon} ${esc(m.title)}</a> / <span>${esc(e.sec)}</span></div>
        <div class="dots">${secItems.map((x) => `<a href="#/e/${x.id}" title="${esc(x.title)}" class="${A.peekEx(x.id).status} ${x === e ? "current" : ""}"></a>`).join("")}</div>
        <div class="meta">${A.typeBadge(e.type)}${A.levelBadge(e.level)}${st.status === "done" ? '<span class="pill ok">✓ Completado</span>' : ""}</div>
        <h1>${esc(e.title)}</h1>
        <p class="type-hint">${esc(A.TYPE_HINT[e.type])}</p>
        ${origin ? `<div class="callout transfer"><b>🔁 Transferencia de:</b> <a href="#/e/${origin.id}">${esc(origin.title)}</a><br>${inline(e.change)}</div>` : ""}
        <div class="md problem">${md(e.problem)}</div>
        <div class="cchips"><span class="muted small">Conceptos:</span>${e.concepts.map((c) => `<button class="cchip" data-c="${c}">${esc(CON_BY[c].title)}</button>`).join("")}</div>
        <div class="tools">
          ${RUNNABLE(e) || e.type === "F" ? `<button class="btn small" id="tablesBtn">📋 Datos</button>` : ""}
          ${RUNNABLE(e) ? `<a class="btn small ghost" href="${m.colab}" target="_blank" rel="noopener">Colab ↗</a>` : ""}
        </div>
        ${hasLadder ? '<div id="ladder"></div>' : ""}
      </aside>
      <section class="workspace" id="ws"></section>
    </div>
    <div class="ex-nav ex-bottom">
      ${prev ? `<a class="btn ghost small" href="#/e/${prev.id}">← ${esc(prev.title)}</a>` : `<a class="btn ghost small" href="#/m/${m.id}">← Módulo</a>`}
      ${next ? `<a class="btn ghost small" href="#/e/${next.id}">${esc(next.title)} →</a>` : `<a class="btn ghost small" href="#/progreso">🏁 Progreso</a>`}
    </div>`;
    $$(".cchip").forEach((b) => b.addEventListener("click", () => A.conceptModal(CON_BY[b.dataset.c])));
    const tb = $("#tablesBtn"); if (tb) tb.addEventListener("click", () => A.showTables(m));
    const ws = $("#ws");
    let redrawLadder = null;
    if (hasLadder) redrawLadder = renderLadder(e, $("#ladder"));
    const ctx = { e, ws, next, redrawLadder: () => redrawLadder && redrawLadder() };
    ({ A: typeA, B: typeB, C: typeC, D: typeCode, G: typeCode, E: typeE, F: typeF })[e.type](ctx);
    if (RUNNABLE(e)) A.ensureMod(m);
  };

  function doneBox(ctx, msg) {
    const n = ctx.next;
    const tr = A.EX.find((x) => x.type === "G" && x.origin === ctx.e.id);
    return `<div class="panel pad done-box"><h3>✅ ${msg}</h3>
      <div class="hero-cta">${tr ? `<a class="btn primary" href="#/e/${tr.id}">🔁 Transferencia: ${esc(tr.title)}</a>` : ""}${n ? `<a class="btn ${tr ? "" : "primary"}" href="#/e/${n.id}">Siguiente: ${esc(n.title)} →</a>` : ""}</div></div>`;
  }

  /* ------------------------------------------------------------------ A · Reconocimiento */
  function typeA(ctx) {
    const { e, ws } = ctx;
    const done = A.peekEx(e.id).status === "done";
    ws.innerHTML = `<div class="panel pad"><h3 class="h-sec">🎯 ¿Qué concepto o herramienta necesitás?</h3><div class="qcard" id="qa"></div></div><div id="after"></div>`;
    const after = $("#after");
    const finish = () => {
      after.innerHTML = (e.explain ? `<div class="panel pad"><h3 class="h-sec">💡 La idea</h3><div class="md">${md(e.explain)}</div></div>` : "") + doneBox(ctx, "Reconocimiento registrado");
    };
    A.renderChoice($("#qa"), "", e.options, e.id, (ok, first) => {
      if (first) A.ratio(e.concepts, "rec", ok);
      if (!ok) { A.tried(e); return; }
      A.complete(e, { firstOk: first });
      finish();
    }, done);
    if (done) finish();
  }

  /* ------------------------------------------------------------------ B · Razonamiento */
  function typeB(ctx) {
    const { e, ws } = ctx;
    const st = A.exState(e.id);
    ws.innerHTML = `<div class="panel pad">
        <h3 class="h-sec">💭 Explicá con tus palabras</h3>
        <p class="muted small">Sin código. Imaginá que se lo explicás a alguien del equipo.</p>
        <textarea class="ta" id="bText" rows="8" placeholder="Yo lo resolvería…">${esc(st.text || "")}</textarea>
        <div class="row-between"><span class="cnt" id="bCnt"></span><button class="btn primary" id="bSend">Enviar razonamiento</button></div>
      </div><div id="bModel"></div>`;
    const ta = $("#bText");
    counter(ta, 40, $("#bCnt"));
    ta.addEventListener("input", () => { st.text = ta.value; A.save(); });
    const showModel = () => {
      const checks = st.checks || [];
      $("#bModel").innerHTML = `<div class="panel pad"><h3 class="h-sec">📝 Respuesta modelo</h3><div class="md">${md(e.model)}</div>
        <h3 class="h-sec">✔️ Autoevaluación: ¿tu explicación incluyó…?</h3>
        <div class="checklist">${e.checklist.map((c, i) => `<label class="ck"><input type="checkbox" data-i="${i}" ${checks[i] ? "checked" : ""}> ${inline(c)}</label>`).join("")}</div>
        <p class="muted small">Sé honesto: esto mide tu capacidad de explicar, no tu nota.</p>
        <button class="btn primary" id="bSave">${st.status === "done" ? "Actualizar autoevaluación" : "Guardar autoevaluación"}</button></div><div id="bDone"></div>`;
      $("#bSave").addEventListener("click", () => {
        const ck = $$("#bModel input[type=checkbox]").map((x) => x.checked);
        const score = ck.filter(Boolean).length / ck.length;
        const first = st.status !== "done";
        st.checks = ck; st.score = score;
        if (first) {
          const w = A.weightFor(e.id);
          A.practiced(e.concepts);
          A.credit(e.concepts, "exp", score >= 0.6 ? w : 0.5 * w);
        }
        A.complete(e, { score });
        $("#bDone").innerHTML = doneBox(ctx, `Razonamiento registrado (${Math.round(score * 100)}% de las ideas clave)`);
      });
      if (st.status === "done") $("#bDone").innerHTML = doneBox(ctx, `Razonamiento registrado (${Math.round((st.score || 0) * 100)}% de las ideas clave)`);
    };
    $("#bSend").addEventListener("click", () => {
      if (!minLen(ta.value, 40)) { A.toast("✍️", "Escribí un poco más", "Al menos 40 caracteres: tu explicación es lo que se evalúa."); return; }
      st.text = ta.value; st.sent = true; A.tried(e); A.save();
      showModel();
    });
    if (st.sent || st.status === "done") showModel();
  }

  /* ------------------------------------------------------------------ C · Plan */
  function typeC(ctx) {
    const { e, ws } = ctx;
    const st = A.exState(e.id);
    st.fields = st.fields || [];
    ws.innerHTML = `<div class="panel pad"><h3 class="h-sec">🧭 Tu plan de solución</h3><p class="muted small">Todavía no hay código: decidí qué datos, qué operación y cómo verificar.</p>
      <div class="plan-form">${e.fields.map((f, i) => {
        if (f.kind === "choice") {
          const ord = A.shuffled(f.options, e.id + i);
          return `<div class="pf"><label>${i + 1}. ${esc(f.label)}</label><div class="seg" data-i="${i}">${ord.map(([o, oi]) => `<button class="segb ${st.fields[i] === oi ? "on" : ""}" data-o="${oi}">${inline(o)}</button>`).join("")}</div><div class="pf-fb" id="pf${i}"></div></div>`;
        }
        return `<div class="pf"><label for="pt${i}">${i + 1}. ${esc(f.label)}</label><textarea class="ta" id="pt${i}" rows="2" data-i="${i}">${esc(st.fields[i] || "")}</textarea><div class="pf-fb" id="pf${i}"></div></div>`;
      }).join("")}</div>
      <button class="btn primary" id="cCmp">Comparar con el plan modelo</button></div><div id="cDone"></div>`;
    $$(".seg").forEach((seg) => $$(".segb", seg).forEach((b) => b.addEventListener("click", () => {
      if (st.compared) return;
      st.fields[+seg.dataset.i] = +b.dataset.o; A.save();
      $$(".segb", seg).forEach((x) => x.classList.toggle("on", x === b));
    })));
    $$(".plan-form textarea").forEach((ta) => ta.addEventListener("input", () => { st.fields[+ta.dataset.i] = ta.value; A.save(); }));
    const compare = () => {
      st.self = st.self || [];
      e.fields.forEach((f, i) => {
        const fb = $("#pf" + i);
        if (f.kind === "choice") {
          const ok = st.fields[i] === f.answer;
          $$(`.seg[data-i="${i}"] .segb`).forEach((b) => { b.disabled = true; if (+b.dataset.o === f.answer) b.classList.add("right"); else if (b.classList.contains("on")) b.classList.add("wrong"); });
          fb.innerHTML = `<div class="verdict ${ok ? "ok" : "bad"} small">${ok ? "✓" : "✗"} ${inline(f.model)}</div>`;
        } else {
          const ta = $("#pt" + i); ta.readOnly = true;
          const v = st.self[i];
          fb.innerHTML = `<div class="model small"><b>Plan modelo:</b> ${inline(f.model)}</div><div class="selfrate" data-i="${i}"><span class="muted small">¿Coincide en lo esencial?</span>${[["1", "Sí"], ["0.5", "En parte"], ["0", "No"]].map(([k, n]) => `<button class="segb ${v != null && String(v) === k ? "on" : ""}" data-v="${k}">${n}</button>`).join("")}</div>`;
        }
      });
      $$(".selfrate").forEach((sr) => $$(".segb", sr).forEach((b) => b.addEventListener("click", () => {
        st.self[+sr.dataset.i] = +b.dataset.v; A.save();
        $$(".segb", sr).forEach((x) => x.classList.toggle("on", x === b));
      })));
      const btn = $("#cCmp");
      btn.textContent = st.status === "done" ? "Actualizar autoevaluación" : "Guardar plan";
      btn.onclick = save;
    };
    const save = () => {
      const texts = e.fields.map((f, i) => (f.kind === "text" ? i : -1)).filter((i) => i >= 0);
      if (texts.some((i) => st.self[i] == null)) { A.toast("🧭", "Autoevaluá cada campo de texto", "Marcá si coincide con el plan modelo."); return; }
      let score = 0, choices = 0, choiceOk = 0;
      e.fields.forEach((f, i) => {
        if (f.kind === "choice") { choices++; if (st.fields[i] === f.answer) { score++; choiceOk++; } }
        else score += st.self[i];
      });
      score /= e.fields.length;
      const first = st.status !== "done";
      if (first) {
        const w = A.weightFor(e.id);
        A.credit(e.concepts, "exp", score >= 0.6 ? w : 0.5 * w);
        if (choices) A.ratio(e.concepts, "rec", choiceOk === choices);
      }
      A.complete(e, { score });
      $("#cDone").innerHTML = doneBox(ctx, `Plan registrado (${Math.round(score * 100)}% de coincidencia)`);
    };
    $("#cCmp").addEventListener("click", () => {
      const missing = e.fields.some((f, i) => (f.kind === "choice" ? st.fields[i] == null : !minLen(st.fields[i], 5)));
      if (missing) { A.toast("🧭", "Completá todos los campos", "Aunque no estés seguro: lo importante es pensarlo."); return; }
      st.compared = true; A.tried(e); A.practiced(e.concepts); A.save();
      compare();
    });
    if (st.compared) compare();
    if (st.status === "done") $("#cDone").innerHTML = doneBox(ctx, `Plan registrado (${Math.round((st.score || 0) * 100)}% de coincidencia)`);
  }

  /* ------------------------------------------------------------------ D / G · Código */
  function candidates(e) {
    const ids = new Set(e.mod.concepts.map((c) => c.id));
    e.concepts.forEach((c) => ids.add(c));
    return A.shuffled(Array.from(ids), "cand" + e.id).map(([c]) => CON_BY[c]);
  }
  function typeCode(ctx) {
    const { e, ws } = ctx;
    const st = A.exState(e.id);
    st.plan = st.plan || { text: "", tools: [], done: false };
    const isG = e.type === "G";
    const cands = candidates(e);
    ws.innerHTML = `
      <div class="stepper" id="stepper"></div>
      <div class="panel pad plan-card ${st.plan.done ? "collapsed" : ""}" id="planCard">
        <div class="pc-head"><h3 class="h-sec">${isG ? "1-2 · ¿Qué cambia?" : "1 · Pensar"}</h3>${st.plan.done ? '<button class="btn small ghost" id="planEdit">Editar plan</button>' : ""}</div>
        <div class="pc-body">
          <label class="lbl" for="planText">${isG ? "¿Qué cambia respecto del ejercicio original y qué parte de tu solución reutilizás?" : "¿Cómo lo resolverías? Explicalo con tus palabras, sin código: qué datos necesitás, qué operación, qué resultado esperás."}</label>
          <textarea class="ta" id="planText" rows="4" placeholder="${isG ? "Antes hacía… ahora cambia… reutilizo…" : "Necesito… después… el resultado debería ser…"}">${esc(st.plan.text)}</textarea>
          <div class="row-between"><span class="cnt" id="planCnt"></span></div>
          <label class="lbl">${isG ? "" : "2 · Planificar: "}¿Qué conceptos o herramientas creés que necesitás?</label>
          <div class="tools-pick">${cands.map((c) => `<button class="tpick ${st.plan.tools.includes(c.id) ? "on" : ""}" data-c="${c.id}">${esc(c.title)}</button>`).join("")}</div>
          <button class="btn primary" id="planGo">Listo: a implementar →</button>
        </div>
        <div class="pc-summary"><b>Tu plan:</b> ${esc(st.plan.text)}<br><span class="muted small">Herramientas: ${st.plan.tools.map((c) => esc(CON_BY[c].title)).join(", ") || "—"}</span></div>
      </div>
      <div class="impl ${st.plan.done ? "" : "locked"}" id="impl">
        <div class="lock-msg">🔒 Primero pensá y planificá. Es la parte más importante.</div>
        <div id="codeHost"></div>
        <label class="ck ai-ck"><input type="checkbox" id="usedAI" ${st.usedAI ? "checked" : ""}> Usé una IA para escribir parte de este código</label>
      </div>
      <div id="after"></div>`;
    const ta = $("#planText");
    counter(ta, 20, $("#planCnt"));
    ta.addEventListener("input", () => { st.plan.text = ta.value; A.save(); });
    $$(".tpick").forEach((b) => b.addEventListener("click", () => {
      const c = b.dataset.c, i = st.plan.tools.indexOf(c);
      if (i >= 0) st.plan.tools.splice(i, 1); else st.plan.tools.push(c);
      b.classList.toggle("on"); A.save();
    }));
    const stepper = () => {
      const s = A.peekEx(e.id);
      const steps = [["Pensar", s.plan && minLen(s.plan.text, 20)], ["Planificar", s.plan && s.plan.done], ["Implementar", (s.attempts || 0) > 0], ["Comprender", s.usedAI ? !!s.reflection : s.passed ? true : null], ["Verificar", !!s.passed], ["Modificar", null]];
      $("#stepper").innerHTML = steps.map(([n, ok], i) => `<span class="sstep ${ok ? "on" : ""} ${ok === null && i === 3 ? "opt" : ""}"><b>${i + 1}</b>${n}</span>`).join("");
    };
    $("#planGo").addEventListener("click", () => {
      if (!minLen(ta.value, 20)) { A.toast("✍️", "Explicá tu idea primero", "Al menos 20 caracteres. Sin código: con palabras."); return; }
      if (!st.plan.tools.length) { A.toast("🧰", "Elegí al menos una herramienta", "¿Qué conceptos creés que vas a usar?"); return; }
      st.plan.done = true; A.practiced(e.concepts); A.save();
      A.renderExercise(e);
    });
    const pe = $("#planEdit");
    if (pe) pe.addEventListener("click", () => $("#planCard").classList.toggle("collapsed"));
    $("#usedAI").addEventListener("change", (ev) => { st.usedAI = ev.target.checked; A.save(); stepper(); });
    const aiBtn = `<button class="btn small ghost" data-act="ai" title="Prompts para pedir ayuda progresiva">🤖 Pedir ayuda</button>`;
    const area = codeArea(e, $("#codeHost"), {
      initial: A.S.code[e.id] != null ? A.S.code[e.id] : e.starter,
      file: e.mod.file, toolbarExtra: aiBtn,
      onAttempt: (r) => { if (!(r.checked && r.passed)) { A.tried(e); stepper(); ctx.redrawLadder(); } else { const x = A.exState(e.id); x.attempts = (x.attempts || 0) + 1; A.save(); } },
      onPass: () => { st.passed = true; A.save(); onPassed(); },
    });
    $("[data-act=ai]", ws).addEventListener("click", () => aiHelp(e, area.cm, () => { st.usedAI = true; $("#usedAI").checked = true; A.save(); stepper(); }));
    if (!st.plan.done) setTimeout(() => ta.focus(), 50);

    function onPassed() {
      stepper();
      const after = $("#after");
      const chosen = new Set(st.plan.tools), needed = e.concepts.filter((c) => cands.some((x) => x.id === c));
      const hit = needed.filter((c) => chosen.has(c)), miss = needed.filter((c) => !chosen.has(c)), extra = [...chosen].filter((c) => !e.concepts.includes(c));
      const toolsFb = `<div class="panel pad"><h3 class="h-sec">🧰 ¿Elegiste bien las herramientas?</h3>
        ${hit.length ? `<p>✓ Acertaste: ${hit.map((c) => `<b>${esc(CON_BY[c].title)}</b>`).join(", ")}</p>` : ""}
        ${miss.length ? `<p>➕ También se usaba: ${miss.map((c) => `<b>${esc(CON_BY[c].title)}</b>`).join(", ")}</p>` : ""}
        ${extra.length ? `<p class="muted">Elegiste además: ${extra.map((c) => esc(CON_BY[c].title)).join(", ")} (no hacía falta, pero pensarlo no está mal).</p>` : ""}
        <p class="small"><b>Cómo verificar en serio:</b> ${inline(e.verify || CON_BY[e.concepts[0]].verify)}</p></div>`;
      const creditNow = () => {
        if (st.credited) return;
        st.credited = true;
        const w = A.weightFor(e.id) * (st.usedAI ? 0.75 : 1);
        A.credit(e.concepts, isG ? "trf" : "res", w);
        if (minLen(st.plan.text, 20)) A.credit(e.concepts, "exp", 0.25);
        if (!st.recCounted) { st.recCounted = true; A.ratio(needed.length ? needed : e.concepts, "rec", !needed.length || hit.length / needed.length >= 0.5); }
        A.complete(e);
      };
      if (st.usedAI && !st.reflection) {
        after.innerHTML = toolsFb + `<div class="panel pad reflect"><h3 class="h-sec">4 · Comprender el código</h3>
          <p>Marcaste que usaste IA. Para que cuente como resuelto, explicá el código con tus palabras:</p>
          <ul class="small"><li>¿Qué hace cada línea clave?</li><li>¿Qué tipo de objeto devuelve y por qué?</li><li>¿Qué pasaría si cambian los datos o falta una columna?</li></ul>
          <textarea class="ta" id="refl" rows="6" placeholder="La línea … hace … devuelve … si falta …"></textarea>
          <div class="row-between"><span class="cnt" id="reflCnt"></span><button class="btn primary" id="reflGo">Guardar explicación</button></div></div>`;
        counter($("#refl"), 80, $("#reflCnt"));
        $("#reflGo").addEventListener("click", () => {
          const v = $("#refl").value;
          if (!minLen(v, 80)) { A.toast("🧠", "Explicá un poco más", "Al menos 80 caracteres."); return; }
          st.reflection = v; A.ratio(e.concepts, "comp", true); A.credit(e.concepts, "exp", 0.5); A.save();
          creditNow(); onPassed();
        });
        return;
      }
      creditNow();
      const tr = A.EX.find((x) => x.type === "G" && x.origin === e.id);
      after.innerHTML = toolsFb + (tr ? "" : `<div class="panel pad"><h3 class="h-sec">6 · Modificar</h3><p>Cambiá una condición vos mismo (otra columna, otra métrica, otro filtro), predecí el resultado y ejecutalo. Si podés adaptarlo sin ayuda, lo aprendiste.</p></div>`) + doneBox(ctx, isG ? "Transferencia lograda" : "Ejercicio resuelto y verificado");
    }
    stepper();
    if (st.passed) onPassed();
  }

  /* ------------------------------------------------------------------ prompts de ayuda */
  function aiHelp(e, cm, onCodeAsked) {
    const st = A.peekEx(e.id);
    const problem = plain(e.problem), plan = (st.plan && st.plan.text) || "(todavía no escribí un plan)", code = cm ? cm.getValue() : "";
    const lib = e.mod.title;
    const P = [
      ["Pista", `Estoy aprendiendo ${lib}. Problema: ${problem}\n\nMi idea: ${plan}\n\nNo me des la solución ni código. Dame solo una pista sobre qué debería pensar a continuación.`, false],
      ["Concepto", `Estoy aprendiendo ${lib}. No me queda claro el concepto de ${e.concepts.map((c) => CON_BY[c].title).join(" / ")}. Explicámelo con un ejemplo de datos distinto a este problema (no lo resuelvas): ${problem}`, false],
      ["Revisar mi código", `Problema: ${problem}\n\nMi código:\n${code}\n\nNo lo reescribas. Decime qué línea tiene el problema y por qué, para que lo corrija yo.`, false],
      ["Explicar un error", `Este es mi código:\n${code}\n\nMe da un error al ejecutarlo. Explicame qué significa el error y qué debería imprimir para encontrar la causa. No me des el código corregido.`, false],
      ["Código (último recurso)", `Problema: ${problem}\n\nMi plan: ${plan}\n\nEscribí el código siguiendo MI plan, con un comentario en cada paso, y explicá qué devuelve cada línea. Después haceme 3 preguntas para comprobar que lo entendí.`, true],
    ];
    A.modal(`<div class="modal-top"><h2>🤖 Pedir ayuda a una IA</h2><button class="btn small" data-close>Cerrar</button></div>
      <p class="muted">Usá el escalón <b>más bajo</b> que te destrabe. Copiá el prompt y pegalo en tu IA (Claude, ChatGPT, etc.). Ya incluye tu problema, tu plan y tu código.</p>
      <div class="prompt-ladder">${P.map(([t, p, last], i) => `<div class="pl-item ${last ? "last" : ""}"><div class="pl-h"><b>${i + 1} · ${esc(t)}</b><button class="btn small" data-i="${i}">Copiar</button></div><pre class="plain">${esc(p)}</pre></div>`).join("")}</div>
      <p class="small muted">Si copiás el prompt de código, se marca "Usé IA" y vas a tener que explicar el código antes de que cuente como resuelto.</p>`, "wide", (card) => {
      $$("[data-i]", card).forEach((b) => b.addEventListener("click", async () => {
        const [, p, last] = P[+b.dataset.i];
        await A.copy(p, b);
        if (last) onCodeAsked();
      }));
    });
  }

  /* ------------------------------------------------------------------ E · Debugging */
  function typeE(ctx) {
    const { e, ws } = ctx;
    const st = A.exState(e.id);
    ws.innerHTML = `
      <div class="panel pad"><div class="steps3" id="steps3"></div>
        <h3 class="h-sec">1 · Detectar</h3><p class="muted small">Tip: ejecutá primero el código con el error (abajo) y leé el mensaje.</p><div class="qcard" id="det"></div>
        <h3 class="h-sec">2 · Explicar por qué ocurre</h3>
        <textarea class="ta" id="why" rows="3" placeholder="Falla porque…">${esc(st.why || "")}</textarea>
        <div class="row-between"><span class="cnt" id="whyCnt"></span><button class="btn small" id="whyGo">${st.why ? "Actualizar" : "Guardar explicación"}</button></div>
        <div id="whyModel"></div>
      </div>
      <h3 class="h-sec ws-title">3 · Corregir</h3>
      <div id="codeHost"></div><div id="after"></div>`;
    const steps = () => {
      const s = A.peekEx(e.id);
      $("#steps3").innerHTML = [["Detectar", s.detect != null], ["Explicar", !!s.why], ["Corregir", !!s.passed]].map(([n, ok], i) => `<span class="sstep ${ok ? "on" : ""}"><b>${i + 1}</b>${n}</span>`).join("");
    };
    A.renderChoice($("#det"), e.detect.q, e.detect.options, e.id, (ok, first) => {
      if (first) { st.detect = ok; st.detectFirst = ok; A.save(); }
      if (!ok) A.tried(e);
      else { st.detect = true; A.save(); }
      steps(); maybeDone();
    }, st.detect === true);
    const ta = $("#why");
    counter(ta, 20, $("#whyCnt"));
    const showWhy = () => { $("#whyModel").innerHTML = `<div class="model"><b>Explicación modelo:</b> ${inline(e.why)}</div>`; };
    $("#whyGo").addEventListener("click", () => {
      if (!minLen(ta.value, 20)) { A.toast("✍️", "Explicá la causa", "Al menos 20 caracteres."); return; }
      st.why = ta.value; A.save(); showWhy(); steps(); maybeDone();
    });
    if (st.why) showWhy();
    const area = codeArea(e, $("#codeHost"), {
      initial: A.S.code[e.id] != null ? A.S.code[e.id] : e.starter, file: e.mod.file,
      toolbarExtra: `<button class="btn small ghost" data-act="ai">🤖 Pedir ayuda</button>`,
      onAttempt: (r) => { if (!(r.checked && r.passed)) { A.tried(e); ctx.redrawLadder(); } },
      onPass: () => { st.passed = true; A.save(); steps(); maybeDone(true); },
    });
    $("[data-act=ai]", ws).addEventListener("click", () => aiHelp(e, area.cm, () => { st.usedAI = true; A.save(); }));
    function maybeDone(justPassed) {
      const s = A.peekEx(e.id), after = $("#after");
      if (!s.passed) return;
      if (s.detect == null || !s.why) {
        if (justPassed || !after.innerHTML) after.innerHTML = `<div class="panel pad"><p>✅ Código corregido. Completá los pasos <b>1 (detectar)</b> y <b>2 (explicar)</b> para registrar el ejercicio: entender el error es lo que se aprende.</p></div>`;
        return;
      }
      if (!s.credited) {
        s.credited = true;
        const w = A.weightFor(e.id) * (s.usedAI ? 0.75 : 1);
        A.credit(e.concepts, "dbg", w * (s.detectFirst ? 1 : 0.6));
        A.credit(e.concepts, "exp", 0.5);
        A.complete(e);
      }
      after.innerHTML = doneBox(ctx, "Bug encontrado, explicado y corregido");
    }
    steps();
    maybeDone();
  }

  /* ------------------------------------------------------------------ F · IA copiloto */
  function typeF(ctx) {
    const { e, ws } = ctx;
    const st = A.exState(e.id);
    st.qa = st.qa || {};
    ws.innerHTML = `
      <div class="panel pad"><h3 class="h-sec">🗣️ El prompt</h3>
        <div class="prompt-box good"><span class="tag">✅ Prompt que te hace aprender</span><p>${esc(e.prompt)}</p><button class="btn small" id="cpP">Copiar</button></div>
        ${e.bad_prompt ? `<div class="prompt-box bad"><span class="tag">❌ Prompt que te hace dependiente</span><p>${esc(e.bad_prompt)}</p></div>` : ""}
      </div>
      <h3 class="h-sec ws-title">🤖 Lo que respondió la IA</h3>
      <p class="muted small ws-sub">${e.solution ? "Ejecutalo, cambialo y observá. También podés pegar acá el código de tu propia IA." : "Leelo con atención antes de responder."}</p>
      <div id="codeHost"></div>
      <div class="panel pad"><h3 class="h-sec">🧠 Demostrá que lo entendés</h3><div id="qs"></div></div>
      <div id="after"></div>`;
    $("#cpP").addEventListener("click", (ev) => A.copy(e.prompt, ev.currentTarget));
    if (e.solution) codeArea(e, $("#codeHost"), { initial: A.S.code[e.id] != null ? A.S.code[e.id] : e.ai_code, file: "respuesta_ia.py", onAttempt: () => {} });
    else $("#codeHost").innerHTML = `<div class="panel">${A.codeBlock(e.ai_code, "python")}</div>`;
    const qs = $("#qs");
    qs.innerHTML = e.questions.map((q, i) => `<div class="fq" id="fq${i}"><div class="fq-n">${i + 1}</div><div class="fq-b"></div></div>`).join("");
    e.questions.forEach((q, i) => {
      const host = $(`#fq${i} .fq-b`);
      if (q.kind === "choice") {
        A.renderChoice(host, q.q, q.options, e.id + i, (ok, first) => {
          if (first) st.qa[i] = ok ? 1 : 0;
          if (!ok) A.tried(e);
          A.save(); check();
        }, st.qa[i] === 1, { revealOnFail: true });
        if (st.qa[i] === 0) { /* respondida mal antes: se muestra como respondida */ }
      } else {
        const saved = st.qa[i];
        host.innerHTML = `<p class="q">${inline(q.q)}</p><textarea class="ta" rows="3" placeholder="Con tus palabras…">${esc((saved && saved.text) || "")}</textarea>
          <div class="row-between"><span class="cnt"></span><button class="btn small">Ver respuesta modelo</button></div><div class="om"></div>`;
        const ta = $("textarea", host), om = $(".om", host);
        counter(ta, 15, $(".cnt", host));
        const showModel = () => {
          const v = st.qa[i] && st.qa[i].self;
          om.innerHTML = `<div class="model"><b>Respuesta modelo:</b> ${inline(q.model)}</div><div class="selfrate"><span class="muted small">¿Coincide en lo esencial?</span>${[["1", "Sí"], ["0.5", "En parte"], ["0", "No"]].map(([k, n]) => `<button class="segb ${v != null && String(v) === k ? "on" : ""}" data-v="${k}">${n}</button>`).join("")}</div>`;
          $$(".segb", om).forEach((b) => b.addEventListener("click", () => { st.qa[i].self = +b.dataset.v; A.save(); $$(".segb", om).forEach((x) => x.classList.toggle("on", x === b)); check(); }));
        };
        $("button.btn", host).addEventListener("click", () => {
          if (!minLen(ta.value, 15)) { A.toast("✍️", "Respondé primero con tus palabras", "Después compará con el modelo."); return; }
          st.qa[i] = Object.assign(st.qa[i] || {}, { text: ta.value }); A.save(); showModel(); check();
        });
        if (saved && saved.text) showModel();
      }
    });
    function check() {
      const all = e.questions.every((q, i) => (q.kind === "choice" ? st.qa[i] != null : st.qa[i] && st.qa[i].self != null));
      if (!all) return;
      if (!st.credited) {
        st.credited = true;
        const ch = e.questions.map((q, i) => (q.kind === "choice" ? st.qa[i] : null)).filter((x) => x !== null);
        const r = ch.length ? ch.reduce((a, b) => a + b, 0) / ch.length : 1;
        const op = e.questions.map((q, i) => (q.kind === "open" ? st.qa[i].self : null)).filter((x) => x !== null);
        const o = op.length ? op.reduce((a, b) => a + b, 0) / op.length : 0;
        const w = A.weightFor(e.id);
        A.ratio(e.concepts, "comp", r >= 0.7);
        if (op.length) A.credit(e.concepts, "exp", w * (o >= 0.5 ? 0.75 : 0.35));
        st.score = r;
        A.complete(e, { score: r });
      }
      $("#after").innerHTML = doneBox(ctx, `Comprensión registrada (${Math.round((st.score || 0) * 100)}% en preguntas cerradas)`);
    }
    check();
  }
})();
