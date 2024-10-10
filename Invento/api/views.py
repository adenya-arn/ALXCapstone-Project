from django.shortcuts import render
from store.models import Item, Category
from .serializers import ItemSerializer, CategorySerializer
from rest_framework import viewsets


# Create your views here.

class CategoryViewset(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class ItemViewset(viewsets.ModelViewSet):
    serializer_class = ItemSerializer 
    queryset =  Item.objects.all()  
