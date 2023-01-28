import csv

from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    # получите текущую страницу и передайте ее в контекст
    # также передайте в контекст список станций на странице
    page_number = int(request.GET.get('page', 1))
    bus_station = []

    with open('data-398-2018-08-30.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
                print(row)
                name = row['Name']
                street = row['Street']
                district = row['District']
                dict1 = {'station': {
                            'Name': '',
                            'Street': '',
                            'District': '',}}
                dict1['station']['Name'] = name
                dict1['station']['Street'] = street
                dict1['station']['District'] = district
                bus_station.append(dict1)

    paginator = Paginator(bus_station, 10)
    page = paginator.get_page(page_number)
    context = {'page': page}
    return render(request, 'stations/index.html', context)
