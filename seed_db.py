import os
import django

# Setup Django before importing models
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.categories.models import Category
from apps.suppliers.models import Supplier
from apps.products.models import Product
from apps.inventory.models import Stock

def seed():
    # Categories
    electronics, _ = Category.objects.get_or_create(name='Electronics', description='Electronic devices and accessories')
    office, _ = Category.objects.get_or_create(name='Office Supplies', description='General office supplies')
    furniture, _ = Category.objects.get_or_create(name='Furniture', description='Office and home furniture')

    # Suppliers
    tech_corp, _ = Supplier.objects.get_or_create(name='TechCorp', email='contact@techcorp.com', phone='123-456-7890', address='123 Tech Lane')
    office_depot, _ = Supplier.objects.get_or_create(name='OfficeDepot', email='sales@officedepot.com', phone='098-765-4321', address='456 Office Blvd')

    # Products
    p1, _ = Product.objects.get_or_create(sku='LAP-001', name='ThinkPad T14', description='Business laptop', price=1200.00, category=electronics, supplier=tech_corp)
    p2, _ = Product.objects.get_or_create(sku='MON-001', name='Dell 27" Monitor', description='4K USB-C Monitor', price=450.00, category=electronics, supplier=tech_corp)
    p3, _ = Product.objects.get_or_create(sku='CHAIR-001', name='Ergonomic Chair', description='Mesh back office chair', price=299.99, category=furniture, supplier=office_depot)
    p4, _ = Product.objects.get_or_create(sku='PEN-001', name='Ballpoint Pens (50 pack)', description='Blue ink pens', price=15.99, category=office, supplier=office_depot)

    # Inventory Stock
    Stock.objects.get_or_create(product=p1, defaults={'quantity': 50, 'reorder_level': 10})
    Stock.objects.get_or_create(product=p2, defaults={'quantity': 30, 'reorder_level': 5})
    Stock.objects.get_or_create(product=p3, defaults={'quantity': 100, 'reorder_level': 20})
    Stock.objects.get_or_create(product=p4, defaults={'quantity': 500, 'reorder_level': 100})

    print("Database successfully seeded with realistic dummy data!")

if __name__ == '__main__':
    seed()
