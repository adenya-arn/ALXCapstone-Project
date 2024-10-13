from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

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

    def __str__(self):
        return f'{self.name}/n - {self.price} - {self.quantity} in {self.category}'