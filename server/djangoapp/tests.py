import json

from django.core.management import call_command
from django.test import TestCase

from .sentiment import analyze


class SentimentTests(TestCase):
    def test_positive(self):
        self.assertEqual(analyze("Fantastic services")[0], "positive")

    def test_negative(self):
        self.assertEqual(analyze("Terrible, rude and slow")[0], "negative")

    def test_negation(self):
        self.assertEqual(analyze("not good")[0], "negative")

    def test_neutral(self):
        self.assertEqual(analyze("The showroom opens at nine")[0], "neutral")


class ApiTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed", verbosity=0)

    def post(self, url, payload):
        return self.client.post(url, data=json.dumps(payload), content_type="application/json")

    def test_all_dealers(self):
        data = self.client.get("/djangoapp/get_dealers").json()
        self.assertEqual(data["status"], 200)
        self.assertGreaterEqual(len(data["dealers"]), 10)

    def test_dealers_by_state_kansas(self):
        dealers = self.client.get("/djangoapp/get_dealers/Kansas").json()["dealers"]
        self.assertGreaterEqual(len(dealers), 1)
        self.assertTrue(all(d["state"] == "Kansas" for d in dealers))

    def test_dealer_by_id_and_404(self):
        self.assertEqual(self.client.get("/djangoapp/dealer/1").json()["dealer"][0]["id"], 1)
        self.assertEqual(self.client.get("/djangoapp/dealer/9999").status_code, 404)

    def test_dealer_reviews(self):
        reviews = self.client.get("/djangoapp/reviews/dealer/1").json()["reviews"]
        self.assertGreaterEqual(len(reviews), 1)
        self.assertIn(reviews[0]["sentiment"], {"positive", "negative", "neutral"})

    def test_car_makes(self):
        cars = self.client.get("/djangoapp/get_cars").json()["CarModels"]
        self.assertTrue(any(c["CarMake"] == "Honda" for c in cars))

    def test_analyze_endpoint(self):
        data = self.client.get("/djangoapp/analyze/Fantastic%20services").json()
        self.assertEqual(data["sentiment"], "positive")

    def test_login_logout_flow(self):
        bad = self.post("/djangoapp/login", {"userName": "demo", "password": "wrong"})
        self.assertEqual(bad.status_code, 401)
        ok = self.post("/djangoapp/login", {"userName": "demo", "password": "Demo@12345"})
        self.assertEqual(ok.json()["status"], "Authenticated")
        self.assertEqual(self.client.get("/djangoapp/current_user").json()["userName"], "demo")
        self.assertEqual(self.client.get("/djangoapp/logout").json()["userName"], "")
        self.assertEqual(self.client.get("/djangoapp/current_user").json()["userName"], "")

    def test_register(self):
        payload = {"userName": "newbie", "password": "Str0ngPass!", "firstName": "New",
                   "lastName": "User", "email": "new@example.com"}
        self.assertEqual(self.post("/djangoapp/register", payload).json()["status"], "Authenticated")
        self.assertEqual(self.post("/djangoapp/register", payload).status_code, 409)

    def test_add_review_requires_login_then_works(self):
        body = {"dealership": 1, "review": "Great and friendly team", "purchase": False}
        self.assertEqual(self.post("/djangoapp/add_review", body).status_code, 401)
        self.post("/djangoapp/login", {"userName": "demo", "password": "Demo@12345"})
        resp = self.post("/djangoapp/add_review", body).json()
        self.assertEqual(resp["review"]["sentiment"], "positive")
        reviews = self.client.get("/djangoapp/reviews/dealer/1").json()["reviews"]
        self.assertTrue(any(r["review"] == "Great and friendly team" for r in reviews))

    def test_seed_is_idempotent(self):
        before = self.client.get("/djangoapp/get_dealers").json()["dealers"]
        call_command("seed", verbosity=0)
        after = self.client.get("/djangoapp/get_dealers").json()["dealers"]
        self.assertEqual(len(before), len(after))


class PageTests(TestCase):
    def test_pages_render(self):
        for url in ["/", "/dealers/", "/about/", "/contact/", "/login/", "/register/",
                    "/dealer/1/", "/postreview/1/"]:
            self.assertEqual(self.client.get(url).status_code, 200, url)
