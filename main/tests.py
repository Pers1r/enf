from django.test import TestCase

# Create your tests here.
from decimal import Decimal
from django.test import TestCase
from main.models import Category, Size, Product, ProductSize

class CategoryModelTests(TestCase):
    def test_category_slug_generation(self):
        category = Category.objects.create(name='Ubrania Zimowe')
        self.assertEqual(category.slug, 'ubrania-zimowe')

    def test_category_custom_slug(self):
        category = Category.objects.create(name='Ubrania Letnie', slug='moj-wlasny-slug')
        self.assertEqual(category.slug, 'moj-wlasny-slug')

    def test_category_str(self):
        category = Category.objects.create(name='Buty')
        self.assertEqual(str(category), 'Buty')

class SizeModelTests(TestCase):
    def test_size_str(self):
        size = Size.objects.create(name='XL')
        self.assertEqual(str(size), 'XL')

class ProductModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Kategoria Testowa')

    def test_product_slug_generation(self):
        product = Product.objects.create(
            name='Czerwona Koszulka',
            category=self.category,
            color='Czerwony',
            price=Decimal('99.99')
        )
        self.assertEqual(product.slug, 'czerwona-koszulka')

    def test_product_custom_slug(self):
        product = Product.objects.create(
            name='Niebieska Koszulka',
            slug='super-niebieska',
            category=self.category,
            color='Niebieski',
            price=Decimal('99.99')
        )
        self.assertEqual(product.slug, 'super-niebieska')

    def test_product_str(self):
        product = Product.objects.create(
            name='Zielona Koszulka',
            category=self.category,
            color='Zielony',
            price=Decimal('99.99')
        )
        self.assertEqual(str(product), 'Zielona Koszulka')

class ProductSizeModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Kategoria Testowa')
        self.product = Product.objects.create(
            name='Testowy Produkt',
            category=self.category,
            color='Czarny',
            price=Decimal('100.00')
        )
        self.size = Size.objects.create(name='XXL')

    def test_product_size_str(self):
        product_size = ProductSize.objects.create(
            product=self.product,
            size=self.size,
            stock=15
        )
        expected_str = 'XXL (15 in stock) for Testowy Produkt'
        self.assertEqual(str(product_size), expected_str)