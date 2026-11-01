/* Login page. */
(function () {
  "use strict";
  const form = document.getElementById("login-form");
  const msg = document.getElementById("form-message");
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    msg.textContent = "";
    const btn = form.querySelector("button[type=submit]");
    btn.disabled = true;
    const result = await window.postJSON("/djangoapp/login", {
      userName: document.getElementById("userName").value.trim(),
      password: document.getElementById("password").value,
    });
    if (result.ok) { window.location.href = "/"; return; }
    msg.textContent = "Wrong username or password. Check them and try again.";
    btn.disabled = false;
  });
})();
