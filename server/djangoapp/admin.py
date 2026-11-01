from django.contrib import admin

from .models import CarMake, CarModel, Dealer, Review


class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 1


@admin.register(CarMake)
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    inlines = [CarModelInline]


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ("name", "car_make", "type", "year")
    list_filter = ("car_make", "type")


@admin.register(Dealer)
class DealerAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "city", "state", "zip")
    list_filter = ("state",)
    search_fields = ("full_name", "city")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "dealership", "sentiment", "created_at")
    list_filter = ("sentiment", "dealership")
