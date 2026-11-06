from celery import shared_task
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.contrib.staticfiles import finders
from order.models import Order
from io import BytesIO
import weasyprint

@shared_task
def payment_complete(order_id):
    order=get_object_or_404(Order,id=order_id)
    subject=f'My shop- Invoice no.{order_id}'
    message=('Please, find invoice attachment for your purchese ')
    email=EmailMessage(subject,message,'admin@email.com',[order.email])
    html=render_to_string('order/pdf.html',{"order":order})
    out=BytesIO()
    stylesheets=[weasyprint.CSS(finders.find("css/pdf.css"))]
    weasyprint.HTML(string=html).write_pdf(out,stylesheets=stylesheets)
    email.attach(f'order_{order_id.pdf}',out.getvalue(),'application/pdf')
    email.send()