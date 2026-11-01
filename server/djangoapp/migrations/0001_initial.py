import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="CarMake",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, unique=True)),
                ("description", models.TextField(blank=True)),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="Dealer",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("full_name", models.CharField(max_length=150)),
                ("short_name", models.CharField(max_length=80)),
                ("address", models.CharField(max_length=200)),
                ("city", models.CharField(max_length=80)),
                ("state", models.CharField(max_length=60)),
                ("st", models.CharField(max_length=2, verbose_name="State abbreviation")),
                ("zip", models.CharField(max_length=10)),
                ("latitude", models.FloatField(default=0.0)),
                ("longitude", models.FloatField(default=0.0)),
            ],
            options={"ordering": ["id"]},
        ),
        migrations.CreateModel(
            name="CarModel",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100)),
                ("type", models.CharField(
                    choices=[("Sedan", "Sedan"), ("SUV", "SUV"), ("Wagon", "Wagon"),
                             ("Truck", "Truck"), ("Hatchback", "Hatchback"), ("Coupe", "Coupe")],
                    default="Sedan", max_length=20)),
                ("year", models.IntegerField(
                    default=2023,
                    validators=[django.core.validators.MinValueValidator(2015),
                                django.core.validators.MaxValueValidator(2035)])),
                ("car_make", models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, related_name="models", to="djangoapp.carmake")),
            ],
            options={"ordering": ["car_make__name", "name"], "unique_together": {("car_make", "name")}},
        ),
        migrations.CreateModel(
            name="Review",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100)),
                ("review", models.TextField()),
                ("purchase", models.BooleanField(default=False)),
                ("purchase_date", models.DateField(blank=True, null=True)),
                ("car_make", models.CharField(blank=True, max_length=100)),
                ("car_model", models.CharField(blank=True, max_length=100)),
                ("car_year", models.IntegerField(blank=True, null=True)),
                ("sentiment", models.CharField(default="neutral", max_length=10)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("dealership", models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, related_name="reviews", to="djangoapp.dealer")),
                ("user", models.ForeignKey(
                    blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                    to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["id"]},
        ),
    ]
