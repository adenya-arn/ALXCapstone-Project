from django.shortcuts import render, get_object_or_404
from store.models import Item, Category, InventoryChange
from .serializers import ItemSerializer, CategorySerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
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

  
