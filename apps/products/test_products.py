from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from .models import Product
from apps.categories.models import Category

User = get_user_model()

class ProductAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testadmin', password='testpassword123')
        self.client.force_authenticate(user=self.user)
        
        self.category = Category.objects.create(name='Electronics')
        self.product = Product.objects.create(
            sku='TEST-001',
            name='Test Product',
            price=99.99,
            category=self.category,
            status='ACTIVE'
        )
        self.url = reverse('api_product_list_create')
        self.detail_url = reverse('api_product_detail', args=[self.product.id])

    def test_get_products_list(self):
        """Test retrieving list of products"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_product(self):
        """Test creating a new product"""
        payload = {
            'sku': 'TEST-002',
            'name': 'New Product',
            'price': '149.99',
            'category': self.category.id,
            'status': 'DRAFT'
        }
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)

    def test_unauthenticated_access(self):
        """Test that unauthenticated users cannot access the API"""
        self.client.logout()
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        # Should be 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
