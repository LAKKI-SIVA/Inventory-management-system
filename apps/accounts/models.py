from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom User model for the Inventory & Order Management System.
    Instead of using the default Django user, we create our own to allow
    future customizations (like adding a 'role' field).
    """
    
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        INVENTORY_MANAGER = 'INVENTORY_MANAGER', 'Inventory Manager'
        CUSTOMER = 'CUSTOMER', 'Customer'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CUSTOMER
    )
    
    class Meta:
        db_table = 'auth_user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"
