/* DataLab · router e inicio */
(() => {
  "use strict";
  const A = window.PQA;

  function route() {
    const raw = location.hash.slice(1) || "/";
    const [path, query] = raw.split("?");
    const parts = path.split("/").filter(Boolean);
    const params = new URLSearchParams(query || "");
    A.clearEditors();
    const mod = (id) => A.MODS.find((m) => m.id === id);
    if (parts[0] === "e" && A.EX_BY[parts[1]]) A.renderExercise(A.EX_BY[parts[1]]);
    else if (parts[0] === "m" && mod(parts[1])) A.renderModule(mod(parts[1]), parts[2]);
    else if (parts[0] === "c" && A.CON_BY[parts[1]]) A.renderConcept(A.CON_BY[parts[1]]);
    else if (parts[0] === "quiz") A.renderQuiz(params);
    else if (parts[0] === "eval" && mod(parts[1])) A.renderEval(mod(parts[1]));
    else if (parts[0] === "ia") A.renderIA();
    else if (parts[0] === "progreso") A.renderProgress();
    else A.renderHome();
    A.updateTop();
    window.scrollTo(0, 0);
    const main = document.getElementById("app");
    if (main) main.focus({ preventScroll: true });
  }
  window.addEventListener("hashchange", route);

  A.updateTop();
  A.startWorker();
  route();

  // para pruebas automáticas
  window.__pq = { A, get state() { return A.S; } };
})();
