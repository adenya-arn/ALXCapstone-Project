from django.shortcuts import render, get_object_or_404
from store.models import Item, Category, InventoryChange, Supplier, Transaction
from .serializers import ItemSerializer, CategorySerializer, SupplierSerializer, TransactionSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from django.db.models import F
# Create your views here.

class CategoryViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    #This is used to list everything in the category model
    def list(self, request):
        queryset = Category.objects.all()
        serializer = CategorySerializer(queryset, many=True)

        return Response (serializer.data, status=status.HTTP_200_OK)


    def create(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(creator=request.user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(queryset)

        return Response(serializer.data)

    def update(self, request, pk=None):
        queryset = get_object_or_404(Category, pk=pk)
        self.check_object_permissions(request, queryset)
        serializer = CategorySerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        queryset = get_object_or_404(Category, pk=pk)
        self.check_object_permissions(request, queryset)
        queryset.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    


class ItemViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def list(self, request):
        queryset = Item.objects.all()

        #Filtering by category
        category_id = request.query_params.get('category', None)
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        #Filtering by price range
        min_price = request.query_params.get('min_price', None)
        max_price = request.query_params.get("max_price", None)
        if min_price and max_price:
            queryset =queryset.filter(price__gte=min_price, price__lte=max_price)
        elif min_price:
            queryset = queryset.filter(price__gte=min_price)
        elif max_price:
            queryset = queryset.filter(price__lte=max_price)

        #Filtering by lowstock
        low_stock = request.query_params.get('low_stock', None)
        if low_stock:
            queryset = queryset.filter(quantity__lt=low_stock)

        # Ordering
        ordering = request.query_params.get('ordering', 'name')
        if ordering.startswith('-'):
            queryset = queryset.order_by(ordering)  # Sort by descending if '-' is in the parameter
        else:
            queryset = queryset.order_by(ordering)  # Sort by ascending by default

        # Pagination
        paginator = PageNumberPagination()
        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            serializer = ItemSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)


        #Serializer
        serializer = ItemSerializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        queryset = get_object_or_404(Item, pk=pk)
        serializer = ItemSerializer(queryset)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            item = serializer.save(creator=request.user)
            InventoryChange.objects.create(item=item, change_quantity=item.quantity, user=request.user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        queryset = get_object_or_404(Item, pk=pk)
        previous_quantity = queryset.quantity
        self.check_object_permissions(request, queryset)

        serializer = ItemSerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid():
            updated = serializer.save()
            quantity_change = updated.quantity - previous_quantity
            InventoryChange.objects.create(item=updated, change_quantity=quantity_change, user=request.user)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        queryset = get_object_or_404(Item, pk=pk)
        self.check_object_permissions(request, queryset)
        queryset.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class InventoryChangeViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, item_id=None):
        queryset = get_object_or_404(Item, pk=item_id)
        changes = queryset.inventory_changes.all()
        change_data = []
        for change in changes:
            change_data.append({
                'change_quantity': change.change_quantity,
                'user': change.user.username,
                'date_changed': change.date_changed,
            })
        return Response(change_data, status=status.HTTP_200_OK)

  
class SupplierViewSet(viewsets.ModelViewSet):
    serializer_class = SupplierSerializer
    queryset = Supplier.objects.all()
    permission_classes = [IsAuthenticated]


class InventoryReportViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='total_inventory_value')
    def total_inventory_value(self, request):
        total_value = sum(item.total_value() for item in Item.objects.all())
        return Response({"total_inventory_value": total_value})

class StockLevelReportViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        low_stock = request.query_params.get('low_stock', None)
        if low_stock == 'true':
            items = Item.objects.filter(quantity__lt=F('threshold'))
        else:
            items = Item.objects.all()

        stock_data = [{"name": item.name, "quantity": item.quantity, "threshold": item.threshold} for item in items]
        return Response(stock_data)

class TransactionHistoryViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        sales = Transaction.objects.filter(transaction_type='sale')
        restocks = Transaction.objects.filter(transaction_type='restock')

        sales_data = [{"item": sale.item.name, "quantity": sale.quantity, "date": sale.date} for sale in sales]
        restock_data = [{"item": restock.item.name, "quantity": restock.quantity, "date": restock.date} for restock in restocks]

        return Response({
            "sales": sales_data,
            "restocks": restock_data
        })
    
    def retrieve(self, request, pk=None):
        try:
            transaction = Transaction.objects.get(pk=pk)
            serializer = TransactionSerializer(transaction)
            return Response(serializer.data)
        except Transaction.DoesNotExist:
            return Response({"detail": "Transaction not found."}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            transaction = Transaction.objects.get(pk=pk)
            serializer = TransactionSerializer(transaction, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Transaction.DoesNotExist:
            return Response({"detail": "Transaction not found."}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            transaction = Transaction.objects.get(pk=pk)
            transaction.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Transaction.DoesNotExist:
            return Response({"detail": "Transaction not found."}, status=status.HTTP_404_NOT_FOUND)
