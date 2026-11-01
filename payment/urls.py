from django.urls import path
from . import views
from .webhooks import stripe_webhook

app_name="payment"
urlpatterns=[
    path("completed/",views.payment_completed,name="completed"),
    path("canceled/",views.payment_canceled,name="canceled"),
    path("process/",views.payment_process,name="process"),
    path("webhook/",stripe_webhook,name='stripe_webhook'),
]