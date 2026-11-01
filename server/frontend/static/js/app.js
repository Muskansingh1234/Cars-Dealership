/* Shared helpers: HTML escaping, session lookup and the nav auth area. */
(function () {
  "use strict";

  const esc = (v) =>
    String(v == null ? "" : v).replace(/[&<>"']/g, (c) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  window.esc = esc;
  window.currentUser = "";

  function renderAuth() {
    const area = document.getElementById("auth-area");
    if (!area) return;
    if (window.currentUser) {
      area.innerHTML =
        '<span class="nav-user" id="nav-username">' + esc(window.currentUser) + "</span>" +
        '<button type="button" class="btn btn-ghost" id="logout-btn">Logout</button>';
      document.getElementById("logout-btn").addEventListener("click", async () => {
        await fetch("/djangoapp/logout", { credentials: "same-origin" });
        window.location.href = "/";
      });
    } else {
      area.innerHTML =
        '<a class="nav-link" href="/login/">Login</a>' +
        '<a class="btn btn-accent" href="/register/">Register</a>';
    }
  }

  window.authReady = fetch("/djangoapp/current_user", { credentials: "same-origin" })
    .then((r) => r.json())
    .catch(() => ({ userName: "" }))
    .then((data) => {
      window.currentUser = data.userName || "";
      renderAuth();
      return window.currentUser;
    });

  window.postJSON = async function (url, body) {
    const res = await fetch(url, {
      method: "POST",
      credentials: "same-origin",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    let data = {};
    try { data = await res.json(); } catch (e) { /* non-JSON error page */ }
    return { ok: res.ok, status: res.status, data: data };
  };

  window.pathId = function () {
    const parts = window.location.pathname.split("/").filter(Boolean);
    return parts[1];
  };
})();
