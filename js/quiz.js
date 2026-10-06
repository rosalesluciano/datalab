/* DataLab · "¿Sé esto?" (reconocimiento aleatorio) y evaluaciones por módulo */
(() => {
  "use strict";
  const A = window.PQA;
  const { $, $$, esc, md, MODS, CON_BY } = A;
  const app = () => $("#app");

  // banco de preguntas: preguntas rápidas del módulo + ejercicios de reconocimiento (A)
  function poolFor(mods) {
    const items = [];
    mods.forEach((m) => {
      m.quiz.forEach((q) => items.push({ id: q.id, mod: m, concepts: q.concepts, scenario: q.scenario, options: q.options }));
      m.exercises.filter((e) => e.type === "A").forEach((e) => items.push({ id: "x-" + e.id, mod: m, concepts: e.concepts, scenario: e.problem, options: e.options }));
    });
    return items;
  }
  function weight(it) {
    const s = A.S.quiz[it.id];
    if (!s) return 2;
    if (s.last === 0) return 3.5;
    return 1 / (1 + s.ok);
  }
  function sample(items, n) {
    const bag = items.slice(), out = [];
    while (out.length < n && bag.length) {
      const total = bag.reduce((a, it) => a + weight(it), 0);
      let r = Math.random() * total, k = 0;
      for (; k < bag.length; k++) { r -= weight(bag[k]); if (r <= 0) break; }
      out.push(bag.splice(Math.min(k, bag.length - 1), 1)[0]);
    }
    return out;
  }

  let session = null;

  A.renderQuiz = (params) => {
    document.title = "¿Sé esto? · DataLab";
    session = null;
    const pre = params.get("m");
    const started = MODS.filter((m) => m.concepts.some((c) => A.S.skills[c.id]));
    let sel = new Set(pre ? [pre] : (started.length ? started : [MODS[0]]).map((m) => m.id));
    let count = 10;
    const stats = Object.values(A.S.quiz);
    const n = stats.reduce((a, s) => a + s.n, 0), ok = stats.reduce((a, s) => a + s.ok, 0);
    const weak = Object.keys(CON_BY).map((c) => ({ c: CON_BY[c], k: A.S.skills[c] })).filter(({ k }) => k && k.rec.n >= 1 && k.rec.ok / k.rec.n < 0.7).slice(0, 8);
    app().innerHTML = `<div class="page-enter">
      <div class="crumbs"><a href="#/">Ruta</a> / <span>¿Sé esto?</span></div>
      <div class="grid-2">
        <section class="panel pad">
          <span class="eyebrow">🎯 Modo reconocimiento</span>
          <h1 class="quiz-title">¿Sé esto?</h1>
          <p class="lead small">Problemas al azar. Para cada uno: <b>¿qué herramienta o concepto usarías?</b> No hace falta escribir código: el objetivo es comprobar que <b>reconocés la solución</b>. Los que fallaste vuelven con más frecuencia.</p>
          <h3 class="h-sec">Módulos</h3>
          <div class="filters" id="qMods">${MODS.map((m) => `<button class="fchip ${sel.has(m.id) ? "on" : ""}" data-m="${m.id}">${m.icon} ${m.num} ${esc(m.title)}</button>`).join("")}</div>
          <h3 class="h-sec">Cantidad</h3>
          <div class="filters" id="qCount">${[5, 10, 20].map((c) => `<button class="fchip ${c === count ? "on" : ""}" data-c="${c}">${c}</button>`).join("")}</div>
          <button class="btn primary" id="qStart" style="margin-top:14px">Empezar</button>
          <p class="muted small" style="margin-top:10px">Si no sabés, usá <b>"No lo sé"</b>: es mejor que adivinar, y el sistema te lo vuelve a preguntar.</p>
        </section>
        <section class="panel pad">
          <h3 class="h-sec">Tu reconocimiento</h3>
          <div class="hs-top">${A.ring(n ? ok / n : 0, 80)}<div><b>${ok}/${n}</b> respuestas correctas<p class="muted small">Sumando todas las sesiones.</p></div></div>
          ${weak.length ? `<h4>Conceptos que todavía no reconocés bien</h4><ul class="links">${weak.map(({ c }) => `<li><a href="#/c/${c.id}">${esc(c.title)}</a> <small class="muted">· ${esc(c.mod.title)}</small></li>`).join("")}</ul>` : '<p class="muted">Cuando respondas preguntas, acá vas a ver qué conceptos te cuesta reconocer.</p>'}
        </section>
      </div>
    </div>`;
    $$("#qMods .fchip").forEach((b) => b.addEventListener("click", () => {
      const id = b.dataset.m;
      if (sel.has(id)) { if (sel.size > 1) sel.delete(id); } else sel.add(id);
      $$("#qMods .fchip").forEach((x) => x.classList.toggle("on", sel.has(x.dataset.m)));
    }));
    $$("#qCount .fchip").forEach((b) => b.addEventListener("click", () => {
      count = +b.dataset.c;
      $$("#qCount .fchip").forEach((x) => x.classList.toggle("on", x === b));
    }));
    $("#qStart").addEventListener("click", () => {
      const pool = poolFor(MODS.filter((m) => sel.has(m.id)));
      start({ items: sample(pool, count), mode: "quiz", back: "#/quiz" });
    });
  };

  A.renderEval = (m) => {
    document.title = `Evaluación ${m.title} · DataLab`;
    const pool = poolFor([m]);
    start({ items: sample(pool, Math.min(10, pool.length)), mode: "eval", mod: m, back: `#/m/${m.id}/evaluacion` });
  };

  function start(s) {
    session = Object.assign(s, { i: 0, results: [], seed: Date.now() });
    question();
  }

  function question() {
    const s = session, it = s.items[s.i];
    app().innerHTML = `<div class="page-enter quiz-page">
      <div class="crumbs"><a href="${s.back}">${s.mode === "eval" ? `Evaluación · ${esc(s.mod.title)}` : "¿Sé esto?"}</a> / <span>${s.i + 1} de ${s.items.length}</span></div>
      <div class="qprog">${A.bar(s.i / s.items.length)}</div>
      <div class="panel pad qbig">
        <div class="q-meta"><span class="pill" style="--c:${it.mod.color}">${it.mod.icon} ${esc(it.mod.title)}</span></div>
        <div class="md scenario">${md(it.scenario)}</div>
        <p class="q-ask">¿Qué herramienta o concepto usarías?</p>
        <div id="qc"></div>
        <div id="qNext"></div>
      </div>
    </div>`;
    A.renderChoice($("#qc"), "", it.options, it.id + s.seed, (ok, first, idx) => {
      if (!first) return;
      const st = (A.S.quiz[it.id] = A.S.quiz[it.id] || { n: 0, ok: 0, last: null });
      st.n++; if (ok) st.ok++; st.last = ok ? 1 : 0; st.at = Date.now();
      A.ratio(it.concepts, "rec", ok);
      s.results.push({ it, ok, dk: idx < 0 });
      A.updateTop();
      const last = s.i === s.items.length - 1;
      $("#qNext").innerHTML = `<div class="q-foot"><span class="muted small">Conceptos: ${it.concepts.map((c) => `<a href="#/c/${c}">${esc(CON_BY[c].title)}</a>`).join(", ")}</span><button class="btn primary" id="qGo">${last ? "Ver resultado" : "Siguiente →"}</button></div>`;
      $("#qGo").addEventListener("click", () => { s.i++; if (last) results(); else question(); });
      $("#qGo").focus();
    }, false, { dontKnow: true, revealOnFail: true });
  }

  function results() {
    const s = session;
    const ok = s.results.filter((r) => r.ok).length, tot = s.results.length, score = tot ? ok / tot : 0;
    if (s.mode === "eval") {
      const prev = A.S.evals[s.mod.id];
      A.S.evals[s.mod.id] = { best: Math.max(score, prev ? prev.best : 0), last: score, at: Date.now() };
      A.save();
      if (score >= 0.8 && (!prev || prev.best < 0.8)) A.toast("🏅", "Evaluación aprobada", `${s.mod.title}: ${Math.round(score * 100)}%`);
    }
    const failed = s.results.filter((r) => !r.ok);
    const weakC = [...new Set(failed.flatMap((r) => r.it.concepts))];
    app().innerHTML = `<div class="page-enter">
      <div class="crumbs"><a href="${s.back}">${s.mode === "eval" ? `Evaluación · ${esc(s.mod.title)}` : "¿Sé esto?"}</a> / <span>Resultado</span></div>
      <div class="grid-2">
        <div class="panel pad">
          <div class="hs-top">${A.ring(score, 100)}<div><h2 style="margin:0">${ok} de ${tot}</h2><p class="muted">${score >= 0.8 ? "Reconocés bien estos problemas. 💪" : score >= 0.5 ? "Vas bien, pero hay conceptos para reforzar." : "Buen diagnóstico: ahora sabés qué repasar."}</p>
          ${s.mode === "eval" ? `<p class="small">${score >= 0.8 ? "✅ Evaluación aprobada (≥ 80%)." : "Para aprobar necesitás 80%."}</p>` : ""}</div></div>
          <div class="hero-cta">
            ${failed.length ? '<button class="btn primary" id="retry">Repetir los que fallé</button>' : ""}
            <a class="btn" href="${s.back}">Volver</a>
          </div>
        </div>
        <div class="panel pad">
          <h3 class="h-sec">Para repasar</h3>
          ${weakC.length ? `<ul class="links">${weakC.map((c) => `<li><a href="#/c/${c}">${esc(CON_BY[c].title)}</a> <small class="muted">· ${esc(CON_BY[c].mod.title)}</small></li>`).join("")}</ul>` : '<p class="muted">¡Nada! Probá con más preguntas o con otro módulo.</p>'}
        </div>
      </div>
      <div class="section-title"><h2>Detalle</h2></div>
      <div class="ex-list">${s.results.map((r) => `<div class="ex-row ${r.ok ? "done" : ""}"><span class="st">${r.ok ? "✓" : r.dk ? "?" : "✗"}</span><span class="t">${A.inline(r.it.scenario.split("\n")[0].slice(0, 140))}${r.it.scenario.length > 140 ? "…" : ""}</span><span class="muted small">${esc(r.it.options.find((o) => o.ok).t.replace(/`/g, ""))}</span></div>`).join("")}</div>
    </div>`;
    const rt = $("#retry");
    if (rt) rt.addEventListener("click", () => start({ items: failed.map((r) => r.it), mode: "quiz", back: s.back }));
  }
})();
