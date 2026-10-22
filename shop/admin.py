from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ["name"]}


@admin.register(Product)
class Product_admin(admin.ModelAdmin):
    list_display = [
        "name",
        "slug",
        "image",
        "price",
        "available",
        "created",
        "updated",
    ]
    list_filter = ["available", "created", "updated"]
    prepopulated_fields = {"slug": ["name"]}
    list_editable = ["available", "price"]
