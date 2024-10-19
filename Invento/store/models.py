from django.db import models
from django.conf import settings
# Create your models here.

class Supplier(models.Model):
    name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    contact = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name} -- {self.contact}/{self.email}'


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    quantity = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits = 12, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='category')
    date_added = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True)
    threshold = models.PositiveIntegerField(default=10)

    def is_below_minimum(self):
        return self.quantity < self.threshold
    
    def total_value(self):
        return self.price * self.quantity

    def __str__(self):
        return f'{self.name}/n - {self.price} - {self.quantity} in {self.category}'
    

def get_total_inventory_value():
    return sum(item.total_value() for item in Item.objects.all())



class InventoryChange(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    change_quantity = models.DecimalField(max_digits=6, decimal_places=2)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_changed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Change of {self.change_quantity} for {self.item.name} by {self.user.username} on {self.date_changed}'


class Transaction(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    transaction_type = models.CharField(max_length=10, choices=[('sale', 'Sale'), ('restock', 'Restock')])
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.item} -- {self.quantity} -- {self.transaction_type} -- {self.date}'
    
def get_inventory_report():
    sales = Transaction.objects.filter(transaction_type='sale')
    restocks = Transaction.objects.filter(transaction_type='restock')