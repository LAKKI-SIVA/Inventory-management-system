import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import StockTransaction

logger = logging.getLogger('inventory')

@receiver(post_save, sender=StockTransaction)
def log_stock_transaction(sender, instance, created, **kwargs):
    """
    Demonstrates decoupling and backend quality by automatically logging
    inventory changes when a StockTransaction is saved.
    """
    if created:
        logger.info(
            f"INVENTORY ALERT: {instance.transaction_type} of {instance.quantity} "
            f"for {instance.stock.product.name} by User: {instance.created_by.username}. "
            f"New Balance: {instance.stock.quantity}"
        )
