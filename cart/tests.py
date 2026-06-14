from django.test import TestCase

# Create your tests here.
from decimal import Decimal
from unittest.mock import MagicMock, patch
from django.test import TestCase, RequestFactory

# from cart.cart import Cart
from cart.forms import AddToCartForm, UpdateCartItemForm
from cart.context_processors import cart_processor
from cart.templatetags.cart_tags import multiply, get_cart_count
from cart.models import Cart as CartModel, CartItem
from main.models import Category, Product, Size, ProductSize


class MockRequest:
    def __init__(self, session_data=None):
        self.session = session_data if session_data is not None else {}
        self.session.modified = False


# class CartUnitTests(TestCase):
#     def setUp(self):
#         self.request = MockRequest()
#
#         self.product1 = MagicMock()
#         self.product1.id = 1
#         self.product1.price = Decimal('50.00')
#
#         self.product2 = MagicMock()
#         self.product2.id = 2
#         self.product2.price = Decimal('30.00')
#
#     def test_init_empty_cart(self):
#         cart = Cart(self.request)
#         self.assertEqual(cart.cart, {})
#         self.assertEqual(self.request.session['cart'], {})
#
#     def test_init_existing_cart(self):
#         self.request.session['cart'] = {'1_XL': {'quantity': 2, 'price': '50.00', 'product_id': '1', 'size': 'XL'}}
#         cart = Cart(self.request)
#         self.assertIn('1_XL', cart.cart)
#         self.assertEqual(cart.cart['1_XL']['quantity'], 2)
#
#     def test_cart_add_new_item(self):
#         cart = Cart(self.request)
#         cart.add(self.product1, size='XL', quantity=2)
#
#         self.assertIn('1_XL', cart.cart)
#         self.assertEqual(cart.cart['1_XL']['quantity'], 2)
#         self.assertEqual(cart.cart['1_XL']['price'], '50.00')
#         self.assertTrue(self.request.session.modified)
#
#     def test_cart_add_existing_item(self):
#         cart = Cart(self.request)
#         cart.add(self.product1, size='XL', quantity=2)
#         cart.add(self.product1, size='XL', quantity=3)
#
#         self.assertEqual(cart.cart['1_XL']['quantity'], 5)
#
#     def test_cart_add_with_override_quantity(self):
#         cart = Cart(self.request)
#         cart.add(self.product1, size='XL', quantity=2)
#         cart.add(self.product1, size='XL', quantity=10, override_quantity=True)
#
#         self.assertEqual(cart.cart['1_XL']['quantity'], 10)
#
#     def test_cart_remove_item(self):
#         cart = Cart(self.request)
#         cart.add(self.product1, size='XL', quantity=1)
#         cart.add(self.product2, size='M', quantity=1)
#
#         cart.remove(self.product1, size='XL')
#
#         self.assertNotIn('1_XL', cart.cart)
#         self.assertIn('2_M', cart.cart)
#         self.assertTrue(self.request.session.modified)
#
#     def test_cart_remove_non_existent_item(self):
#         cart = Cart(self.request)
#         cart.remove(self.product1, size='XL')
#         self.assertEqual(cart.cart, {})
#
#     def test_cart_update_quantity_positive(self):
#         cart = Cart(self.request)
#         cart.add(self.product1, size='XL', quantity=1)
#         cart.update_quantity(self.product1, size='XL', quantity=7)
#
#         self.assertEqual(cart.cart['1_XL']['quantity'], 7)
#
#     def test_cart_update_quantity_zero_or_negative(self):
#         cart = Cart(self.request)
#         cart.add(self.product1, size='XL', quantity=5)
#
#         cart.update_quantity(self.product1, size='XL', quantity=0)
#         self.assertNotIn('1_XL', cart.cart)
#
#     def test_cart_len(self):
#         cart = Cart(self.request)
#         cart.add(self.product1, size='XL', quantity=2)
#         cart.add(self.product2, size='M', quantity=4)
#
#         self.assertEqual(len(cart), 6)
#
#     def test_cart_clear(self):
#         cart = Cart(self.request)
#         cart.add(self.product1, size='XL', quantity=1)
#         cart.clear()
#
#         self.assertNotIn('cart', self.request.session)
#
#     @patch('cart.cart.Product.objects.filter')
#     def test_cart_iter_and_get_total_price(self, mock_filter):
#         cart = Cart(self.request)
#         cart.add(self.product1, size='XL', quantity=2)
#         cart.add(self.product2, size='M', quantity=3)
#
#         mock_filter.return_value = [self.product1, self.product2]
#
#         items = list(cart)
#
#         self.assertEqual(len(items), 2)
#         self.assertEqual(cart.get_total_price(), Decimal('190.00'))
#
#     @patch('cart.cart.Product.objects.filter')
#     def test_get_cart_items(self, mock_filter):
#         cart = Cart(self.request)
#         cart.add(self.product1, size='XL', quantity=2)
#         mock_filter.return_value = [self.product1]
#
#         items = cart.get_cart_items()
#
#         self.assertEqual(len(items), 1)
#         self.assertEqual(items[0]['quantity'], 2)
#         self.assertEqual(items[0]['size'], 'XL')
#         self.assertEqual(items[0]['price'], Decimal('50.00'))
#         self.assertEqual(items[0]['total_price'], Decimal('100.00'))
#         self.assertEqual(items[0]['cart_key'], '1_XL')


class CartFormsTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(
            name='Test Product',
            category=self.category,
            price=Decimal('100.00')
        )
        self.size = Size.objects.create(name='L')
        self.product_size = ProductSize.objects.create(
            product=self.product,
            size=self.size,
            stock=10
        )

    def test_add_to_cart_form_initialization(self):
        form = AddToCartForm(product=self.product)
        self.assertIn('size_id', form.fields)
        choices = form.fields['size_id'].choices
        self.assertEqual(len(choices), 1)
        self.assertEqual(choices[0], (self.product_size.id, 'L'))

    def test_add_to_cart_form_valid_data(self):
        data = {'size_id': self.product_size.id, 'quantity': 2}
        form = AddToCartForm(product=self.product, data=data)
        self.assertTrue(form.is_valid())

    def test_add_to_cart_form_invalid_quantity(self):
        data = {'size_id': self.product_size.id, 'quantity': 0}
        form = AddToCartForm(product=self.product, data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('quantity', form.errors)

    def test_update_cart_item_form_max_quantity_validator(self):
        cart = CartModel.objects.create(session_key='dummy_session')
        cart_item = CartItem.objects.create(
            cart=cart,
            product=self.product,
            product_size=self.product_size,
            quantity=2,
            price=Decimal('100.00')
        )

        form_valid = UpdateCartItemForm(instance=cart_item, data={'quantity': 10})
        self.assertTrue(form_valid.is_valid())

        form_invalid = UpdateCartItemForm(instance=cart_item, data={'quantity': 15})
        self.assertFalse(form_invalid.is_valid())
        self.assertIn('quantity', form_invalid.errors)


class MockSession(dict):
    def __init__(self, session_key=None):
        super().__init__()
        self.session_key = session_key

    def create(self):
        self.session_key = 'new_generated_session_key'


class CartContextProcessorTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_cart_processor_without_session_key(self):
        request = self.factory.get('/')
        request.session = MockSession(session_key=None)

        context = cart_processor(request)

        self.assertIsNotNone(request.session.session_key)
        self.assertEqual(context['cart_total_items'], 0)
        self.assertEqual(context['cart_subtotal'], Decimal('0.00') if hasattr(CartModel(), 'subtotal') else 0)

    def test_cart_processor_with_existing_cart(self):
        session_key = 'existing_session_key'
        request = self.factory.get('/')
        request.session = MockSession(session_key=session_key)

        CartModel.objects.create(session_key=session_key)

        context = cart_processor(request)
        self.assertEqual(context['cart_total_items'], 0)


class CartTemplateTagsTests(TestCase):
    def test_multiply_filter(self):
        self.assertEqual(multiply(5, 2), 10.0)
        self.assertEqual(multiply('5', '2.5'), 12.5)

    def test_multiply_filter_invalid_input(self):
        self.assertEqual(multiply(None, 5), 0)
        self.assertEqual(multiply('text', 'text'), 0)

    def test_get_cart_count_no_session(self):
        request = RequestFactory().get('/')
        request.session = MockSession(session_key=None)
        context = {'request': request}

        self.assertEqual(get_cart_count(context), 0)

    def test_get_cart_count_existing_cart(self):
        session_key = 'tag_session_key'
        request = RequestFactory().get('/')
        request.session = MockSession(session_key=session_key)
        context = {'request': request}

        CartModel.objects.create(session_key=session_key)

        self.assertEqual(get_cart_count(context), 0)