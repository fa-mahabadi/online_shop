import os

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.admin.views.decorators import staff_member_required

from django.conf import settings
from .forms import OrderForm
from cart.cart import Cart
from .models import Order,OrderItem
from .tasks import order_created
from django.template.loader import render_to_string
from django.contrib.staticfiles import finders
import weasyprint
def order_create(request):
    cart=Cart(request)
    if request.method=="POST":
        form=OrderForm(request.POST)
        if form.is_valid():
            order=form.save()
            for item in cart:
                OrderItem.objects.create(order=order,product=item['product'],price=item['price'],quantity=item['quantity'])
            cart.clear()
            order_created.delay(order.id)
            request.session['order_id']=order.id
            return redirect("payment:process")
    else:    
        form=OrderForm()
        return render(request,"order/create.html",{"form":form,"cart":cart})

    
@staff_member_required
def admin_order_detail(request,order_id):
    order=get_object_or_404(Order,id=order_id)
    return render(request,"order/detail.html",{"order":order})

@staff_member_required
def admin_order_pdf(request,order_id):
    order=get_object_or_404(Order,id=order_id)
    html=render_to_string("order/pdf.html",{"order":order})
    response=HttpResponse(content_type="application/pdf")
    response["Content-Disposition"]=f'filename=order_{order.id}'
    weasyprint.HTML(string=html).write_pdf(response,stylesheets=[weasyprint.CSS(finders.find('css/pdf.css'))])
    return response

