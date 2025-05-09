from django.contrib import admin
from .models import Company, Country, Car, CarDescription

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "headquarters")

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "company")

@admin.register(CarDescription)
class CarDescriptionAdmin(admin.ModelAdmin):
    list_display = ("id", "car")
