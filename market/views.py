from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.conf import settings
from .models import Order, OrderItem, Product
import json
import requests


def send_telegram_message(order):
    """Telegram channel ga buyurtma xabari yuborish"""
    try:
        bot_token = settings.TELEGRAM_BOT_TOKEN
        channel_id = settings.TELEGRAM_CHANNEL_ID
        
        items_text = ''
        for item in order.items.all():
            items_text += f"  • {item.product_name} x{item.quantity} = ${item.subtotal}\n"
        
        message = (
            f"🛍️ Yangi buyurtma berildi!\n\n"
            f"📋 Buyurtma ID: #{order.id}\n"
            f"👤 Mijoz: {order.customer_name}\n"
            f"📧 Email: {order.customer_email}\n"
            f"📍 Manzil: {order.customer_address}\n\n"
            f"🛒 Mahsulotlar:\n{items_text}\n"
            f"💰 Jami: ${order.total_price}"
        )
        
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = {
            "chat_id": channel_id,
            "text": message,
            "parse_mode": "HTML"
        }
        
        requests.post(url, json=data)
    except Exception as e:
        print(f"Telegram xabar yuborishda xato: {e}")


def home(request):
    products = Product.objects.filter(available=True)
    return render(request, 'market/home.html', {'products': products})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    return render(request, 'market/product_detail.html', {'product': product})


def cart(request):
    return render(request, 'market/cart.html')


def about(request):
    return render(request, 'market/about.html')


def checkout(request):
    if request.method == 'POST':
        cart_data = request.POST.get('cart_data', '')
        customer_name = request.POST.get('customer_name', '').strip()
        customer_email = request.POST.get('customer_email', '').strip()
        customer_address = request.POST.get('customer_address', '').strip()
        
        errors = []
        if not customer_name:
            errors.append('Ismingizni kiriting.')
        if not customer_email:
            errors.append('Elektron pochta manzilingizni kiriting.')
        if not customer_address:
            errors.append('Manzilingizni kiriting.')

        try:
            cart_items = json.loads(cart_data or '[]')
        except json.JSONDecodeError:
            cart_items = []

        if not cart_items:
            errors.append('Savatchada hech qanday mahsulot yo‘q.')

        if errors:
            return render(request, 'market/checkout.html', {
                'errors': errors,
                'customer_name': customer_name,
                'customer_email': customer_email,
                'customer_address': customer_address,
            })

        total_price = sum((float(item.get('price', 0)) * int(item.get('quantity', 1))) for item in cart_items)
        order = Order.objects.create(
            customer_name=customer_name,
            customer_email=customer_email,
            customer_address=customer_address,
            total_price=total_price,
        )
        for item in cart_items:
            quantity = int(item.get('quantity', 1))
            price = float(item.get('price', 0))
            subtotal = quantity * price
            OrderItem.objects.create(
                order=order,
                product_name=item.get('name', 'Mahsulot'),
                price=price,
                quantity=quantity,
                subtotal=subtotal,
            )
        
        send_telegram_message(order)
        
        return redirect(reverse('market:order_complete', args=[order.id]))

    return render(request, 'market/checkout.html')


def order_complete(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'market/order_complete.html', {'order': order})
