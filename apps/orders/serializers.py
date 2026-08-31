from rest_framework import serializers
from .models import Order, OrderItem
from apps.customers.models import Customer

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_sku = serializers.CharField(source='product.sku', read_only=True)

    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'product_name', 'product_sku', 'quantity', 'unit_price', 'subtotal')
        read_only_fields = ('unit_price', 'subtotal')

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    customer_name = serializers.CharField(source='customer.name', read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'order_number', 'customer', 'customer_name', 'status', 'total_amount', 'notes', 'created_at', 'items')
        read_only_fields = ('order_number', 'status', 'total_amount', 'created_at')

class OrderCreateItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

class OrderCreateSerializer(serializers.Serializer):
    """
    Used exclusively for accepting POST requests to create a new Order.
    We don't use ModelSerializer because we pass this data directly to the OrderService.
    """
    customer_id = serializers.IntegerField()
    notes = serializers.CharField(required=False, allow_blank=True)
    items = OrderCreateItemSerializer(many=True)

    def validate_customer_id(self, value):
        if not Customer.objects.filter(id=value).exists():
            raise serializers.ValidationError("Customer does not exist.")
        return value
