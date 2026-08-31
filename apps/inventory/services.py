from django.db import transaction
from django.core.exceptions import ValidationError
from .models import Stock, StockTransaction
from apps.products.models import Product

class InventoryService:
    """
    Service layer for managing inventory.
    We NEVER modify stock directly in a view. We always use this service 
    to ensure the ledger (StockTransaction) stays perfectly in sync with the current Stock.
    """

    @staticmethod
    def initialize_stock(product: Product) -> Stock:
        """Called automatically when a new product is created."""
        stock, created = Stock.objects.get_or_create(product=product)
        return stock

    @staticmethod
    @transaction.atomic
    def adjust_stock(stock: Stock, quantity_change: int, transaction_type: str, user=None, reference_number: str = "", notes: str = "") -> StockTransaction:
        """
        The core engine for inventory movement. 
        Uses @transaction.atomic so if any part fails, the entire database action rolls back!
        """
        if quantity_change == 0:
            raise ValidationError("Quantity change cannot be zero.")

        # Calculate new total
        new_quantity = stock.quantity + quantity_change

        # Enforce business rule: No negative stock
        if new_quantity < 0:
            raise ValidationError(f"Insufficient stock for {stock.product.name}. Cannot reduce by {abs(quantity_change)}.")

        # 1. Update the Stock model
        stock.quantity = new_quantity
        stock.full_clean() # Runs the clean() method on the model to double-check constraints
        stock.save()

        # 2. Record the ledger entry
        transaction_record = StockTransaction.objects.create(
            stock=stock,
            transaction_type=transaction_type,
            quantity=quantity_change,
            reference_number=reference_number,
            notes=notes,
            created_by=user
        )

        return transaction_record

    @staticmethod
    @transaction.atomic
    def reserve_stock(stock: Stock, quantity_to_reserve: int):
        """Called when a customer places an order but it hasn't shipped yet."""
        if quantity_to_reserve <= 0:
            raise ValidationError("Reserve quantity must be positive.")
            
        if stock.available_quantity < quantity_to_reserve:
            raise ValidationError(f"Not enough available stock to reserve {quantity_to_reserve} units.")

        stock.reserved_quantity += quantity_to_reserve
        stock.save()

    @staticmethod
    @transaction.atomic
    def release_reserved_stock(stock: Stock, quantity_to_release: int):
        """Called if a customer cancels their order before it ships."""
        if stock.reserved_quantity < quantity_to_release:
            raise ValidationError("Cannot release more stock than is currently reserved.")
            
        stock.reserved_quantity -= quantity_to_release
        stock.save()
