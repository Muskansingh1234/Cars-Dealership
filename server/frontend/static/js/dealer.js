/* Dealer detail page: dealer info + reviews. */
(function () {
  "use strict";
  const id = window.pathId();
  const head = document.getElementById("dealer-head");
  const list = document.getElementById("review-list");

  function reviewCard(r) {
    const label = r.sentiment || "neutral";
    const car = [r.car_year, r.car_make, r.car_model].filter(Boolean).join(" ");
    return '<article class="review ' + esc(label) + '">' +
      "<header><strong>" + esc(r.name) + '</strong><span class="badge ' + esc(label) + '">' +
      esc(label.charAt(0).toUpperCase() + label.slice(1)) + "</span></header>" +
      "<p>" + esc(r.review) + "</p>" +
      (r.purchase ? '<p class="muted">Purchased' + (car ? ": " + esc(car) : "") +
        (r.purchase_date ? " on " + esc(r.purchase_date) : "") + "</p>" : "") +
      "</article>";
  }

  (async function init() {
    await window.authReady;
    try {
      const [dRes, rRes] = await Promise.all([
        fetch("/djangoapp/dealer/" + id), fetch("/djangoapp/reviews/dealer/" + id),
      ]);
      if (!dRes.ok) { head.innerHTML = '<p class="error">Dealer not found. <a href="/">Back to all dealers</a></p>'; return; }
      const dealer = (await dRes.json()).dealer[0];
      const reviews = (await rRes.json()).reviews || [];
      document.title = dealer.full_name + " | Cars Dealership";
      head.innerHTML =
        "<h1>" + esc(dealer.full_name) + "</h1>" +
        '<p class="lead">' + esc(dealer.address) + ", " + esc(dealer.city) + ", " + esc(dealer.state) + " " + esc(dealer.zip) + "</p>" +
        (window.currentUser
          ? '<a class="btn" id="post-review-link" href="/postreview/' + esc(dealer.id) + '/">Post a review</a>'
          : '<p class="muted"><a href="/login/">Log in</a> to post a review.</p>');
      list.innerHTML = reviews.length
        ? reviews.map(reviewCard).join("")
        : '<p class="status">No reviews yet for this dealership.</p>';
    } catch (e) {
      head.innerHTML = '<p class="error">Could not load this dealership. Refresh to try again.</p>';
    }
  })();
})();
