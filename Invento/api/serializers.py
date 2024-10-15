from rest_framework  import serializers
from store.models import Item, Category

class ItemSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'quantity', 'price', 'category_name']

    def get_category_name(self, obj):
        return obj.category.name


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'creator']