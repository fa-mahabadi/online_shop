from decimal import Decimal

from django.db import models
from shop.models import Product
from django.conf import settings
from coupon.models import Coupon
from django.core.validators import MaxValueValidator,MinValueValidator
class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    stripe_id=models.CharField(max_length=250,blank=True)
    coupon=models.ForeignKey(Coupon,related_name="orders",on_delete=models.SET_NULL,blank=True,null=True)
    discount=models.IntegerField(default=0,validators=[MinValueValidator(0),MaxValueValidator(100)])

    def __str__(self) -> str:
        return f"{self.first_name} - {self.last_name}"

    def get_stripe_url(self):
        if not self.stripe_id:
            return ''
        if '__test__' in settings.STRIPE_SECRET_KEY:
            path= '/test/'
        else:
            path="/"
        return f'https://dashboard.stripe.com{path}payments/{self.id}'

    def get_total_cost_before_discount(self):
        return sum(item.get_cost()for item in self.items.all )

    def get_discount(self):
        if self.discount:
            return self.get_total_cost_before_discount()*(self.discount/Decimal(100))
        return Decimal(0)

    def get_total_cost(self):
        return self.get_total_cost_before_discount()-self.get_discount()

    class Meta:
        ordering = ["-created"]
        indexes = [models.Index(fields=["created"])]


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order_item")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self) -> str:
        return str(self.id)

    def get_cost(self):
        return self.quantity * self.price
