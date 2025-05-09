from django.shortcuts import render, get_object_or_404
from .models import Car


def home(request):
    # Пример простой главной страницы
    return render(request, 'catalog/home.html')


def car_list(request):
    cars = Car.objects.all()
    return render(request, 'catalog/car_list.html', {'cars': cars})


def car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    return render(request, 'catalog/car_detail.html', {'car': car})
