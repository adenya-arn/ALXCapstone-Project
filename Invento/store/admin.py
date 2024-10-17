from django.contrib import admin
from .models import Category, Item, InventoryChange, Supplier

# Register your models here.

admin.site.register(Category)
admin.site.register(Item)
admin.site.register(InventoryChange)
admin.site.register(Supplier)