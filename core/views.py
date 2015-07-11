from django.http.response import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
import json
from django.http import JsonResponse
from models import Booking
from models import Menu


def menu_place(request, place):
    menu_set = Menu.objects.filter(school__place=place).values()

    return JsonResponse(menu_set)

def menu_place_booked(request, place, year, month):
    # do something with the your data
    months =[
        'jan',
        'feb',
        'mar',
        'apr',
        'may',
        'jun',
        'jul',
        'aug',
        'sep',
        'oct',
        'nov',
        'dec'
    ]
    months_dict ={
        'jan':1,
        'feb':2,
        'mar':3,
        'apr':4,
        'may':5,
        'jun':6,
        'jul':7,
        'aug':8,
        'sep':9,
        'oct':10,
        'nov':11,
        'dec':12
    }
    if month not in months:
        raise HttpResponseNotFound()

    month_num = months_dict[month]
    data = {}
    # menu_set = Menu.objects.filter(school__place=place)
    place_obj = Place.objects.get(name=place)
    Menu.objects.filter(place=place_obj)
    closed_spots = Booking.objects.filter(menu__place=place, date__in=[])
    for booked in closed_spots:
        if booked.month in data:
            if booked
                data[booked.month]

    # just return a JsonResponse
    return JsonResponse(data)


