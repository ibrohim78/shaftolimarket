import stripe
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from market.models import Order
from django.urls import reverse

# Stripe maxfiy kalitini sozlash
stripe.api_key = settings.STRIPE_SECRET_KEY

def create_test_checkout_session(request, order_id):
    """
    Haqiqiy buyurtma uchun Stripe to'lov sessiyasini yaratish.
    """
    try:
        order = get_object_or_404(Order, id=order_id)
        # Oddiy test mahsuloti bilan sessiya yaratish
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': f"Buyurtma #{order.id}",
                        },
                        'unit_amount': int(order.total_price * 100),  # Sentlarda ($1 = 100 sent)
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=request.build_absolute_uri(reverse('market:order_complete', args=[order.id])),
            cancel_url=request.build_absolute_uri(reverse('market:home')),
        )
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)