from django.shortcuts import render, get_object_or_404
from store.models import Item, Category
from .serializers import ItemSerializer, CategorySerializer
from rest_framework import viewsets, status
from rest_framework.response import Response

# Create your views here.

class CategoryViewSet(viewsets.ViewSet):

    #This is used to list everything in the category model
    def list(self, request):
        queryset = Category.objects.all()
        serializer = CategorySerializer(queryset, many=True)

        return Response (serializer.data)


    def create(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(queryset)

        return Response(serializer.data)

    def update(self, request, pk=None):
        queryset = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        queryset = get_object_or_404(Category, pk=pk)
        queryset.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    


class ItemViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Item.objects.all()
        serializer = ItemSerializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        queryset = get_object_or_404(Item, pk=pk)
        serializer = ItemSerializer(queryset)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        queryset = get_object_or_404(Item, pk=pk)
        serializer = ItemSerializer(queryset, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        queryset = get_object_or_404(Item, pk=pk)
        queryset.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryViewset1(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class ItemViewset1(viewsets.ModelViewSet):
    serializer_class = ItemSerializer 
    queryset =  Item.objects.all()  
