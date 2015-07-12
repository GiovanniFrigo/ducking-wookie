import datetime
from django.contrib.auth import get_user_model
from django.http.response import Http404, HttpResponseBadRequest
from django.shortcuts import render
import json
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from models import Booking, Menu, Place


def menu_place(request, place):
    place_obj = Place.objects.get(name__iexact=place)
    menu_list = []
    for listitem in list(Menu.objects.filter(available_in=place_obj).values()):
        listitem['photo'] = Menu.objects.get(id=listitem['id']).photo.url
        menu_list.append(listitem)
    menu_dict = {'menus': menu_list}

    return JsonResponse(menu_dict)

def add_months(sourcedate, months):
    import calendar
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month / 12
    month = month % 12 + 1
    day = min(sourcedate.day,calendar.monthrange(year,month)[1])
    return datetime.datetime(year=year,month=month,day=1) # hardcoded 1 instead of `day` because I need first day of this month

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

    end_month = add_months(month_selected, 1) + datetime.timedelta(days=-1)
    data = {'menus': []}
    place_obj = Place.objects.get(name__iexact=place)
    menus_in_place = Menu.objects.filter(available_in=place_obj)
    for menu in menus_in_place:
        closed_spots = list(
            Booking.objects.filter(
                place=place_obj,
                menu=menu,
                date__lt=end_month,
                date__gt=month_selected
            ).values(
                'id',
                'date'
            )
        )
        data['menus'].append({
            'id': menu.id,
            'name': menu.name,
            'description': menu.description,
            'closedSpots': closed_spots
        })

    return JsonResponse(data)


def get_availability_count(date, menu, place_obj):
    daily_booking_count = Booking.objects.filter(
        place=place_obj,
        menu=menu,
        date__gte=date,
        date__lt=date + datetime.timedelta(days=1) - datetime.timedelta(
            seconds=1)
    ).count()
    return menu.available_number_per_day - daily_booking_count

def free_spots(date, place_obj):
    menus_in_place = Menu.objects.filter(available_in=place_obj)
    result = {}
    for menu in menus_in_place:
        result['%s' % menu.id] = get_availability_count(date, menu, place_obj)
    return result


def menu_place_not_booked(request, place, year, month):
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
        'jan': 1,
        'feb': 2,
        'mar': 3,
        'apr': 4,
        'may': 5,
        'jun': 6,
        'jul': 7,
        'aug': 8,
        'sep': 9,
        'oct': 10,
        'nov': 11,
        'dec': 12
    }
    if month not in months:
        raise Http404()
    place_obj = Place.objects.get(name__iexact=place)

    month_num = months_dict[month]
    year = int(year)
    month_selected = datetime.datetime(year=year, month=month_num, day=1)

    end_month = add_months(month_selected, 1) + datetime.timedelta(days=-1)
    delta = end_month - month_selected
    calendar = {'calendar': {}}
    from calendar import monthrange
    num_of_days = monthrange(year, month_num)[1]
    # for i in range(delta.days):
    for i in range(1, num_of_days+1):
        working_date = month_selected.replace(
            year=month_selected.year,
            month=month_selected.month,
            day=i
        )
        calendar['calendar']['%s' % i] = free_spots(working_date, place_obj)

    return JsonResponse(calendar)


class BookCBV(View):
    """
    Anything different from POST will be served a 405 error.
    """
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(BookCBV, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        try:
            received_json_data=json.loads(request.body)
            place = Place.objects.get(name__iexact=received_json_data['place'])
            user, created = get_user_model().objects.get_or_create(email=received_json_data['email'], username=received_json_data['email'])
            menu = Menu.objects.get(id=int(received_json_data['menu_id']))
            n_people = int(received_json_data['n_people'])
            date_meal = datetime.datetime(received_json_data['year'], received_json_data['month'], received_json_data['day'])
            if get_availability_count(date_meal, menu, place) > 0:
                booking = Booking.objects.create(user=user, place=place, guest_number=n_people, menu=menu, date=date_meal)
                return JsonResponse({'booking_id': booking.id})
            else:
                return HttpResponseBadRequest("no booking availability here...")
        except KeyError as ke:
            return HttpResponseBadRequest(ke)
        except Exception as ex:
            return HttpResponseBadRequest(ex)
