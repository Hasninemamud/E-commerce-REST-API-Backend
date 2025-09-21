from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from products.models import Product, Category
from orders.models import Order, OrderItem

User = get_user_model()

class APITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpassword123',
            first_name='Test',
            last_name='User'
        )
        self.admin_user = User.objects.create_superuser(
            email='admin@example.com',
            password='adminpassword123'
        )
        self.category = Category.objects.create(
            name='Test Category',
            description='Test category description'
        )
        self.product = Product.objects.create(
            name='Test Product',
            description='Test product description',
            price=29.99,
            category=self.category
        )

    def test_user_registration(self):
        """Test user registration endpoint"""
        data = {
            'email': 'newuser@example.com',
            'password': 'newpassword123',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = self.client.post(reverse('accounts:register'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('access' in response.data)
        self.assertTrue('refresh' in response.data)

    def test_user_login(self):
        """Test user login endpoint"""
        data = {
            'email': 'test@example.com',
            'password': 'testpassword123'
        }
        response = self.client.post(reverse('accounts:login'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)
        self.assertTrue('refresh' in response.data)

    def test_get_products(self):
        """Test get products endpoint"""
        response = self.client.get(reverse('products:product-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_get_product_detail(self):
        """Test get product detail endpoint"""
        response = self.client.get(
            reverse('products:product-detail', kwargs={'pk': self.product.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Product')

    def test_create_product_admin(self):
        """Test create product endpoint (admin only)"""
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'name': 'New Product',
            'description': 'New product description',
            'price': 39.99,
            'category': self.category.pk
        }
        response = self.client.post(reverse('products:product-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)

    def test_create_product_non_admin(self):
        """Test create product endpoint (non-admin)"""
        self.client.force_authenticate(user=self.user)
        data = {
            'name': 'New Product',
            'description': 'New product description',
            'price': 39.99,
            'category': self.category.pk
        }
        response = self.client.post(reverse('products:product-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_order(self):
        """Test create order endpoint"""
        self.client.force_authenticate(user=self.user)
        data = {
            'items': [
                {
                    'product': self.product.pk,
                    'quantity': 2
                }
            ]
        }
        response = self.client.post(reverse('orders:order-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderItem.objects.count(), 1)

    def test_get_user_orders(self):
        """Test get user orders endpoint"""
        # Create an order first
        order = Order.objects.create(user=self.user, total_amount=59.98)
        OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=2,
            price=29.99
        )
        
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('orders:order-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)