from django.urls import path, include
from rest_framework import routers
from .views import ItemViewSet, CategoryViewSet


router = routers.DefaultRouter()
router.register(r'item', ItemViewSet, basename='item')
router.register(r'category', CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
]