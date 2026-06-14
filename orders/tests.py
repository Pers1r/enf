from django.test import TestCase

# Create your tests here.
from decimal import Decimal
from django.test import TestCase
from orders.models import Order, OrderItem
from orders.forms import OrderForm
from users.models import CustomUser
from main.models import Category, Product, Size, ProductSize


class OrderModelTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='klient@example.com',
            first_name='Jan',
            last_name='Kowalski',
            password='testpassword123'
        )

        self.order = Order.objects.create(
            user=self.user,
            first_name='Jan',
            last_name='Kowalski',
            email='klient@example.com',
            total_price=Decimal('150.00')
        )

    def test_order_creation_default_status(self):
        self.assertEqual(self.order.status, 'pending')

    def test_order_string_representation(self):
        expected_str = f'Order {self.order.id} by klient@example.com'
        self.assertEqual(str(self.order), expected_str)


class OrderItemModelTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='klient2@example.com',
            first_name='Anna',
            last_name='Nowak',
            password='testpassword123'
        )

        self.category = Category.objects.create(name='Ubrania')

        self.product = Product.objects.create(
            name='Koszulka Testowa',
            category=self.category,
            color='Czarny',
            price=Decimal('50.00')
        )

        self.size = Size.objects.create(name='XL')

        self.product_size = ProductSize.objects.create(
            product=self.product,
            size=self.size,
            stock=10
        )

        self.order = Order.objects.create(
            user=self.user,
            first_name='Anna',
            last_name='Nowak',
            email='klient2@example.com',
            total_price=Decimal('150.00')
        )

        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            size=self.product_size,
            quantity=3,
            price=Decimal('50.00')
        )

    def test_order_item_string_representation(self):
        expected_str = 'Koszulka Testowa - XL (3)'
        self.assertEqual(str(self.order_item), expected_str)

    def test_order_item_get_total_price(self):
        expected_total = Decimal('150.00')
        self.assertEqual(self.order_item.get_total_price(), expected_total)


class OrderFormTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='formularz@example.com',
            first_name='Piotr',
            last_name='Testowy',
            password='testpassword123',
            company='Testowa Firma',
            address1='Testowa 1',
            city='Warszawa',
            postal_code='00-001'
        )

    def test_form_initialization_with_user(self):
        form = OrderForm(user=self.user)
        self.assertEqual(form.initial.get('first_name'), 'Piotr')
        self.assertEqual(form.initial.get('email'), 'formularz@example.com')
        self.assertEqual(form.initial.get('company'), 'Testowa Firma')
        self.assertEqual(form.initial.get('city'), 'Warszawa')

    def test_form_initialization_without_user(self):
        form = OrderForm()
        self.assertIsNone(form.initial.get('first_name'))
        self.assertIsNone(form.initial.get('email'))

    def test_form_valid_data(self):
        form_data = {
            'first_name': 'Adam',
            'last_name': 'Nowak',
            'email': 'adam@example.com',
            'address1': 'Prosta 2',
            'city': 'Kraków',
            'country': 'Polska',
            'postal_code': '30-000'
        }
        form = OrderForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_form_invalid_missing_required_fields(self):
        form_data = {
            'email': 'adam@example.com',
            'city': 'Kraków'
        }
        form = OrderForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors)
        self.assertIn('last_name', form.errors)

    def test_form_clean_strips_html_tags(self):
        form_data = {
            'first_name': 'Adam',
            'last_name': 'Nowak',
            'email': 'adam@example.com',
            'company': '<b>Super</b> Firma',
            'address1': '<script>alert("hacked")</script>Zła Ulica',
            'city': '<i>Kraków</i>'
        }
        form = OrderForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['company'], 'Super Firma')
        self.assertEqual(form.cleaned_data['address1'], 'alert("hacked")Zła Ulica')
        self.assertEqual(form.cleaned_data['city'], 'Kraków')