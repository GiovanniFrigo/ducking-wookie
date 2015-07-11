import datetime
from django.http.response import Http404
from django.shortcuts import render
import json
from django.http import JsonResponse
from models import Booking, Menu, Place


def menu_place(request, place):
    place_obj = Place.objects.get(name=place)
    menu_set = list(Menu.objects.filter(available_in=place_obj).values())

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
        raise Http404()

    month_num = months_dict[month]
    month_selected = datetime.datetime(year=int(year), month=month_num, day=1)
    def add_months(sourcedate, months):
        import calendar
        month = sourcedate.month - 1 + months
        year = sourcedate.year + month / 12
        month = month % 12 + 1
        day = min(sourcedate.day,calendar.monthrange(year,month)[1])
        return datetime.datetime(year=year,month=month,day=1) # hardcoded 1 instead of `day` because I need first day of this month
    end_month = add_months(month_selected, 1) + datetime.timedelta(days=-1)
    data = {}
    data['menus'] = []
    # menu_set = Menu.objects.filter(school__place=place)
    place_obj = Place.objects.get(name=place)
    menus_in_place = Menu.objects.filter(available_in=place_obj)
    for menu in menus_in_place:
        closed_spots = Booking.objects.filter(
            place=place_obj,
            menu=menu,
            date__lt=end_month,
            date__gt=month_selected
        ).values(
            'id',
            'date'
        )
        data['menus'].append({
            'id': menu.id,
            'name': menu.name,
            'description': menu.description,
            'closedSpots': closed_spots
        })

    return JsonResponse(data)










