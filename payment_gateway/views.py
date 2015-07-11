from django.shortcuts import render
import braintree
from django.http.response import HttpResponseBadRequest, HttpResponse

# Create your views here.
def generate_token(request):
    braintree.Configuration.configure(
        braintree.Environment.Sandbox,
        '7k9mcqvpy3bzn5c7',
        'rfyzzc5ftvxwkdmm',
        'af2678c533f0174b2837c844e303de02'
    )

    return braintree.ClientToken.generate()


def post_payment(request):
    if "payment_method_nonce" not in request.forms:
        return HttpResponseBadRequest()

    nonce = request.form["payment_method_nonce"]

    result = braintree.Transaction.sale({
        "amount": "10.00",
        "payment_method_nonce": nonce
    })

    if result.is_success:
        return HttpResponse("success!: " + result.transaction.id)
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
        return HttpResponse(errors)
