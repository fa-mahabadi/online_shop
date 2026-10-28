from celery import shared_task
from django.core.mail import send_mail
from order.models import Order

@shared_task
def order_created(order_id):
    order=Order.objects.get(id=order_id)
    subject=f'order no.{order.id}'
    message=(f'Dear, {order.first_name}'
    f'\n order placed successfully on order'
    f'\n your order id is {order.id}')
    mail_send=send_mail(subject,message,'admin@email.com',[order.email])
    return mail_send