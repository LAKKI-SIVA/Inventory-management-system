from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.products.models import Product
from apps.categories.models import Category
from django.core.exceptions import ValidationError
from .models import Stock
from .services import InventoryService

User = get_user_model()

class InventoryServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='invuser', password='password123')
        self.category = Category.objects.create(name='Widgets')
        self.product = Product.objects.create(
            sku='WIDG-001', name='Widget A', price=10.00, category=self.category
        )
        self.stock = Stock.objects.create(product=self.product, quantity=0, reorder_level=10)

    def test_stock_adjustment_in(self):
        """Test adding stock increases quantity"""
        initial_qty = self.stock.quantity
        InventoryService.adjust_stock(
            stock=self.stock,
            quantity_change=50,
            transaction_type='IN',
            user=self.user
        )
        self.stock.refresh_from_db()
        self.assertEqual(self.stock.quantity, initial_qty + 50)

    def test_stock_adjustment_out(self):
        """Test removing stock decreases quantity"""
        # First add some stock
        InventoryService.adjust_stock(self.stock, 100, 'IN', self.user)
        
        # Then remove some
        InventoryService.adjust_stock(self.stock, -30, 'OUT', self.user)
        self.stock.refresh_from_db()
        self.assertEqual(self.stock.quantity, 70)

    def test_negative_stock_validation(self):
        """Test that stock cannot go below zero"""
        with self.assertRaises(ValidationError):
            InventoryService.adjust_stock(self.stock, -50, 'OUT', self.user)
