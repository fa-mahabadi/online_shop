from django.shortcuts import redirect, render
from .forms import OrderForm
from cart.cart import Cart
from .models import Order,OrderItem
from .tasks import order_created

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
