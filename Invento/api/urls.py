from django.urls import path, include
from rest_framework import routers
from .views import ItemViewSet, CategoryViewSet, InventoryChangeViewSet, SupplierViewSet, InventoryReportViewSet, StockLevelReportViewSet, TransactionHistoryViewSet

router = routers.DefaultRouter()
router.register(r'item', ItemViewSet, basename='item')
router.register(r'category', CategoryViewSet, basename='category')
router.register(r'supplier', SupplierViewSet, basename='supplier')
router.register(r'inventory_reports', InventoryReportViewSet, basename='inventory_reports')
router.register(r'stock_levels', StockLevelReportViewSet, basename='stock_levels')
router.register(r'transaction', TransactionHistoryViewSet, basename='transaction')
urlpatterns = [
    path('items/<int:item_id>/inventory-changes/', InventoryChangeViewSet.as_view({'get': 'list'})),    
]

urlpatterns += router.urls