from django.shortcuts import render, redirect
import stripe
from django.conf import settings
from django.http import JsonResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
# Create your views here.
stripe.api_key = settings.STRIPE_SECRET_KEY

# @csrf_exempt
# def make_payment(request):
#     try:
#         # Retrieve the payment method details from the client
#         payment_method_id = request.POST.get('paymentMethodId')
#         amount = 1000  # Set your product price here (in cents)
#         customer_id = request.POST.get('customerId')

#         # Create or update a customer with the payment method
#         customer = stripe.Customer.create(
#             payment_method=payment_method_id,
#             email='customer@example.com',
#             invoice_settings={
#                 'default_payment_method': payment_method_id,
#             },
#         )

#         # Save the customer ID for future use (e.g., repurchases)
#         if customer_id:
#             stripe.Customer.modify(customer_id, default_payment_method=payment_method_id)

#         # Create a payment intent
#         payment_intent = stripe.PaymentIntent.create(
#             amount=amount,
#             currency='usd',
#             customer=customer.id,
#             confirmation_method='manual',
#             confirm=True,
#         )

#         return JsonResponse({'clientSecret': payment_intent.client_secret})

#     except stripe.error.StripeError as e:
#         return JsonResponse({'error': str(e)})



# def retrieve_cards(request):
#     try:
#         customer_id = request.POST.get('customerId')
        
#         # Retrieve the customer from Stripe
#         customer = stripe.Customer.retrieve(customer_id)
        
#         # Retrieve the list of payment methods for the customer
#         cards = stripe.PaymentMethod.list(
#             customer=customer_id,
#             type='card'
#         )
        
#         # Extract relevant details from the cards
#         saved_cards = [
#             {
#                 'id': card.id,
#                 'brand': card.card.brand,
#                 'last4': card.card.last4,
#             }
#             for card in cards.data
#         ]
        
#         return JsonResponse({'cards': saved_cards})
    
#     except stripe.error.StripeError as e:
#         return JsonResponse({'error': str(e)})



@login_required
def purchase_product(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        customer = Customer.objects.get(user=request.user)
        payment_method_id = request.POST.get('payment_method_id')


        if payment_method_id == 'new_card':
            return redirect('add_payment_method')

        try:
            # Create a payment intent
            intent = stripe.PaymentIntent.create(
                amount=1000,  # Amount in cents
                currency='usd',
                customer=customer.stripe_customer_id,
                payment_method=payment_method_id,
                off_session=True,
                confirm=True,
            )

            # Process the payment

            # If the payment is successful, perform any necessary actions here

            return JsonResponse({"message":"Purchase successfully"})

        except stripe.error.CardError as e:
            # Handle card error
            pass
        except stripe.error.InvalidRequestError as e:
            # Handle invalid request
            pass
        except stripe.error.AuthenticationError as e:
            # Handle authentication error
            pass
        except stripe.error.APIConnectionError as e:
            # Handle API connection error
            pass
        except stripe.error.StripeError as e:
            # Handle other Stripe errors
            pass

    customer = Customer.objects.get(user=request.user)
    payment_methods = PaymentMethod.objects.filter(customer=customer)

    return render(request, 'purchase.html',  {'payment_methods': payment_methods})

@login_required
def manage_payment_methods(request):
    customer = Customer.objects.get(user=request.user)
    payment_methods = PaymentMethod.objects.filter(customer=customer)

    return render(request, 'payment_methods.html', {'payment_methods': payment_methods})



@login_required
def add_payment_method(request):
    if request.method == 'POST':
        customer = Customer.objects.get(user=request.user)

        print(request.POST)
        payid = request.POST.get('payment_method_id')
        last4 = request.POST.get('card_last')
        month = request.POST.get('card_exp_month')
        year = request.POST.get('card_exp_year')
        try:

            # Save the payment method details to the database
            payment = PaymentMethod(
                customer=customer,
                stripe_payment_method_id=payid,
                last4=last4,
                exp_month=month,
                exp_year=year
            )
            print(payment)
            payment.save()
            return redirect('manage_payment_methods')  # Redirect to the payment methods page

        except stripe.error.CardError as e:
            print("card error")
            print(e)
        except stripe.error.InvalidRequestError as e:
            print("requets error")
            print(e)
        except stripe.error.AuthenticationError as e:
            print("auth error")
            print(e)
        except stripe.error.APIConnectionError as e:
            print("api error")
            print(e)
        except stripe.error.StripeError as e:
            print("stripe error")
            print(e)

    return render(request, 'add_payment_method.html')