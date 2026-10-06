/* DataLab · núcleo: utilidades, estado, dominio por concepto, Python y UI común */
(() => {
  "use strict";
  const A = (window.PQA = window.PQA || {});
  const D = window.PQ;
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => Array.from(el.querySelectorAll(s));
  Object.assign(A, { D, $, $$ });

  /* ------------------------------------------------------------------ índices */
  const MODS = D.modules;
  const EX = [], EX_BY = {}, CON_BY = {}, Q_BY = {};
  MODS.forEach((m, mi) => {
    m.mi = mi;
    m.concepts.forEach((c, ci) => { c.mod = m; c.ci = ci; CON_BY[c.id] = c; });
    m.exercises.forEach((e, ei) => { e.mod = m; e.ei = ei; EX.push(e); EX_BY[e.id] = e; });
    m.quiz.forEach((q) => { q.mod = m; Q_BY[q.id] = q; });
  });
  // qué tipos de evidencia existen para cada concepto (para saber qué indicadores aplican)
  const KIND_OF = { A: "rec", B: "exp", C: "exp", D: "res", E: "dbg", F: "comp", G: "trf" };
  const APPLIES = {};
  Object.keys(CON_BY).forEach((id) => (APPLIES[id] = new Set(["known", "prac", "comp"])));
  EX.forEach((e) => e.concepts.forEach((c) => {
    const s = APPLIES[c];
    s.add(KIND_OF[e.type]);
    if (e.type === "F" || e.type === "B" || e.type === "C") s.add("exp");
    if (e.type === "D" || e.type === "G") s.add("rec"); // elegir herramientas en el plan
  }));
  MODS.forEach((m) => m.quiz.forEach((q) => q.concepts.forEach((c) => APPLIES[c].add("rec"))));
  Object.assign(A, { MODS, EX, EX_BY, CON_BY, Q_BY, APPLIES });

  A.DIMS = [
    { k: "known", n: "Conocido", d: "Abriste la ficha del concepto o un ejercicio que lo usa." },
    { k: "prac", n: "Practicado", d: "Hiciste al menos un intento con este concepto." },
    { k: "comp", n: "Comprendido", d: "Respondiste bien la pregunta de la ficha o explicaste código de IA." },
    { k: "rec", n: "Reconocer", d: "Identificás cuándo usarlo (reconocimiento, ¿Sé esto?, elegir herramientas)." },
    { k: "res", n: "Resolver", d: "Lo implementaste en un ejercicio de código sin ver la solución." },
    { k: "dbg", n: "Debuggear", d: "Encontraste y corregiste un error relacionado." },
    { k: "exp", n: "Explicar", d: "Explicaste con tus palabras (razonamiento, plan, comprensión)." },
    { k: "trf", n: "Transferir", d: "Resolviste una variante nueva del problema." },
  ];
  A.TYPE_ICON = { A: "🎯", B: "💭", C: "🧭", D: "⌨️", E: "🐞", F: "🤖", G: "🔁" };
  A.TYPE_HINT = {
    A: "Elegí la herramienta o el concepto adecuado.",
    B: "Explicá con tus palabras cómo lo resolverías. Sin código.",
    C: "Completá el plan de solución antes de programar.",
    D: "Pensá → planificá → implementá → verificá.",
    E: "Detectá el error, explicá por qué ocurre y corregilo.",
    F: "Leé el código que dio una IA y demostrá que lo entendés.",
    G: "Cambió una condición: adaptá lo que ya sabés.",
  };

  /* ------------------------------------------------------------------ texto */
  const esc = (s) => String(s == null ? "" : s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  function inline(raw) {
    return String(raw).split("`").map((seg, i) => (i % 2
      ? `<code>${esc(seg)}</code>`
      : esc(seg).replace(/\*\*(.+?)\*\*/g, "<b>$1</b>").replace(/(^|[^*])\*([^*\s](?:[^*]*[^*\s])?)\*/g, "$1<i>$2</i>"))).join("");
  }
  function codeBlock(code, lang) {
    const pre = document.createElement("pre");
    pre.className = "code";
    const c = document.createElement("code");
    pre.appendChild(c);
    if (window.CodeMirror && CodeMirror.runMode) CodeMirror.runMode(code, lang === "sql" ? "text/x-sql" : "python", c);
    else c.textContent = code;
    return pre.outerHTML;
  }
  function md(src) {
    if (!src) return "";
    const out = [], lines = String(src).split("\n");
    let para = [], i = 0;
    const flush = () => { if (para.length) { out.push(`<p>${inline(para.join(" "))}</p>`); para = []; } };
    const LI = /^\s*(?:-|\d+\.)\s+(.*)$/;
    while (i < lines.length) {
      const l = lines[i];
      if (l.startsWith("```")) {
        flush();
        const lang = l.slice(3).trim() || "python", buf = [];
        i++;
        while (i < lines.length && !lines[i].startsWith("```")) buf.push(lines[i++]);
        i++;
        out.push(codeBlock(buf.join("\n"), lang));
        continue;
      }
      if (/^\s*\|/.test(l)) {
        flush();
        const rows = [];
        while (i < lines.length && /^\s*\|/.test(lines[i])) rows.push(lines[i++]);
        const cells = (r) => r.trim().replace(/^\||\|$/g, "").split(/(?<!\\)\|/).map((c) => inline(c.trim().replace(/\\\|/g, "|")));
        const body = rows.filter((r) => !/^\s*\|[\s:|-]+\|\s*$/.test(r));
        const [head, ...rest] = body;
        out.push(`<div class="md-table"><table><thead><tr>${cells(head).map((c) => `<th>${c}</th>`).join("")}</tr></thead><tbody>${rest.map((r) => `<tr>${cells(r).map((c) => `<td>${c}</td>`).join("")}</tr>`).join("")}</tbody></table></div>`);
        continue;
      }
      if (l.startsWith("> ")) {
        flush();
        const buf = [];
        while (i < lines.length && lines[i].startsWith("> ")) buf.push(lines[i++].slice(2));
        const t = buf.join(" ");
        const kind = t.startsWith("⚠️") ? "warn" : t.startsWith("💼") ? "work" : "tip";
        out.push(`<div class="callout ${kind}">${inline(t)}</div>`);
        continue;
      }
      if (/^#{2,4}\s/.test(l)) { flush(); out.push(`<h4>${inline(l.replace(/^#+\s*/, ""))}</h4>`); i++; continue; }
      if (LI.test(l)) {
        flush();
        const ordered = /^\s*\d+\./.test(l), items = [];
        while (i < lines.length && LI.test(lines[i])) items.push(`<li>${inline(lines[i++].match(LI)[1])}</li>`);
        out.push(ordered ? `<ol>${items.join("")}</ol>` : `<ul>${items.join("")}</ul>`);
        continue;
      }
      if (!l.trim()) { flush(); i++; continue; }
      para.push(l); i++;
    }
    flush();
    return out.join("");
  }
  const pre = (txt) => `<pre class="plain">${esc(txt)}</pre>`;
  // mezcla determinista (para que la opción correcta no sea siempre la primera)
  function hash(s) { let h = 2166136261; for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); } return h >>> 0; }
  function shuffled(arr, seed) {
    const a = arr.map((v, i) => [v, i]);
    let x = hash(String(seed)) || 1;
    for (let i = a.length - 1; i > 0; i--) { x ^= x << 13; x ^= x >>> 17; x ^= x << 5; const j = (x >>> 0) % (i + 1); [a[i], a[j]] = [a[j], a[i]]; }
    return a; // [[valor, índiceOriginal], ...]
  }
  Object.assign(A, { esc, inline, md, codeBlock, pre, shuffled, hash });

  /* ------------------------------------------------------------------ estado */
  const KEY = "pq_state_v3";
  const fresh = () => ({
    v: 3, ex: {}, code: {}, skills: {}, quiz: {}, evals: {}, gateOk: {},
    streak: { last: null, count: 0 }, day: { date: null, count: 0 }, created: Date.now(),
  });
  function load() {
    let s = null;
    try { s = JSON.parse(localStorage.getItem(KEY)); } catch (e) { s = null; }
    s = Object.assign(fresh(), s || {});
    if (!s.migrated) {
      // migra lo resuelto en la versión anterior (solo como evidencia de "resolver")
      try {
        const old = JSON.parse(localStorage.getItem("pq_state_v2") || "null");
        if (old && old.solved) {
          Object.keys(old.solved).forEach((id) => {
            const e = EX_BY[id];
            if (!e || (s.ex[id] && s.ex[id].status === "done")) return;
            s.ex[id] = { status: "done", attempts: 1, hint: (old.hints && old.hints[id]) >= 2 ? 6 : 0, migrated: true, at: old.solved[id].at || Date.now() };
            const w = s.ex[id].hint >= 6 ? 0.25 : 1;
            e.concepts.forEach((c) => { const k = sk(s, c); k.prac++; k.res = Math.min(2, k.res + w); k.known = k.known || Date.now(); });
          });
          if (old.code) Object.keys(old.code).forEach((id) => { if (EX_BY[id] && s.code[id] == null) s.code[id] = old.code[id]; });
        }
      } catch (e) { /* sin datos previos */ }
      s.migrated = true;
    }
    return s;
  }
  function sk(s, c) {
    return (s.skills[c] = s.skills[c] || { known: 0, prac: 0, comp: { ok: 0, n: 0 }, rec: { ok: 0, n: 0 }, res: 0, dbg: 0, exp: 0, trf: 0 });
  }
  A.S = load();
  A.save = () => { try { localStorage.setItem(KEY, JSON.stringify(A.S)); } catch (e) { /* sin storage */ } };
  A.skill = (c) => sk(A.S, c);
  A.exState = (id) => (A.S.ex[id] = A.S.ex[id] || { status: "new", attempts: 0, hint: 0 });
  A.peekEx = (id) => A.S.ex[id] || { status: "new", attempts: 0, hint: 0 };
  A.resetState = () => { A.S = fresh(); A.S.migrated = true; A.save(); };

  const ymd = (d) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
  const today = () => ymd(new Date());
  const yesterday = () => { const d = new Date(); d.setDate(d.getDate() - 1); return ymd(d); };
  A.streakNow = () => (A.S.streak.last === today() || A.S.streak.last === yesterday() ? A.S.streak.count : 0);
  A.dayCount = () => (A.S.day.date === today() ? A.S.day.count : 0);
  A.GOAL = 3;
  function tickActivity() {
    const t = today(), S = A.S;
    if (S.streak.last !== t) { S.streak.count = S.streak.last === yesterday() ? S.streak.count + 1 : 1; S.streak.last = t; }
    if (S.day.date !== t) S.day = { date: t, count: 0 };
    S.day.count++;
  }

  /* ------------------------------------------------------------------ evidencia y dominio */
  // peso según la ayuda usada: pistas 1-3 no penalizan; concepto/ejemplo 0.5; código de la solución 0.25
  A.weightFor = (id) => {
    const st = A.peekEx(id);
    if ((st.solStage || 0) >= 3) return 0.25;
    if ((st.hint || 0) >= 4) return 0.5;
    return 1;
  };
  A.markSeen = (concepts) => { concepts.forEach((c) => { const k = A.skill(c); if (!k.known) k.known = Date.now(); }); A.save(); };
  A.practiced = (concepts) => { concepts.forEach((c) => { const k = A.skill(c); k.prac++; if (!k.known) k.known = Date.now(); }); A.save(); };
  A.credit = (concepts, dim, amount) => {
    concepts.forEach((c) => { const k = A.skill(c); k[dim] = Math.min(3, (k[dim] || 0) + amount); });
    A.save();
  };
  A.ratio = (concepts, dim, ok) => {
    concepts.forEach((c) => { const k = A.skill(c); k[dim].n++; if (ok) k[dim].ok++; if (!k.known) k.known = Date.now(); k.prac++; });
    A.save();
  };
  // marca un ejercicio como completado (una sola vez) y registra actividad
  A.complete = (e, extra = {}) => {
    const st = A.exState(e.id);
    const first = st.status !== "done";
    Object.assign(st, extra, { status: "done" });
    if (first) { st.at = Date.now(); tickActivity(); }
    A.save();
    A.updateTop();
    return first;
  };
  A.tried = (e) => { const st = A.exState(e.id); st.attempts = (st.attempts || 0) + 1; if (st.status === "new") st.status = "tried"; A.save(); };

  // valor 0..1 de un indicador para un concepto (null = no aplica)
  A.dimValue = (cid, dim) => {
    if (!APPLIES[cid].has(dim)) return null;
    const k = A.S.skills[cid];
    if (!k) return 0;
    switch (dim) {
      case "known": return k.known ? 1 : 0;
      case "prac": return k.prac >= 2 ? 1 : k.prac ? 0.5 : 0;
      case "comp": return k.comp.ok >= 1 ? 1 : 0;
      case "rec": {
        const r = k.rec.n ? k.rec.ok / k.rec.n : 0;
        return k.rec.ok >= 2 && r >= 0.7 ? 1 : k.rec.ok >= 1 ? 0.5 : 0;
      }
      default: return k[dim] >= 1 ? 1 : k[dim] > 0 ? 0.5 : 0;
    }
  };
  A.mastery = (cid) => {
    const vals = A.DIMS.map((d) => A.dimValue(cid, d.k)).filter((v) => v !== null);
    return vals.length ? vals.reduce((a, b) => a + b, 0) / vals.length : 0;
  };
  A.masteryLabel = (v) => (v >= 0.999 ? ["Dominado", "lv4"] : v >= 0.7 ? ["Comprendido", "lv3"] : v >= 0.4 ? ["En práctica", "lv2"] : v >= 0.15 ? ["Conocido", "lv1"] : ["Por descubrir", "lv0"]);
  A.modMastery = (m) => m.concepts.reduce((s, c) => s + A.mastery(c.id), 0) / m.concepts.length;
  A.globalMastery = () => { const all = Object.keys(CON_BY); return all.reduce((s, c) => s + A.mastery(c), 0) / all.length; };
  A.dimAggregate = (concepts) => A.DIMS.map((d) => {
    const vals = concepts.map((c) => A.dimValue(c, d.k)).filter((v) => v !== null);
    return { ...d, v: vals.length ? vals.reduce((a, b) => a + b, 0) / vals.length : 0 };
  });
  A.modDone = (m) => m.exercises.filter((e) => A.peekEx(e.id).status === "done").length;
  A.nextFor = (m) => m.exercises.find((e) => A.peekEx(e.id).status !== "done");
  A.nextGlobal = () => {
    for (const m of MODS) { const n = A.nextFor(m); if (n) return n; }
    return null;
  };

  /* ------------------------------------------------------------------ UI común */
  A.toast = (ico, title, sub = "") => {
    const t = document.createElement("div");
    t.className = "toast";
    t.innerHTML = `<span class="ico">${ico}</span><div><b>${esc(title)}</b>${sub ? `<small>${esc(sub)}</small>` : ""}</div>`;
    $("#toasts").appendChild(t);
    setTimeout(() => { t.classList.add("out"); setTimeout(() => t.remove(), 320); }, 3600);
  };
  const modalQueue = [];
  let modalOpen = false;
  A.modal = (html, cls = "", onOpen) => { modalQueue.push({ html, cls, onOpen }); if (!modalOpen) nextModal(); };
  function nextModal() {
    const m = modalQueue.shift();
    if (!m) { modalOpen = false; $("#modal").classList.add("hidden"); document.body.classList.remove("no-scroll"); return; }
    modalOpen = true;
    const card = $("#modalCard");
    card.className = "modal-card " + m.cls;
    card.innerHTML = m.html;
    $("#modal").classList.remove("hidden");
    document.body.classList.add("no-scroll");
    $$("[data-close]", card).forEach((b) => b.addEventListener("click", nextModal));
    if (m.onOpen) m.onOpen(card);
    const f = card.querySelector("button, a, textarea");
    if (f) f.focus();
  }
  A.closeModal = nextModal;
  $("#modal").addEventListener("click", (e) => { if (e.target.id === "modal") nextModal(); });
  document.addEventListener("keydown", (e) => { if (e.key === "Escape" && modalOpen) nextModal(); });

  A.copy = async (text, btn) => {
    let ok = false;
    try { await navigator.clipboard.writeText(text); ok = true; } catch (e) {
      const ta = document.createElement("textarea");
      ta.value = text; document.body.appendChild(ta); ta.select();
      try { ok = document.execCommand("copy"); } catch (e2) { ok = false; }
      ta.remove();
    }
    if (btn) { const t = btn.textContent; btn.textContent = ok ? "✓ Copiado" : "No se pudo copiar"; setTimeout(() => (btn.textContent = t), 1500); }
    return ok;
  };

  A.ring = (v, size = 84, label) => {
    const p = Math.round(v * 100);
    return `<div class="ring" style="--p:${p};--s:${size}px"><span>${label != null ? label : p + "%"}</span></div>`;
  };
  A.bar = (v, color) => `<div class="bar"${color ? ` style="--c:${color}"` : ""}><i style="width:${Math.round(v * 100)}%"></i></div>`;
  A.dimPills = (cid) => `<div class="dims">${A.DIMS.map((d) => {
    const v = A.dimValue(cid, d.k);
    const cls = v === null ? "na" : v >= 1 ? "on" : v > 0 ? "half" : "off";
    return `<span class="dim ${cls}" title="${esc(d.n)}: ${v === null ? "no aplica a este concepto" : esc(d.d)}">${esc(d.n)}</span>`;
  }).join("")}</div>`;
  A.levelBadge = (lv) => `<span class="lvl lvl-${lv}">${esc(D.levels[lv])}</span>`;
  A.typeBadge = (t) => `<span class="type t-${t}">${A.TYPE_ICON[t]} ${esc(D.types[t])}</span>`;
  A.statusIcon = (id) => { const s = A.peekEx(id).status; return s === "done" ? "✓" : s === "tried" ? "◐" : ""; };

  /* ------------------------------------------------------------------ barra superior */
  A.updateTop = () => {
    const g = A.globalMastery();
    $("#mastTop").innerHTML = `${A.ring(g, 30, "")}<span class="mt-txt"><b>${Math.round(g * 100)}%</b> dominio</span>`;
    $("#streakChip b").textContent = A.streakNow();
    $("#themeBtn").textContent = document.documentElement.dataset.theme === "light" ? "🌙" : "☀️";
    const h = location.hash || "#/";
    $$(".nav a").forEach((a) => a.classList.toggle("on", a.dataset.nav && h.startsWith(a.dataset.nav) && (a.dataset.nav !== "#/" || h === "#/" || h === "")));
  };
  $("#themeBtn").addEventListener("click", () => {
    const t = document.documentElement.dataset.theme === "light" ? "dark" : "light";
    document.documentElement.dataset.theme = t;
    try { localStorage.setItem("pq_theme", t); } catch (e) { /* */ }
    A.updateTop();
  });

  /* ------------------------------------------------------------------ Python (Web Worker + Pyodide) */
  let worker, seq = 0;
  const pending = new Map(), waiters = [];
  A.pyReady = false;
  const libsReady = new Set();
  function setPy(state, text) {
    const el = $("#pyStatus");
    el.className = "py-status " + state;
    $(".txt", el).textContent = text;
  }
  function startWorker() {
    A.pyReady = false;
    libsReady.clear();
    setPy("", "Cargando Python…");
    worker = new Worker("js/worker.js");
    worker.onmessage = (ev) => {
      const m = ev.data;
      if (m.type === "status") setPy("", m.text);
      else if (m.type === "ready") { A.pyReady = true; setPy("ready", "Python listo"); waiters.splice(0).forEach((f) => f()); }
      else if (m.type === "fatal") setPy("error", "Error cargando Python");
      else if (m.type === "result") {
        const p = pending.get(m.id);
        if (p) { pending.delete(m.id); clearTimeout(p.t); p.res(m.data); }
      }
    };
    worker.onerror = () => setPy("error", "Error cargando Python");
  }
  const whenReady = () => (A.pyReady ? Promise.resolve() : new Promise((r) => waiters.push(r)));
  A.py = async (msg, timeout = 30000) => {
    await whenReady();
    return new Promise((res) => {
      const id = ++seq;
      const t = setTimeout(() => {
        pending.delete(id);
        worker.terminate();
        pending.forEach((p) => { clearTimeout(p.t); p.res({ error: { msg: "Python se reinició" } }); });
        pending.clear();
        startWorker();
        res({ error: { msg: "⏱️ El código tardó demasiado. ¿Hay un bucle infinito?", line: null, tip: "Python se reinició solo. Revisá que la condición del while cambie en cada vuelta." } });
      }, timeout);
      pending.set(id, { res, t });
      worker.postMessage(Object.assign({ id }, msg));
    });
  };
  A.libMsg = (m) => ({ packages: m.packages || [], pip: m.micropip || [] });
  A.ensureMod = async (m) => {
    if ((!m.packages.length && !m.micropip.length) || libsReady.has(m.id)) return {};
    const r = await A.py(Object.assign({ type: "load" }, A.libMsg(m)), 300000);
    if (!r.error) libsReady.add(m.id);
    return r;
  };
  A.libsReady = libsReady;
  A.startWorker = startWorker;

  /* ------------------------------------------------------------------ modal de datos */
  const tablesCache = {};
  A.showTables = (m) => {
    A.modal(`<div class="modal-top"><h2>📋 Datos disponibles · ${esc(m.title)}</h2><button class="btn small" data-close>Cerrar</button></div>
      <p class="muted small">Estas variables ya están cargadas cuando ejecutás tu código. Miralas antes de planificar: ¿qué columnas y tipos tienen?</p>
      <div class="tabs" id="tblTabs">${m.tables.map((t, i) => `<button class="tab ${i ? "" : "on"}" data-t="${esc(t)}">${esc(t)}</button>`).join("")}</div>
      <div id="tblBody"><div class="placeholder"><span class="big">⏳</span>${A.pyReady ? "Cargando datos…" : "Esperando a que Python termine de cargar…"}</div></div>
      ${m.packages.includes("sqlite3") ? '<p class="small">También tenés <code>conn</code>: una base SQLite con <code>clientes</code>, <code>productos</code> y <code>pedidos</code>.</p>' : ""}`,
    "wide", async (card) => {
      if (!tablesCache[m.id]) {
        await A.ensureMod(m);
        tablesCache[m.id] = await A.py(Object.assign({ type: "tables", setup: m.setup, names: m.tables }, A.libMsg(m)), 120000);
      }
      const data = tablesCache[m.id];
      if (!card.isConnected || !$("#tblBody", card)) return;
      if (data.error) { $("#tblBody", card).innerHTML = `<p>Error: ${esc(data.error.msg)}</p>`; delete tablesCache[m.id]; return; }
      const show = (t) => {
        const d = data[t];
        $("#tblBody", card).innerHTML = `<p class="dtypes"><b>${esc(t)}</b> · ${esc(d.info)}<br>${esc(d.dtypes)}</p>${d.html}`;
        $$(".tab", card).forEach((b) => b.classList.toggle("on", b.dataset.t === t));
      };
      $$(".tab", card).forEach((b) => b.addEventListener("click", () => show(b.dataset.t)));
      show(m.tables[0]);
    });
  };
})();
