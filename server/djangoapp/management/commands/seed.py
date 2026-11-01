"""Load sample dealers, reviews, car makes/models and demo users. Safe to run repeatedly."""
import json
import os
from pathlib import Path

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from djangoapp.models import CarMake, CarModel, Dealer, Review
from djangoapp.sentiment import analyze

DATA_DIR = Path(__file__).resolve().parents[2] / "data"


def _load(name):
    with open(DATA_DIR / name, encoding="utf-8") as fh:
        return json.load(fh)


class Command(BaseCommand):
    help = "Seed the SQLite database with sample data and demo accounts."

    def handle(self, *args, **options):
        for d in _load("dealerships.json"):
            Dealer.objects.update_or_create(
                id=d["id"],
                defaults=dict(
                    full_name=d["full_name"], short_name=d["short_name"], address=d["address"],
                    city=d["city"], state=d["state"], st=d["st"], zip=d["zip"],
                    latitude=d["lat"], longitude=d["long"],
                ),
            )

        for r in _load("reviews.json"):
            label, _ = analyze(r["review"])
            Review.objects.update_or_create(
                id=r["id"],
                defaults=dict(
                    dealership_id=r["dealership"], name=r["name"], review=r["review"],
                    purchase=r["purchase"], purchase_date=r["purchase_date"] or None,
                    car_make=r["car_make"], car_model=r["car_model"], car_year=r["car_year"],
                    sentiment=label,
                ),
            )

        for make in _load("car_records.json"):
            obj, _ = CarMake.objects.get_or_create(
                name=make["name"], defaults={"description": make["description"]}
            )
            for m in make["models"]:
                CarModel.objects.get_or_create(
                    car_make=obj, name=m["name"], defaults={"type": m["type"], "year": m["year"]}
                )

        root_pw = os.environ.get("ROOT_PASSWORD", "Root@12345")
        if not User.objects.filter(username="root").exists():
            User.objects.create_superuser("root", "root@carsdealership.example", root_pw)
        demo_pw = os.environ.get("DEMO_PASSWORD", "Demo@12345")
        if not User.objects.filter(username="demo").exists():
            User.objects.create_user(
                "demo", "demo@carsdealership.example", demo_pw,
                first_name="Demo", last_name="Customer",
            )

        self.stdout.write(self.style.SUCCESS(
            f"Seeded {Dealer.objects.count()} dealers, {Review.objects.count()} reviews, "
            f"{CarMake.objects.count()} makes, {CarModel.objects.count()} models."
        ))
