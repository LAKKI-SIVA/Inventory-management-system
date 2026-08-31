from django.core.exceptions import ValidationError
from .models import Product

class ProductService:
    """
    Service layer for Product business logic.
    Instead of putting fat logic in Views or Models, we keep it here.
    """

    @staticmethod
    def create_product(sku: str, name: str, price: float, category_id: int, supplier_id: int = None, **kwargs) -> Product:
        if price <= 0:
            raise ValidationError("Product price must be greater than zero.")
        
        # Check SKU uniqueness before hitting the DB constraint
        if Product.objects.filter(sku=sku).exists():
            raise ValidationError(f"A product with SKU {sku} already exists.")
            
        product = Product.objects.create(
            sku=sku,
            name=name,
            price=price,
            category_id=category_id,
            supplier_id=supplier_id,
            **kwargs
        )
        return product

    @staticmethod
    def update_product(product: Product, sku: str, name: str, price: float, category_id: int, supplier_id: int = None, **kwargs) -> Product:
        if price <= 0:
            raise ValidationError("Product price must be greater than zero.")
        
        if product.sku != sku and Product.objects.filter(sku=sku).exists():
            raise ValidationError(f"A product with SKU {sku} already exists.")
            
        product.sku = sku
        product.name = name
        product.price = price
        product.category_id = category_id
        product.supplier_id = supplier_id
        for key, value in kwargs.items():
            setattr(product, key, value)
            
        product.save()
        return product

    @staticmethod
    def mark_as_active(product: Product):
        if not product.category.is_active:
            raise ValidationError("Cannot activate a product in an inactive category.")
        product.status = Product.Status.ACTIVE
        product.save()
