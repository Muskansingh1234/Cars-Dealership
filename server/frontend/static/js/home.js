/* Home page: list dealers, filter by state, show "Review Dealer" when logged in. */
(function () {
  "use strict";
  const select = document.getElementById("state-filter");
  const rows = document.getElementById("dealer-rows");
  const status = document.getElementById("dealer-status");
  const reviewHead = document.getElementById("review-col");
  let loggedIn = false;

  function render(dealers) {
    reviewHead.hidden = !loggedIn;
    if (!dealers.length) {
      rows.innerHTML = "";
      status.textContent = "No dealerships found for this state.";
      return;
    }
    status.textContent = dealers.length + (dealers.length === 1 ? " dealership" : " dealerships");
    rows.innerHTML = dealers.map((d) =>
      "<tr>" +
      "<td>" + esc(d.id) + "</td>" +
      '<td><a href="/dealer/' + esc(d.id) + '/">' + esc(d.full_name) + "</a></td>" +
      "<td>" + esc(d.city) + "</td>" +
      "<td>" + esc(d.address) + "</td>" +
      "<td>" + esc(d.zip) + "</td>" +
      "<td>" + esc(d.state) + "</td>" +
      (loggedIn
        ? '<td><a class="btn btn-outline" href="/postreview/' + esc(d.id) + '/">Review Dealer</a></td>'
        : "") +
      "</tr>").join("");
  }

  async function fetchDealers(state) {
    const url = state ? "/djangoapp/get_dealers/" + encodeURIComponent(state) : "/djangoapp/get_dealers";
    const res = await fetch(url, { credentials: "same-origin" });
    return (await res.json()).dealers || [];
  }

  async function show(state) {
    status.textContent = "Loading dealerships…";
    try { render(await fetchDealers(state)); }
    catch (e) { status.textContent = "Could not load dealerships. Refresh to try again."; }
  }

  (async function init() {
    await window.authReady;
    loggedIn = !!window.currentUser;
    const all = await fetchDealers("");
    const states = Array.from(new Set(all.map((d) => d.state))).sort();
    select.innerHTML = '<option value="">All states</option>' +
      states.map((s) => '<option value="' + esc(s) + '">' + esc(s) + "</option>").join("");
    const wanted = new URLSearchParams(window.location.search).get("state") || "";
    select.value = states.indexOf(wanted) >= 0 ? wanted : "";
    if (select.value) { show(select.value); } else { render(all); }
    select.addEventListener("change", () => {
      const state = select.value;
      history.pushState({}, "", "/dealers/" + (state ? "?state=" + encodeURIComponent(state) : ""));
      show(state);
    });
  })();
})();
