from django.urls import path, include
from rest_framework import routers
from .views import ItemViewSet, CategoryViewSet, InventoryChangeViewSet


router = routers.DefaultRouter()
router.register(r'item', ItemViewSet, basename='item')
router.register(r'category', CategoryViewSet, basename='category')

urlpatterns = [
    path('items/<int:item_id>/inventory-changes/', InventoryChangeViewSet.as_view({'get': 'list'})),    
]

urlpatterns += router.urls