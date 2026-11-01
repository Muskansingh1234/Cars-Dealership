/*
 * Register.jsx — Sign-up page component (React).
 * Five inputs: Username, First Name, Last Name, Email, Password + a Register button.
 * Loaded in the browser through Babel standalone by static/Register.html (no build step needed).
 * If you move this into a Vite/CRA project, replace the first line with
 *   import React, { useState } from "react";
 * and add `export default Register;` at the bottom.
 */
const { useState } = React;

function Register() {
  const [form, setForm] = useState({
    userName: "",
    firstName: "",
    lastName: "",
    email: "",
    password: "",
  });
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  const onChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const onSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setBusy(true);
    try {
      const res = await fetch("/djangoapp/register", {
        method: "POST",
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });
      const data = await res.json();
      if (res.ok) {
        window.location.href = "/";
        return;
      }
      setError(data.error || data.message || "Registration failed. Please try again.");
    } catch (err) {
      setError("Could not reach the server. Please try again.");
    }
    setBusy(false);
  };

  return (
    <div className="panel form-card">
      <h1>Sign up</h1>
      <form onSubmit={onSubmit} id="register-form">
        <div className="field">
          <label htmlFor="userName">Username</label>
          <input id="userName" name="userName" type="text" value={form.userName}
                 onChange={onChange} autoComplete="username" required />
        </div>
        <div className="row-2">
          <div className="field">
            <label htmlFor="firstName">First Name</label>
            <input id="firstName" name="firstName" type="text" value={form.firstName}
                   onChange={onChange} autoComplete="given-name" required />
          </div>
          <div className="field">
            <label htmlFor="lastName">Last Name</label>
            <input id="lastName" name="lastName" type="text" value={form.lastName}
                   onChange={onChange} autoComplete="family-name" required />
          </div>
        </div>
        <div className="field">
          <label htmlFor="email">Email</label>
          <input id="email" name="email" type="email" value={form.email}
                 onChange={onChange} autoComplete="email" required />
        </div>
        <div className="field">
          <label htmlFor="password">Password</label>
          <input id="password" name="password" type="password" value={form.password}
                 onChange={onChange} autoComplete="new-password" minLength={8} required />
        </div>
        {error && <p className="error" role="alert">{error}</p>}
        <button type="submit" className="btn" disabled={busy}>
          {busy ? "Registering…" : "Register"}
        </button>
        <p className="muted">Already have an account? <a href="/login/">Log in</a></p>
      </form>
    </div>
  );
}

window.Register = Register;
