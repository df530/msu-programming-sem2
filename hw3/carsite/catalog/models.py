from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название фирмы")
    headquarters = models.CharField(max_length=100, blank=True, verbose_name="Штаб-квартира")

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название страны")

    def __str__(self):
        return self.name


class Car(models.Model):
    name = models.CharField(max_length=100, verbose_name="Модель автомобиля")
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="cars",
        verbose_name="Фирма-производитель"
    )
    countries = models.ManyToManyField(
        Country,
        related_name="cars",
        verbose_name="Страны производства"
    )

    def __str__(self):
        return self.name


class CarDescription(models.Model):
    car = models.OneToOneField(Car, on_delete=models.CASCADE, verbose_name="Автомобиль")
    description = models.TextField(verbose_name="Полное описание", blank=True)
    image = models.ImageField(
        upload_to='car_images/',
        blank=True,
        null=True,
        verbose_name="Фото автомобиля"
    )

    def __str__(self):
        return f"Описание для {self.car.name}"
