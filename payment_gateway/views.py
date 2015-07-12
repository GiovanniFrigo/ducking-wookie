from django.contrib.auth import get_user_model
from django.shortcuts import render
import braintree
from django.http.response import HttpResponseBadRequest, JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from core.models import Booking, Place, Menu
import datetime
from core.views import get_availability_count


@csrf_exempt
# Create your views here.
def generate_token(request):
    token = braintree.ClientToken.generate()

    return JsonResponse({"token": token})


@csrf_exempt
def post_payment(request):
    if request.POST.get("payment_method_nonce") is None:
        return HttpResponseBadRequest()

    nonce = request.POST.get("payment_method_nonce")

    try:
        # received_json_data=json.loads(request.body)
        place = Place.objects.get(name__iexact=request.POST.get("place"))
        user, created = get_user_model().objects.get_or_create(email=request.POST.get('email'), username=request.POST.get('email'))
        menu = Menu.objects.get(id=int(request.POST.get('menu_id')))
        n_people = int(request.POST.get('n_people'))
        date_meal = datetime.datetime(int(request.POST.get('year')), int(request.POST.get('month')), int(request.POST.get('day')))
        if get_availability_count(date_meal, menu, place) > 0:
            booking = Booking.objects.create(user=user, place=place, guest_number=n_people, menu=menu, date=date_meal)
        else:
            return HttpResponseBadRequest("no booking availability here...")
    except KeyError as ke:
        return HttpResponseBadRequest(ke)
    except Exception as ex:
        return HttpResponseBadRequest(ex)

    created_booking = Booking.objects.get(id=booking.id)
    result = braintree.Transaction.sale({
        "amount": "%s" % str(created_booking.menu.price_per_person*created_booking.guest_number),  #"10.00",
        "payment_method_nonce": nonce
    })

    if result.is_success:
        created_booking.transaction_id = result.transaction.id
        created_booking.save()
        return JsonResponse({"status": "success!"})
    elif result.transaction:
        return HttpResponse("\nError processing transaction:" +
                            "\n  code: " + result.transaction.processor_response_code +
                            "\n  text: " + result.transaction.processor_response_text)
    else:
        errors = ""
        for error in result.errors.deep_errors:
            errors = errors + "\nattribute: " + error.attribute + \
                                "\n  code: " + error.code + \
                                "\n  message: " + error.message
        return HttpResponse("result: %s // res.err: %s // error: %s" % (str(result), str(result.errors), errors,))
