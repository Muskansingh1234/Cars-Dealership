# Screenshots (Tasks 12, 13, 17-22, 25-28)

Screenshots must come from YOUR running app. Save each one in this folder with the exact name below
(.png or .jpeg). Make sure the browser address bar is visible in every screenshot.

| Task | File name | Where / what to capture |
|------|-----------|--------------------------|
| 12 | `admin_login` | `http://127.0.0.1:8000/admin/` -> log in as `root`; capture the admin home page after login |
| 13 | `admin_logout` | Click "Log out" in the admin; capture the "Logged out" page |
| 17 | `get_dealers` | `http://127.0.0.1:8000/` while logged out - dealer table visible |
| 18 | `get_dealers_loggedin` | Log in as `demo`; home page showing your username in the nav, the **Review Dealer** buttons and the URL |
| 19 | `dealersbystate` | Pick **Kansas** in the filter; URL shows `/dealers/?state=Kansas` |
| 20 | `dealer_id_reviews` | Click a dealer, e.g. `/dealer/1/` - dealer details plus reviews |
| 21 | `dealership_review_submission` | `/postreview/1/` with the form filled in, **before** clicking Post review |
| 22 | `added_review` | After posting you land on `/dealer/1/` - capture your new review in the list |
| 25 | `deployed_landingpage` | Your deployed URL home page (logged out) |
| 26 | `deployed_loggedin` | Deployed site, logged in, username visible in the nav |
| 27 | `deployed_dealer_detail` | Deployed `/dealer/<id>/` page |
| 28 | `deployed_add_review` | Deployed dealer page showing a review you added |
