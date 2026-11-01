from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class CarMake(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class CarModel(models.Model):
    SEDAN, SUV, WAGON, TRUCK, HATCHBACK, COUPE = "Sedan", "SUV", "Wagon", "Truck", "Hatchback", "Coupe"
    TYPE_CHOICES = [(t, t) for t in (SEDAN, SUV, WAGON, TRUCK, HATCHBACK, COUPE)]

    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE, related_name="models")
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=SEDAN)
    year = models.IntegerField(
        default=2023, validators=[MinValueValidator(2015), MaxValueValidator(2035)]
    )

    class Meta:
        ordering = ["car_make__name", "name"]
        unique_together = ("car_make", "name")

    def __str__(self):
        return f"{self.car_make.name} {self.name}"


class Dealer(models.Model):
    full_name = models.CharField(max_length=150)
    short_name = models.CharField(max_length=80)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=80)
    state = models.CharField(max_length=60)
    st = models.CharField("State abbreviation", max_length=2)
    zip = models.CharField(max_length=10)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.full_name

    def to_dict(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "short_name": self.short_name,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "st": self.st,
            "zip": self.zip,
            "lat": self.latitude,
            "long": self.longitude,
        }


class Review(models.Model):
    dealership = models.ForeignKey(Dealer, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL
    )
    name = models.CharField(max_length=100)
    review = models.TextField()
    purchase = models.BooleanField(default=False)
    purchase_date = models.DateField(null=True, blank=True)
    car_make = models.CharField(max_length=100, blank=True)
    car_model = models.CharField(max_length=100, blank=True)
    car_year = models.IntegerField(null=True, blank=True)
    sentiment = models.CharField(max_length=10, default="neutral")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.name} on {self.dealership.short_name}"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "dealership": self.dealership_id,
            "review": self.review,
            "purchase": self.purchase,
            "purchase_date": self.purchase_date.isoformat() if self.purchase_date else "",
            "car_make": self.car_make,
            "car_model": self.car_model,
            "car_year": self.car_year,
            "sentiment": self.sentiment,
        }
