from rest_framework import serializers
from .models import Stock, StockTransaction

class StockSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_sku = serializers.CharField(source='product.sku', read_only=True)
    available_quantity = serializers.IntegerField(read_only=True)

    class Meta:
        model = Stock
        fields = ('id', 'product', 'product_name', 'product_sku', 'quantity', 'reserved_quantity', 'available_quantity', 'reorder_level')
        read_only_fields = ('quantity', 'reserved_quantity') # API users cannot edit stock directly!

class StockAdjustSerializer(serializers.Serializer):
    """
    Used exclusively for the API endpoint where users post a stock adjustment.
    """
    transaction_type = serializers.ChoiceField(choices=StockTransaction.TransactionType.choices)
    quantity = serializers.IntegerField()
    reference_number = serializers.CharField(max_length=100, required=False, allow_blank=True)
    notes = serializers.CharField(required=False, allow_blank=True)
