/* Post Review page. */
(function () {
  "use strict";
  const id = window.pathId();
  const form = document.getElementById("review-form");
  const msg = document.getElementById("form-message");
  const title = document.getElementById("dealer-title");
  const carSelect = document.getElementById("car");
  const purchase = document.getElementById("purchase");
  const purchaseFields = document.getElementById("purchase-fields");

  purchase.addEventListener("change", () => { purchaseFields.hidden = !purchase.checked; });

  (async function init() {
    await window.authReady;
    if (!window.currentUser) {
      form.hidden = true;
      msg.innerHTML = 'You need to <a href="/login/">log in</a> before posting a review.';
      msg.className = "error";
      return;
    }
    const [dRes, cRes] = await Promise.all([fetch("/djangoapp/dealer/" + id), fetch("/djangoapp/get_cars")]);
    if (dRes.ok) title.textContent = (await dRes.json()).dealer[0].full_name;
    const cars = (await cRes.json()).CarModels || [];
    carSelect.innerHTML = '<option value="">Choose a car</option>' +
      cars.map((c) => '<option value="' + esc(c.CarMake + "|" + c.CarModel) + '">' +
        esc(c.CarMake + " " + c.CarModel) + "</option>").join("");
  })();

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    msg.textContent = ""; msg.className = "";
    const [make, model] = carSelect.value ? carSelect.value.split("|") : ["", ""];
    if (purchase.checked && (!make || !document.getElementById("year").value)) {
      msg.textContent = "Choose the car and year you purchased."; msg.className = "error"; return;
    }
    const btn = form.querySelector("button[type=submit]");
    btn.disabled = true;
    const result = await window.postJSON("/djangoapp/add_review", {
      dealership: Number(id),
      review: document.getElementById("review").value,
      purchase: purchase.checked,
      purchase_date: purchase.checked ? document.getElementById("date").value : "",
      car_make: purchase.checked ? make : "",
      car_model: purchase.checked ? model : "",
      car_year: purchase.checked ? document.getElementById("year").value : "",
    });
    if (result.ok) { window.location.href = "/dealer/" + id + "/"; return; }
    msg.textContent = result.data.message || "Could not post the review.";
    msg.className = "error";
    btn.disabled = false;
  });
})();
