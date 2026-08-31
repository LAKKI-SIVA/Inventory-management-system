from django.db import models
from django.core.exceptions import ValidationError
from apps.products.models import Product
from django.conf import settings

class Stock(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='stock')
    quantity = models.PositiveIntegerField(default=0)
    reserved_quantity = models.PositiveIntegerField(default=0)
    reorder_level = models.PositiveIntegerField(default=10)

    class Meta:
        db_table = 'inventory_stock'

    def __str__(self):
        return f"{self.product.name} (Available: {self.available_quantity})"

    @property
    def available_quantity(self):
        """
        Available stock is total quantity minus what has been reserved for pending orders.
        """
        return self.quantity - self.reserved_quantity

    def clean(self):
        # Database-level constraint: Stock can never be negative
        if self.quantity < 0:
            raise ValidationError("Stock quantity cannot be negative.")
        if self.reserved_quantity > self.quantity:
            raise ValidationError("Reserved quantity cannot exceed total stock quantity.")


class StockTransaction(models.Model):
    class TransactionType(models.TextChoices):
        IN = 'IN', 'Stock In'
        OUT = 'OUT', 'Stock Out'
        ADJUSTMENT = 'ADJUSTMENT', 'Adjustment'

    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TransactionType.choices)
    quantity = models.IntegerField(help_text="Can be negative for OUT/ADJUSTMENT")
    reference_number = models.CharField(max_length=100, blank=True, help_text="Order ID or PO Number")
    notes = models.TextField(blank=True)
    
    # Track who made the transaction!
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'inventory_transactions'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.transaction_type} ({self.quantity}) for {self.stock.product.name}"
