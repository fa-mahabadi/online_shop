from decimal import Decimal

from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from order.models import Order
from django.urls import reverse
from django.conf import settings
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_VERSION_API

def payment_process(request):
    order_id = request.session.get("order_id")
    order = get_object_or_404(Order, id=order_id)
    if request.method == "POST":
        cancel_url = request.build_absolute_uri(reverse("payment:canceled"))
        success_url = request.build_absolute_uri(reverse("payment:completed"))
        # STRIPE CHECKOUT SESSION DATA
        session_data = {
            "mode": "payment",
            "client_reference_id": order.id,
            "cancel_url": cancel_url,
            "success_url": success_url,
            "line_items": [],
        }
        # ADD ORDER ITEM TO SESSION
        for item in order.items.all():
            session_data["line_items"].append(
                {
                    "price_data": {
                        "currency": "usd",
                        "unit_amount": int(item.price * Decimal('100')),
                        "product_data": {"name": item.product.name},
                    },
                    "quantity": item.quantity,
                }
            )

        session = stripe.checkout.Session.create(**session_data)
        return redirect(session.url, code=303)
    return render(request, "payment/process.html", {"order": order})


def payment_canceled(request):
    return render(request,"payment/canceled.html")


def payment_completed(request):
    return render(request,"payment/completed.html")
