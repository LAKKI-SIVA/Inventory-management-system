import uuid
from django.db import transaction
from django.core.exceptions import ValidationError
from apps.products.models import Product
from apps.inventory.services import InventoryService
from apps.inventory.models import Stock
from .models import Order, OrderItem

class OrderService:
    """
    Service layer for Order business logic.
    Handles complex cross-module communication (Orders -> Inventory).
    """

    @staticmethod
    def generate_order_number() -> str:
        # Generate a unique string like ORD-8f7d9a
        return f"ORD-{uuid.uuid4().hex[:6].upper()}"

    @staticmethod
    @transaction.atomic
    def create_order(customer_id: int, items_data: list, notes: str = "") -> Order:
        """
        items_data should be a list of dicts: [{'product_id': 1, 'quantity': 2}, ...]
        """
        if not items_data:
            raise ValidationError("An order must contain at least one item.")

        # 1. Create the Order Header
        order = Order.objects.create(
            order_number=OrderService.generate_order_number(),
            customer_id=customer_id,
            notes=notes,
            status=Order.Status.PENDING
        )

        total_amount = 0

        # 2. Process each item
        for item in items_data:
            product_id = item.get('product_id')
            quantity = item.get('quantity')

            if quantity <= 0:
                raise ValidationError("Quantity must be greater than zero.")

            # Get the product
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                raise ValidationError(f"Product ID {product_id} does not exist.")

            # Create OrderItem
            order_item = OrderItem(
                order=order,
                product=product,
                quantity=quantity,
                unit_price=product.price
            )
            order_item.save() # This triggers the save() method which calculates the subtotal

            total_amount += order_item.subtotal

            # 3. INTER-MODULE COMMUNICATION: Reserve the inventory!
            # We get the Stock for this product and call the InventoryService
            try:
                stock = Stock.objects.get(product=product)
                InventoryService.reserve_stock(stock, quantity)
            except Stock.DoesNotExist:
                raise ValidationError(f"No stock record found for product {product.name}.")
            except ValidationError as e:
                # If InventoryService raises an error (e.g. not enough stock), we re-raise it
                raise ValidationError(f"Error reserving stock for {product.name}: {str(e)}")

        # 4. Update the Order Header with the final total
        order.total_amount = total_amount
        order.save()

        return order

    @staticmethod
    @transaction.atomic
    def process_order(order: Order, user=None):
        """
        Moves order from PENDING -> SHIPPED.
        This removes the reserved stock and permanently adjusts the total stock OUT.
        """
        if order.status != Order.Status.PENDING and order.status != Order.Status.CONFIRMED:
            raise ValidationError("Only pending or confirmed orders can be processed for shipping.")

        for item in order.items.all():
            stock = item.product.stock
            
            # 1. Release the mathematical hold
            InventoryService.release_reserved_stock(stock, item.quantity)
            
            # 2. Permanently remove the physical stock from the warehouse
            InventoryService.adjust_stock(
                stock=stock,
                quantity_change=-item.quantity, # Negative because we are shipping it OUT
                transaction_type='OUT',
                user=user,
                reference_number=order.order_number,
                notes="Shipped to customer"
            )

        order.status = Order.Status.SHIPPED
        order.save()
