from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model.
    It translates complex Database Objects into clean JSON for the API.
    """
    category_name = serializers.CharField(source='category.name', read_only=True)
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)

    class Meta:
        model = Product
        fields = (
            'id', 'sku', 'name', 'description', 'price', 
            'category', 'category_name', 
            'supplier', 'supplier_name', 
            'status', 'image', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')
