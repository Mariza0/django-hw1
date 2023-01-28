from django.shortcuts import render, redirect
from phones.models import list_phones, product


def index(request):
    return redirect('catalog')


def show_catalog(request):
    sort = request.GET.get('sort', "") # берем параметр сортировки
    template = 'catalog.html'
    list_phone = list_phones(sort) # запрос к БД
    context = {'phones': list_phone}
    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'
    phone = product(slug) # запрос к БД
    context = {'phone': phone}
    return render(request, template, context)