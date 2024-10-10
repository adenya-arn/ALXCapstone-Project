from django.urls import path, include
from rest_framework import routers
from .views import ItemViewset, CategoryViewset


router = routers.DefaultRouter()
router.register(r'item', ItemViewset, basename='item')
router.register(r'category', CategoryViewset, basename='category')

urlpatterns = [
    path('', include(router.urls)),
]