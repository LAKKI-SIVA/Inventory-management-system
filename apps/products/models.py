from django.db import models
from apps.categories.models import Category
from apps.suppliers.models import Supplier

class Product(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active'
        DRAFT = 'DRAFT', 'Draft'
        ARCHIVED = 'ARCHIVED', 'Archived'

    sku = models.CharField(max_length=50, unique=True, help_text="Stock Keeping Unit")
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Relationships
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT
    )
    
    # We will let the Inventory app handle the actual 'stock_quantity' later, 
    # but we will store the image here if we want to display it.
    image = models.ImageField(upload_to='products/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products'
        ordering = ['name']

    def __str__(self):
        return f"{self.sku} - {self.name}"
