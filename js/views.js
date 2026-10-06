/* DataLab · vistas: inicio, módulo, concepto, método IA y progreso */
(() => {
  "use strict";
  const A = window.PQA;
  const { $, $$, esc, md, MODS, CON_BY, EX_BY } = A;
  const app = () => $("#app");

  const METHOD = [
    ["Concepto", "¿Qué problema resuelve y cuándo lo necesito?"],
    ["Problema", "Un caso real con datos."],
    ["Razonamiento", "¿Qué información necesito? ¿Qué operación?"],
    ["Estrategia", "Plan en pasos y herramientas."],
    ["Implementación", "Código propio o con IA como copiloto."],
    ["Verificación", "¿El resultado es correcto? ¿Y si cambian los datos?"],
  ];
  const PHASES = [
    ["1", "Pensar", "Explicás la solución con tus palabras."],
    ["2", "Planificar", "Elegís qué herramientas creés necesitar."],
    ["3", "Implementar", "Escribís el código (o pedís ayuda a una IA)."],
    ["4", "Comprender", "Si usaste IA, explicás qué hace el código."],
    ["5", "Verificar", "Lo ejecutás contra datos reales."],
    ["6", "Modificar", "Resolvés una variante: transferencia."],
  ];

  /* ================================================================== INICIO */
  A.renderHome = () => {
    document.title = "DataLab · Ciencia de Datos con método";
    const g = A.globalMastery();
    const next = A.nextGlobal();
    const allC = Object.keys(CON_BY);
    const dims = A.dimAggregate(allC);
    const py = MODS[0], pyM = A.modMastery(py);
    app().innerHTML = `<div class="page-enter">
      <section class="hero">
        <div class="hero-main">
          <span class="eyebrow">🧪 Laboratorio personal de Ciencia de Datos</span>
          <h1>Aprendé a <span class="hl">pensar con datos</span>, no a memorizar sintaxis</h1>
          <p class="lead">Python → Pandas → DataFrames → NumPy → Matplotlib → Seaborn → Machine Learning. En cada concepto: reconocé el problema, diseñá la estrategia, implementá (con IA como copiloto si hace falta), debuggeá y verificá.</p>
          <div class="method">${METHOD.map(([n, d], i) => `<span class="mstep" title="${esc(d)}"><b>${i + 1}</b>${esc(n)}</span>`).join('<span class="marrow">→</span>')}</div>
          <div class="hero-cta">
            ${next ? `<a class="btn primary" href="#/e/${next.id}">▶ ${A.S.created && Object.keys(A.S.ex).length ? "Continuar" : "Empezar por Python"} <span class="kbd">${esc(next.title)}</span></a>` : `<a class="btn primary" href="#/progreso">Ver mi progreso</a>`}
            <a class="btn" href="#/quiz">🎯 ¿Sé esto?</a>
            <a class="btn ghost" href="#/ia">🤖 Cómo estudiar con IA</a>
          </div>
        </div>
        <div class="hero-side panel">
          <div class="hs-top">${A.ring(g, 92)}<div><h3>Dominio global</h3><p class="muted small">No sube por completar ejercicios: sube cuando demostrás que podés <b>reconocer, resolver, debuggear, explicar y transferir</b>.</p></div></div>
          <div class="skillbars">${dims.map((d) => `<div class="sb" title="${esc(d.d)}"><span>${esc(d.n)}</span>${A.bar(d.v)}<em>${Math.round(d.v * 100)}%</em></div>`).join("")}</div>
          <div class="hs-foot"><span>🔥 <b>${A.streakNow()}</b> días de racha</span><span>Hoy: <b>${A.dayCount()}</b>/${A.GOAL}</span></div>
        </div>
      </section>

      <div class="section-title"><h2>Tu ruta</h2><span>Python es la base: no saltees el módulo 00</span></div>
      <div class="route">${MODS.map((m, i) => {
        const v = A.modMastery(m), done = A.modDone(m), tot = m.exercises.length;
        const warn = i > 0 && pyM < 0.3;
        const isNext = next && next.mod === m;
        return `<a class="route-item ${isNext ? "current" : ""}" href="#/m/${m.id}" style="--c:${m.color}">
          <div class="ri-num">${m.num}</div>
          <div class="ri-icon">${m.icon}</div>
          <div class="ri-body">
            <div class="ri-head"><h3>${esc(m.title)}</h3>${isNext ? '<span class="pill now">Estás acá</span>' : ""}${warn ? '<span class="pill warn" title="Te recomendamos dominar Python primero">Requiere Python</span>' : ""}</div>
            <p>${esc(m.desc)}</p>
            <div class="ri-foot">${A.bar(v, m.color)}<span>${Math.round(v * 100)}% dominio · ${done}/${tot} ejercicios · ${m.concepts.length} conceptos</span></div>
          </div>
        </a>`;
      }).join("")}</div>

      <div class="section-title"><h2>Cómo funciona un ejercicio de código</h2><span>La solución completa es siempre el último recurso</span></div>
      <div class="phases">${PHASES.map(([n, t, d]) => `<div class="phase"><div class="n">${n}</div><h4>${t}</h4><p>${d}</p></div>`).join("")}</div>

      <div class="section-title"><h2>Siete tipos de práctica</h2><span>Cada uno entrena una habilidad distinta</span></div>
      <div class="types-grid">${Object.keys(A.D.types).map((t) => `<div class="tcard t-${t}"><span class="ti">${A.TYPE_ICON[t]}</span><b>${esc(A.D.types[t])}</b><small>${esc(A.TYPE_HINT[t])}</small></div>`).join("")}</div>

      <footer class="foot">
        <span>🧪 DataLab (PandasQuest) · Python, Pandas, NumPy, Matplotlib, Seaborn y Machine Learning en el navegador</span>
        <span><a href="https://github.com/rosalesluciano/pandas-quest" target="_blank" rel="noopener">GitHub</a> · <a href="#/progreso">Progreso y copia de seguridad</a></span>
      </footer>
    </div>`;
  };

  /* ================================================================== MÓDULO */
  const TABS = [["inicio", "Inicio"], ["conceptos", "Conceptos"], ["practica", "Práctica"], ["proyecto", "Proyecto"], ["evaluacion", "Evaluación"], ["repaso", "Repaso"]];
  let pracFilter = "all";

  A.renderModule = (m, tab = "inicio") => {
    if (!TABS.some(([k]) => k === tab)) tab = "inicio";
    document.title = `${m.num} ${m.title} · DataLab`;
    const v = A.modMastery(m), next = A.nextFor(m);
    const i = m.mi;
    app().innerHTML = `<div class="page-enter">
      <div class="crumbs"><a href="#/">Ruta</a> / <span>Módulo ${m.num}</span></div>
      <div class="mod-hero" style="--c:${m.color}">
        <div class="mod-icon">${m.icon}</div>
        <div class="grow"><div class="mod-num">Módulo ${m.num}</div><h1>${esc(m.title)}</h1><p>${esc(m.desc)}</p></div>
        <div class="mh-side">${A.ring(v, 74)}<small>dominio</small></div>
      </div>
      <div class="mh-actions">
        ${next ? `<a class="btn primary" href="#/e/${next.id}">▶ ${A.modDone(m) ? "Continuar" : "Empezar"} <span class="kbd">${esc(next.title)}</span></a>` : `<a class="btn primary" href="#/eval/${m.id}">Hacer la evaluación</a>`}
        <a class="btn" href="#/quiz?m=${m.id}">🎯 ¿Sé esto? de este módulo</a>
        <a class="btn ghost" href="${m.colab}" target="_blank" rel="noopener">Abrir en Colab ↗</a>
      </div>
      <nav class="mtabs" role="tablist">${TABS.map(([k, n]) => `<a role="tab" class="${k === tab ? "on" : ""}" href="#/m/${m.id}/${k}">${n}</a>`).join("")}</nav>
      <div id="tabBody"></div>
      <div class="ex-nav" style="margin-top:28px">
        ${i > 0 ? `<a class="btn ghost" href="#/m/${MODS[i - 1].id}">← ${MODS[i - 1].num} ${esc(MODS[i - 1].title)}</a>` : "<span></span>"}
        ${i < MODS.length - 1 ? `<a class="btn ghost" href="#/m/${MODS[i + 1].id}">${MODS[i + 1].num} ${esc(MODS[i + 1].title)} →</a>` : ""}
      </div>
    </div>`;
    const body = $("#tabBody");
    ({ inicio: tabInicio, conceptos: tabConceptos, practica: tabPractica, proyecto: tabProyecto, evaluacion: tabEvaluacion, repaso: tabRepaso })[tab](m, body);
    // Python primero
    if (m.mi > 0 && A.modMastery(MODS[0]) < 0.3 && !A.S.gateOk[m.id]) {
      A.modal(`<span class="big-emoji">🐍</span><h2>Python es la base</h2>
        <p>Este módulo usa funciones, diccionarios, comprensiones y manejo de errores todo el tiempo. Con el módulo 00 vas a poder <b>leer y modificar</b> el código que te dé una IA en lugar de copiarlo.</p>
        <div class="hero-cta center"><a class="btn primary" href="#/m/m00" data-close>Ir a Python</a><button class="btn" id="gateGo">Ya sé Python, seguir</button></div>`,
      "center", (card) => $("#gateGo", card).addEventListener("click", () => { A.S.gateOk[m.id] = true; A.save(); A.closeModal(); }));
    }
  };

  function sectionsOf(m) {
    const secs = [];
    m.exercises.forEach((e) => { let s = secs[secs.length - 1]; if (!s || s.name !== e.sec) secs.push((s = { name: e.sec, items: [] })); s.items.push(e); });
    return secs;
  }

  function tabInicio(m, body) {
    const secs = sectionsOf(m);
    body.innerHTML = `<div class="grid-2">
      <div class="panel pad">
        <h3 class="h-sec">🎯 Qué vas a aprender</h3>
        <ul class="checks">${m.learn.map((l) => `<li>${A.inline(l)}</li>`).join("")}</ul>
        <h3 class="h-sec">💡 Por qué importa</h3>
        <div class="md">${md(m.why)}</div>
        <h3 class="h-sec">🤖 Cómo usar la IA en este módulo</h3>
        <div class="callout ai">${md(m.ai)}</div>
      </div>
      <div class="panel pad">
        <h3 class="h-sec">🧭 Ruta sugerida</h3>
        <ol class="secs">${secs.map((s) => {
          const d = s.items.filter((e) => A.peekEx(e.id).status === "done").length;
          const first = s.items.find((e) => A.peekEx(e.id).status !== "done") || s.items[0];
          return `<li><a href="#/e/${first.id}"><span class="sn">${esc(s.name)}</span><span class="sc">${d}/${s.items.length}</span></a>${A.bar(d / s.items.length, m.color)}</li>`;
        }).join("")}</ol>
      </div>
    </div>
    <div class="section-title"><h2>Tu dominio por concepto</h2><span>Pasá el mouse sobre cada indicador para ver qué significa</span></div>
    <div class="matrix panel">${matrix(m)}</div>`;
  }

  function matrix(m) {
    return `<div class="mx-row mx-head"><span class="mx-c">Concepto</span>${A.DIMS.map((d) => `<span class="mx-d" title="${esc(d.d)}">${esc(d.n)}</span>`).join("")}<span class="mx-v">Nivel</span></div>
      ${m.concepts.map((c) => {
        const v = A.mastery(c.id), [lab, cls] = A.masteryLabel(v);
        return `<a class="mx-row" href="#/c/${c.id}"><span class="mx-c">${esc(c.title)}</span>${A.DIMS.map((d) => {
          const x = A.dimValue(c.id, d.k);
          return `<span class="mx-d"><i class="dot ${x === null ? "na" : x >= 1 ? "on" : x > 0 ? "half" : "off"}" title="${esc(d.n)}${x === null ? " (no aplica)" : ""}"></i></span>`;
        }).join("")}<span class="mx-v"><span class="mlabel ${cls}">${lab}</span></span></a>`;
      }).join("")}`;
  }

  function tabConceptos(m, body) {
    body.innerHTML = `<p class="muted">Cada ficha responde: qué problema resuelve, cuándo lo necesitás, cómo reconocerlo, qué podés y qué NO podés hacer, qué no hace falta memorizar y cómo pedírselo a una IA.</p>
      <div class="cgrid">${m.concepts.map((c) => {
        const v = A.mastery(c.id), [lab, cls] = A.masteryLabel(v);
        return `<a class="ccard" href="#/c/${c.id}" style="--c:${m.color}">
          <div class="cc-top"><h3>${esc(c.title)}</h3><span class="mlabel ${cls}">${lab}</span></div>
          <code class="tool">${esc(c.tool)}</code>
          <p>${A.inline(c.problem)}</p>
          ${A.bar(v, m.color)}
        </a>`;
      }).join("")}</div>`;
  }

  function tabPractica(m, body) {
    const counts = {};
    m.exercises.forEach((e) => (counts[e.type] = (counts[e.type] || 0) + 1));
    const filters = [["all", "Todo", m.exercises.length]].concat(Object.keys(A.D.types).filter((t) => counts[t]).map((t) => [t, `${A.TYPE_ICON[t]} ${A.D.types[t]}`, counts[t]]));
    if (!filters.some(([k]) => k === pracFilter)) pracFilter = "all";
    const draw = () => {
      const secs = sectionsOf(m);
      $("#exList", body).innerHTML = secs.map((s) => {
        const items = s.items.filter((e) => pracFilter === "all" || e.type === pracFilter);
        if (!items.length) return "";
        return `<h3 class="sec-title">${esc(s.name)}</h3>${items.map((e) => {
          const st = A.peekEx(e.id).status;
          return `<a class="ex-row ${st}" href="#/e/${e.id}">
            <span class="st">${A.statusIcon(e.id) || e.ei + 1}</span>
            <span class="t">${esc(e.title)}</span>
            ${A.typeBadge(e.type)}${A.levelBadge(e.level)}
          </a>`;
        }).join("")}`;
      }).join("");
      $$(".fchip", body).forEach((b) => b.classList.toggle("on", b.dataset.f === pracFilter));
    };
    body.innerHTML = `<div class="filters">${filters.map(([k, n, c]) => `<button class="fchip" data-f="${k}">${n} <small>${c}</small></button>`).join("")}</div>
      <p class="muted small">La ruta mezcla tipos a propósito: reconocer → razonar → planificar → implementar → debuggear → transferir. Filtrá si querés repasar una habilidad puntual (por ejemplo, solo Debugging).</p>
      <div class="ex-list" id="exList"></div>`;
    $$(".fchip", body).forEach((b) => b.addEventListener("click", () => { pracFilter = b.dataset.f; draw(); }));
    draw();
  }

  function tabProyecto(m, body) {
    const p = m.project;
    const allIds = p.phases.flatMap((ph) => ph.ids);
    const done = allIds.filter((id) => A.peekEx(id).status === "done").length;
    body.innerHTML = `<div class="grid-2">
      <div class="panel pad">
        <span class="eyebrow">🏗️ Proyecto integrador</span>
        <h2 class="proj-title">${esc(p.title)}</h2>
        <div class="md">${md(p.story)}</div>
        <div class="callout tip"><b>Objetivo:</b> ${A.inline(p.goal)}</div>
        <h3 class="h-sec">Fases</h3>
        <ol class="phase-list">${p.phases.map((ph) => `<li>
          <div class="pl-head"><b>${esc(ph.name)}</b><span class="muted small">${A.inline(ph.desc)}</span></div>
          ${ph.ids.map((id) => { const e = EX_BY[id]; return `<a class="ex-row mini ${A.peekEx(id).status}" href="#/e/${id}"><span class="st">${A.statusIcon(id) || "·"}</span><span class="t">${esc(e.title)}</span>${A.typeBadge(e.type)}</a>`; }).join("")}
        </li>`).join("")}</ol>
      </div>
      <div class="panel pad">
        <div class="hs-top">${A.ring(done / allIds.length, 70, `${done}/${allIds.length}`)}<div><h3>Avance del proyecto</h3><p class="muted small">El proyecto integra los conceptos del módulo (y de los anteriores).</p></div></div>
        <h3 class="h-sec">📦 Entregables</h3>
        <ul class="checks">${p.deliverable.map((d) => `<li>${A.inline(d)}</li>`).join("")}</ul>
        <h3 class="h-sec">🤖 Reglas de uso de IA</h3>
        <ul class="rules">${p.ai_rules.map((r) => `<li>${A.inline(r)}</li>`).join("")}</ul>
      </div>
    </div>`;
  }

  function tabEvaluacion(m, body) {
    const ev = A.S.evals[m.id];
    const weak = m.concepts.map((c) => ({ c, k: A.S.skills[c.id] })).filter(({ k }) => k && k.rec.n && k.rec.ok / k.rec.n < 0.7);
    body.innerHTML = `<div class="grid-2">
      <div class="panel pad">
        <h3 class="h-sec">📝 Evaluación de reconocimiento</h3>
        <p>Problemas al azar del módulo: para cada uno, elegí qué herramienta o concepto usarías. Mide si <b>reconocés</b> la solución, que es la base de tu método. Aprobás con <b>80%</b>.</p>
        <p class="muted small">La evaluación no reemplaza a la práctica: un 100% acá con poca práctica de código sigue siendo "reconocer", no "resolver".</p>
        <a class="btn primary" href="#/eval/${m.id}">Empezar evaluación</a>
      </div>
      <div class="panel pad">
        <h3 class="h-sec">Resultados</h3>
        ${ev ? `<div class="hs-top">${A.ring(ev.best, 70)}<div><b>Mejor resultado: ${Math.round(ev.best * 100)}%</b><p class="muted small">Último: ${Math.round(ev.last * 100)}% · ${ev.best >= 0.8 ? "✅ Aprobada" : "Todavía no alcanza el 80%"}</p></div></div>` : '<p class="muted">Todavía no hiciste la evaluación de este módulo.</p>'}
        ${weak.length ? `<h4>Conceptos para reforzar</h4><ul class="links">${weak.map(({ c }) => `<li><a href="#/c/${c.id}">${esc(c.title)}</a></li>`).join("")}</ul>` : ""}
      </div>
    </div>`;
  }

  function tabRepaso(m, body) {
    const sorted = m.concepts.slice().sort((a, b) => A.mastery(a.id) - A.mastery(b.id));
    body.innerHTML = `<div class="panel pad">
      <h3 class="h-sec">🗂️ Chuleta: qué hacer → con qué herramienta → por qué → cómo verificarlo</h3>
      <p class="muted small">La sintaxis exacta la consultás (documentación o IA). Lo que tenés que poder hacer de memoria es la primera columna: reconocer la señal.</p>
      <div class="md-table cheat"><table><thead><tr><th>Si ves…</th><th>Concepto / herramienta</th><th>Por qué</th><th>Cómo verificarlo</th></tr></thead><tbody>
      ${m.concepts.map((c) => `<tr><td><ul>${c.signals.map((s) => `<li>${A.inline(s)}</li>`).join("")}</ul></td><td><a href="#/c/${c.id}"><b>${esc(c.title)}</b></a><br><code>${esc(c.tool)}</code></td><td>${A.inline(c.problem)}</td><td>${A.inline(c.verify)}</td></tr>`).join("")}
      </tbody></table></div>
    </div>
    <div class="section-title"><h2>Repasar primero</h2><span>Los conceptos con menor dominio</span></div>
    <div class="cgrid">${sorted.slice(0, 4).map((c) => { const [lab, cls] = A.masteryLabel(A.mastery(c.id)); return `<a class="ccard" href="#/c/${c.id}" style="--c:${m.color}"><div class="cc-top"><h3>${esc(c.title)}</h3><span class="mlabel ${cls}">${lab}</span></div><p class="small">${A.inline(c.nomemo)}</p></a>`; }).join("")}</div>`;
  }

  /* ================================================================== CONCEPTO */
  A.renderConcept = (c) => {
    const m = c.mod;
    document.title = `${c.title} · DataLab`;
    A.markSeen([c.id]);
    const exs = A.EX.filter((e) => e.concepts.includes(c.id));
    const prev = m.concepts[c.ci - 1], next = m.concepts[c.ci + 1];
    const k = A.S.skills[c.id];
    const answered = k && k.comp.ok > 0;
    app().innerHTML = `<div class="page-enter concept-page">
      <div class="crumbs"><a href="#/">Ruta</a> / <a href="#/m/${m.id}/conceptos">${m.icon} ${esc(m.title)}</a> / <span>Concepto</span></div>
      <div class="c-hero" style="--c:${m.color}">
        <div class="grow"><h1>${esc(c.title)}</h1><code class="tool big">${esc(c.tool)}</code></div>
        <div class="mh-side">${A.ring(A.mastery(c.id), 70)}<small>${A.masteryLabel(A.mastery(c.id))[0]}</small></div>
      </div>
      ${A.dimPills(c.id)}
      <div class="grid-2 c-grid">
        <section class="panel pad"><h3 class="h-sec">🧩 ¿Qué problema resuelve?</h3><div class="md">${md(c.problem)}</div>
          <h3 class="h-sec">⏰ ¿Cuándo lo necesito?</h3><div class="md">${md(c.when)}</div>
          <h3 class="h-sec">🔎 ¿Cómo reconozco que lo necesito?</h3><ul class="signals">${c.signals.map((s) => `<li>${A.inline(s)}</li>`).join("")}</ul></section>
        <section class="panel pad"><div class="cando"><div><h3 class="h-sec ok">✅ Qué puedo hacer</h3><ul>${c.can.map((s) => `<li>${A.inline(s)}</li>`).join("")}</ul></div>
          <div><h3 class="h-sec no">⛔ Qué NO puedo hacer (límites)</h3><ul>${c.cant.map((s) => `<li>${A.inline(s)}</li>`).join("")}</ul></div></div>
          <h3 class="h-sec">🧠 Qué NO necesito memorizar</h3><div class="callout tip">${md(c.nomemo)}</div></section>
        <section class="panel pad"><h3 class="h-sec">🤖 Cómo pedírselo a una IA</h3>
          <div class="prompt-box"><p>${esc(c.ai)}</p><button class="btn small" id="copyPrompt">Copiar prompt</button></div>
          <p class="muted small">Fijate que el prompt pide <b>explicación antes que código</b> y da contexto. Eso te deja entender y verificar lo que recibas.</p>
          <h3 class="h-sec">✔️ Cómo verifico que funciona</h3><div class="md">${md(c.verify)}</div></section>
        <section class="panel pad"><h3 class="h-sec">🧪 Ejemplo de referencia</h3>
          <details class="reveal"><summary>Ver ejemplo (con otros datos)</summary>${A.codeBlock(c.example, "python")}</details>
          <h3 class="h-sec">❓ Comprobá que lo entendiste</h3>
          <div class="qcard" id="cCheck"></div></section>
      </div>
      <div class="section-title"><h2>Practicá este concepto</h2><span>${exs.length} ejercicios</span></div>
      <div class="ex-list">${exs.map((e) => `<a class="ex-row ${A.peekEx(e.id).status}" href="#/e/${e.id}"><span class="st">${A.statusIcon(e.id) || "·"}</span><span class="t">${esc(e.title)} <small class="muted">· ${esc(e.mod.title)}</small></span>${A.typeBadge(e.type)}${A.levelBadge(e.level)}</a>`).join("")}</div>
      <div class="ex-nav" style="margin-top:24px">
        ${prev ? `<a class="btn ghost" href="#/c/${prev.id}">← ${esc(prev.title)}</a>` : "<span></span>"}
        ${next ? `<a class="btn ghost" href="#/c/${next.id}">${esc(next.title)} →</a>` : `<a class="btn ghost" href="#/m/${m.id}/practica">Ir a la práctica →</a>`}
      </div>
    </div>`;
    $("#copyPrompt").addEventListener("click", (ev) => A.copy(c.ai, ev.currentTarget));
    A.renderChoice($("#cCheck"), c.check.q, c.check.options, "c-" + c.id, (ok, first) => {
      if (first) A.ratio([c.id], "comp", ok);
      A.updateTop();
    }, answered);
  };

  // pregunta de opción múltiple reutilizable. onAnswer(ok, primerIntento)
  A.renderChoice = (el, q, options, seed, onAnswer, alreadyOk = false, opts = {}) => {
    const order = A.shuffled(options, seed);
    let first = !alreadyOk;
    el.innerHTML = `${q ? `<p class="q">${A.inline(q)}</p>` : ""}<div class="opts">${order.map(([o, i]) => `<button class="opt" data-i="${i}">${A.inline(o.t)}</button>`).join("")}</div>${opts.dontKnow ? '<button class="btn small ghost dk">No lo sé</button>' : ""}<div class="fb"></div>`;
    const fb = $(".fb", el);
    const answer = (i) => {
      const o = i < 0 ? null : options[i];
      const ok = !!(o && o.ok);
      const good = options.find((x) => x.ok);
      $$(".opt", el).forEach((b) => {
        const oi = +b.dataset.i;
        b.classList.toggle("right", options[oi].ok && (ok || opts.revealOnFail));
        if (oi === i) b.classList.add(ok ? "right" : "wrong");
        if (ok || opts.revealOnFail) b.disabled = true;
      });
      fb.innerHTML = ok
        ? `<div class="verdict ok small"><b>✓ Correcto.</b> ${A.inline(o.why || "")}</div>`
        : i < 0
          ? `<div class="verdict info small"><b>Bien por la honestidad.</b> Era: <b>${A.inline(good.t)}</b>. ${A.inline(good.why || "")}</div>`
          : `<div class="verdict bad small"><b>✗ No.</b> ${A.inline(o.why || "")}${opts.revealOnFail ? `<br>Correcta: <b>${A.inline(good.t)}</b>. ${A.inline(good.why || "")}` : " Probá de nuevo."}</div>`;
      if (i < 0) $$(".opt", el).forEach((b) => (b.disabled = true));
      const dk = $(".dk", el); if (dk) dk.remove();
      onAnswer(ok, first, i);
      first = false;
    };
    $$(".opt", el).forEach((b) => b.addEventListener("click", () => answer(+b.dataset.i)));
    const dk = $(".dk", el); if (dk) dk.addEventListener("click", () => answer(-1));
    if (alreadyOk) {
      const gi = options.findIndex((o) => o.ok);
      $$(".opt", el).forEach((b) => { b.disabled = true; if (+b.dataset.i === gi) b.classList.add("right"); });
      fb.innerHTML = `<div class="verdict ok small"><b>✓ Ya respondiste bien.</b> ${A.inline(options[gi].why || "")}</div>`;
    }
  };

  /* ================================================================== MÉTODO IA */
  const PROMPTS = [
    ["1 · Pista", "Estoy resolviendo este problema: [problema]. Mi idea es [tu plan]. No me des la solución ni código: dame solo una pista sobre qué debería pensar a continuación."],
    ["2 · Concepto", "No entiendo cuándo usar [concepto, ej. groupby]. Explicámelo con un ejemplo de datos distinto al de mi ejercicio, sin resolver mi ejercicio."],
    ["3 · Revisión de mi código", "Este es mi código: [código]. Esperaba [resultado esperado] y obtengo [resultado]. No lo reescribas: decime en qué línea está el problema y por qué, para que lo corrija yo."],
    ["4 · Código (último recurso)", "Problema: [problema]. Mi plan: [pasos]. Escribí el código siguiendo MI plan, con comentarios en cada paso, y explicá qué devuelve cada línea. Después haceme 3 preguntas para comprobar que lo entendí."],
    ["5 · Explicar código ajeno", "Explicame línea por línea este código: [código]. Para cada línea decime qué entra, qué sale y qué tipo de objeto devuelve. ¿Qué pasaría si cambian los datos o falta una columna?"],
    ["6 · Debug sin solución", "Me aparece este error: [traceback]. Explicame qué significa y qué debería inspeccionar (qué imprimir) para encontrar la causa. No me des el código corregido."],
  ];
  A.PROMPTS = PROMPTS;
  A.renderIA = () => {
    document.title = "Cómo estudiar con IA · DataLab";
    const STEPS = ["Intentá resolverlo.", "Pensá la estrategia.", "Escribí pseudocódigo.", "Si te trabás, pedile una **pista** a la IA.", "Si seguís trabado, pedile que **explique el concepto**.", "Recién después pedile **código**.", "Leé y entendé el código.", "Ejecutalo.", "Modificalo.", "Volvé a resolver un problema parecido **sin IA**."];
    const CHECK = ["Puedo explicar qué hace cada línea.", "Sé qué tipo de objeto devuelve cada paso (Series, DataFrame, número, array…).", "Lo ejecuté con los datos reales y verifiqué el resultado contra un cálculo conocido.", "Probé qué pasa si cambian los datos (columna faltante, vacío, valores raros).", "Puedo modificarlo para una variante del problema.", "Podría reescribirlo sin IA (aunque tenga que consultar la sintaxis)."];
    const FLAGS = ["Copiás el enunciado completo y pegás la respuesta sin leerla.", "No sabrías explicar por qué funciona.", "Ante un error, volvés a pedirle a la IA en lugar de leer el traceback.", "No podés resolver una variante sencilla sin ayuda.", "Aceptás un resultado sin verificarlo."];
    app().innerHTML = `<div class="page-enter">
      <div class="crumbs"><a href="#/">Ruta</a> / <span>Método</span></div>
      <section class="ia-hero panel pad">
        <span class="eyebrow">🤖 Regla de oro</span>
        <h1>La IA es tu copiloto, no tu muleta</h1>
        <p class="lead">El objetivo no es escribir Python de memoria: es poder <b>pensar → diseñar → orquestar → implementar con IA → debuggear → validar</b>. Para eso, la IA tiene que acelerar tu razonamiento, no reemplazarlo.</p>
      </section>
      <div class="grid-2">
        <div class="panel pad no-yes no"><h3>❌ NO</h3><p class="big-q">«Hacé este ejercicio.»</p><p class="muted">Obtenés una respuesta, pero no aprendés a reconocer el problema la próxima vez. Y si la IA se equivoca, no lo vas a notar.</p></div>
        <div class="panel pad no-yes yes"><h3>✅ SÍ</h3><p class="big-q">«Mi plan es X. ¿Qué me falta pensar?»</p><p class="muted">Vos ponés el razonamiento; la IA acelera la sintaxis, explica conceptos y revisa. Vos verificás.</p></div>
      </div>
      <div class="section-title"><h2>Los 10 pasos</h2><span>El orden importa</span></div>
      <ol class="ten">${STEPS.map((s, i) => `<li class="${i < 3 ? "self" : i < 6 ? "ask" : "own"}"><span class="n">${i + 1}</span><span>${A.inline(s)}</span></li>`).join("")}</ol>
      <div class="legend-row"><span class="lg self">Vos solo</span><span class="lg ask">Ayuda progresiva</span><span class="lg own">Apropiarte del código</span></div>
      <div class="section-title"><h2>Escalera de prompts</h2><span>Usá el escalón más bajo que te destrabe</span></div>
      <div class="prompts">${PROMPTS.map(([t, p], i) => `<div class="panel pad prompt-card"><h4>${esc(t)}</h4><p>${esc(p)}</p><button class="btn small" data-p="${i}">Copiar</button></div>`).join("")}</div>
      <div class="grid-2">
        <div class="panel pad"><h3 class="h-sec">✔️ Antes de aceptar código de una IA</h3><ul class="checks">${CHECK.map((c) => `<li>${A.inline(c)}</li>`).join("")}</ul></div>
        <div class="panel pad"><h3 class="h-sec">🚩 Señales de dependencia</h3><ul class="rules">${FLAGS.map((c) => `<li>${A.inline(c)}</li>`).join("")}</ul></div>
      </div>
      <div class="section-title"><h2>Cómo lo aplica esta plataforma</h2></div>
      <div class="phases">${PHASES.map(([n, t, d]) => `<div class="phase"><div class="n">${n}</div><h4>${t}</h4><p>${d}</p></div>`).join("")}</div>
      <div class="panel pad" style="margin-top:16px"><ul class="rules plain">
        <li>En los ejercicios de código no podés escribir hasta haber explicado tu idea y elegido herramientas.</li>
        <li>El botón <b>🤖 Pedir ayuda</b> arma prompts con tu problema y tu plan, ordenados de menor a mayor ayuda.</li>
        <li>Si marcás que usaste IA para el código, tenés que explicarlo antes de que cuente como resuelto.</li>
        <li>La escalera de pistas muestra la solución completa solo al final, y primero como idea y pseudocódigo.</li>
        <li>Los ejercicios <b>IA copiloto</b> te dan código generado por una IA para que practiques leerlo críticamente (a veces tiene errores sutiles).</li>
      </ul></div>
    </div>`;
    $$("[data-p]").forEach((b) => b.addEventListener("click", () => A.copy(PROMPTS[+b.dataset.p][1], b)));
  };

  /* ================================================================== PROGRESO */
  A.renderProgress = () => {
    document.title = "Progreso · DataLab";
    const all = Object.keys(CON_BY);
    const dims = A.dimAggregate(all);
    const byType = {};
    A.EX.forEach((e) => { const t = (byType[e.type] = byType[e.type] || { done: 0, tot: 0 }); t.tot++; if (A.peekEx(e.id).status === "done") t.done++; });
    const journal = [];
    Object.entries(A.S.ex).forEach(([id, st]) => {
      const e = EX_BY[id]; if (!e) return;
      const add = (label, text) => { if (text && text.trim()) journal.push({ e, label, text, at: st.at || 0 }); };
      add("Mi plan", st.plan && st.plan.text);
      add("Mi razonamiento", st.text);
      add("Por qué fallaba", st.why);
      add("Explicación del código de IA", st.reflection);
    });
    journal.sort((a, b) => b.at - a.at);
    app().innerHTML = `<div class="page-enter">
      <div class="crumbs"><a href="#/">Ruta</a> / <span>Progreso</span></div>
      <div class="grid-2">
        <div class="panel pad"><div class="hs-top">${A.ring(A.globalMastery(), 96)}<div><h2 style="margin:0">Tu dominio</h2><p class="muted small">Completar no es dominar. Cada concepto tiene hasta 8 indicadores; solo cuentan los que aplican a ese concepto.</p></div></div>
          <div class="skillbars">${dims.map((d) => `<div class="sb" title="${esc(d.d)}"><span>${esc(d.n)}</span>${A.bar(d.v)}<em>${Math.round(d.v * 100)}%</em></div>`).join("")}</div></div>
        <div class="panel pad"><h3 class="h-sec">Práctica por tipo</h3>
          <div class="skillbars">${Object.keys(A.D.types).map((t) => { const x = byType[t] || { done: 0, tot: 0 }; return `<div class="sb"><span>${A.TYPE_ICON[t]} ${esc(A.D.types[t])}</span>${A.bar(x.tot ? x.done / x.tot : 0)}<em>${x.done}/${x.tot}</em></div>`; }).join("")}</div>
          <p class="small muted">🔥 Racha: <b>${A.streakNow()}</b> días · Hoy: <b>${A.dayCount()}</b> ejercicios</p></div>
      </div>
      ${MODS.map((m) => `<div class="section-title"><h2>${m.icon} ${m.num} · ${esc(m.title)}</h2><span>${Math.round(A.modMastery(m) * 100)}% · evaluación: ${A.S.evals[m.id] ? Math.round(A.S.evals[m.id].best * 100) + "%" : "—"}</span></div><div class="matrix panel">${matrix(m)}</div>`).join("")}
      <div class="section-title"><h2>📓 Diario de razonamiento</h2><span>Lo que escribiste con tus palabras: releelo para repasar</span></div>
      <div class="journal">${journal.length ? journal.slice(0, 30).map((j) => `<div class="panel pad jitem"><div class="jh"><a href="#/e/${j.e.id}"><b>${esc(j.e.title)}</b></a><span class="muted small">${esc(j.label)} · ${esc(j.e.mod.title)}</span></div><p>${esc(j.text)}</p></div>`).join("") : '<p class="muted">Todavía no escribiste explicaciones. Aparecen acá a medida que resolvés ejercicios.</p>'}</div>
      <div class="section-title"><h2>Copia de seguridad</h2><span>El progreso se guarda en este navegador</span></div>
      <div class="panel pad backup">
        <button class="btn" id="expBtn">⬇️ Exportar progreso</button>
        <label class="btn" for="impFile">⬆️ Importar progreso</label><input type="file" id="impFile" accept="application/json" hidden>
        <button class="btn ghost danger" id="resetBtn">Reiniciar todo</button>
      </div>
    </div>`;
    $("#expBtn").addEventListener("click", () => {
      const blob = new Blob([JSON.stringify(A.S, null, 1)], { type: "application/json" });
      const a = document.createElement("a");
      a.href = URL.createObjectURL(blob);
      a.download = `datalab-progreso-${new Date().toISOString().slice(0, 10)}.json`;
      a.click();
      setTimeout(() => URL.revokeObjectURL(a.href), 1000);
    });
    $("#impFile").addEventListener("change", async (ev) => {
      const f = ev.target.files[0]; if (!f) return;
      try {
        const data = JSON.parse(await f.text());
        if (!data || data.v !== 3 || typeof data.ex !== "object") throw new Error("formato");
        A.S = Object.assign(A.S, data); A.save(); A.updateTop(); A.renderProgress(); A.toast("✅", "Progreso importado");
      } catch (e) { A.toast("⚠️", "Archivo inválido", "Tiene que ser una exportación de DataLab"); }
    });
    $("#resetBtn").addEventListener("click", () => {
      if (confirm("¿Seguro? Se borra todo tu progreso, planes y explicaciones de este navegador.")) { A.resetState(); A.updateTop(); A.renderProgress(); }
    });
  };
})();
