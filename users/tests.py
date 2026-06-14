from django.test import TestCase
from django.core.exceptions import ValidationError
from users.models import CustomUser
from users.forms import CustomUserCreationForm, CustomUserLoginForm, CustomUserUpdateForm


class CustomUserManagerTests(TestCase):
    def test_create_user(self):
        CustomUser.username.create_user(
            email='normal@user.com',
            first_name='Jan',
            last_name='Kowalski',
            password='foo'
        )
        user = CustomUser.objects.get(email='normal@user.com')
        self.assertEqual(user.email, 'normal@user.com')
        self.assertEqual(user.first_name, 'Jan')
        self.assertEqual(user.last_name, 'Kowalski')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.check_password('foo'))

    def test_create_user_without_email_raises_error(self):
        with self.assertRaises(ValueError):
            CustomUser.username.create_user(
                email='',
                first_name='Jan',
                last_name='Kowalski',
                password='foo'
            )

    def test_create_user_email_normalization(self):
        email = 'test@DOMAIN.COM'
        CustomUser.username.create_user(
            email=email,
            first_name='Jan',
            last_name='Kowalski',
            password='foo'
        )
        user = CustomUser.objects.get(email='test@domain.com')
        self.assertEqual(user.email, 'test@domain.com')

    def test_create_superuser(self):
        CustomUser.username.create_superuser(
            email='super@user.com',
            first_name='Super',
            last_name='Admin',
            password='foo'
        )
        admin_user = CustomUser.objects.get(email='super@user.com')
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.check_password('foo'))

    def test_create_superuser_with_is_staff_false_raises_error(self):
        with self.assertRaisesMessage(ValueError, 'Superuser must have is_staff=True.'):
            CustomUser.username.create_superuser(
                email='super@user.com',
                first_name='Super',
                last_name='Admin',
                password='foo',
                is_staff=False
            )

    def test_create_superuser_with_is_superuser_false_raises_error(self):
        with self.assertRaisesMessage(ValueError, 'Superuser must have is_superuser=True.'):
            CustomUser.username.create_superuser(
                email='super@user.com',
                first_name='Super',
                last_name='Admin',
                password='foo',
                is_superuser=False
            )


class CustomUserLogicTests(TestCase):
    def test_user_string_representation(self):
        user = CustomUser(email='test@example.com')
        self.assertEqual(str(user), 'test@example.com')

    def test_clean_strips_html_tags(self):
        user = CustomUser(
            email='test@example.com',
            first_name='Jan',
            last_name='Kowalski',
            company='<b>Super</b> Firma',
            address1='<script>alert(1)</script>Ulica',
            city='<i>Warszawa</i>'
        )
        user.clean()

        self.assertEqual(user.company, 'Super Firma')
        self.assertEqual(user.address1, 'alert(1)Ulica')
        self.assertEqual(user.city, 'Warszawa')


class CustomUserCreationFormTests(TestCase):
    def setUp(self):
        CustomUser.username.create_user(
            email='zajety@example.com', first_name='Jan', last_name='Kowalski', password='testpassword123'
        )
        self.existing_user = CustomUser.objects.get(email='zajety@example.com')

    def test_form_valid_data(self):
        form_data = {
            'first_name': 'Anna',
            'last_name': 'Nowak',
            'email': 'anna@example.com',
            'password1': 'SilneHaslo123!',
            'password2': 'SilneHaslo123!'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_form_invalid_existing_email(self):
        form_data = {
            'first_name': 'Piotr',
            'last_name': 'Zajęty',
            'email': 'zajety@example.com',
            'password1': 'SilneHaslo123!',
            'password2': 'SilneHaslo123!'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertEqual(form.errors['email'][0], 'Email already exists')

    def test_form_passwords_mismatch(self):
        form_data = {
            'first_name': 'Anna',
            'last_name': 'Nowak',
            'email': 'anna2@example.com',
            'password1': 'SilneHaslo123!',
            'password2': 'ZupelnieInneHaslo!'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(any(
            'match' in str(err).lower() or 'pasuj' in str(err).lower() for err_list in form.errors.values() for err in
            err_list))


class CustomUserLoginFormTests(TestCase):
    def setUp(self):
        CustomUser.username.create_user(
            email='klient@example.com', first_name='Jan', last_name='Kowalski', password='testpassword123'
        )
        self.user = CustomUser.objects.get(email='klient@example.com')

        CustomUser.username.create_user(
            email='nieaktywny@example.com', first_name='Jan', last_name='Kowalski', password='testpassword123',
            is_active=False
        )
        self.inactive_user = CustomUser.objects.get(email='nieaktywny@example.com')

    def test_form_valid_login(self):
        form_data = {'username': 'klient@example.com', 'password': 'testpassword123'}
        form = CustomUserLoginForm(request=None, data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_form_invalid_password(self):
        form_data = {'username': 'klient@example.com', 'password': 'zle_haslo'}
        form = CustomUserLoginForm(request=None, data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['__all__'][0], 'Email or password is invalid')

    def test_form_inactive_user(self):
        form_data = {'username': 'nieaktywny@example.com', 'password': 'testpassword123'}
        form = CustomUserLoginForm(request=None, data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['__all__'][0], 'Email or password is invalid')


class CustomUserUpdateFormTests(TestCase):
    def setUp(self):
        CustomUser.username.create_user(
            email='user1@example.com', first_name='Jan', last_name='Pierwszy', password='testpassword123'
        )
        self.user1 = CustomUser.objects.get(email='user1@example.com')

        CustomUser.username.create_user(
            email='user2@example.com', first_name='Anna', last_name='Druga', password='testpassword123'
        )
        self.user2 = CustomUser.objects.get(email='user2@example.com')

    def test_form_valid_update(self):
        form_data = {
            'first_name': 'Janek',
            'last_name': 'Zaktualizowany',
            'email': 'user1@example.com',
            'phone': '123456789',
            'city': 'Kraków'
        }
        form = CustomUserUpdateForm(instance=self.user1, data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_form_invalid_phone_number(self):
        form_data = {
            'first_name': 'Janek',
            'last_name': 'Zaktualizowany',
            'phone': 'ToNieJestNumer'
        }
        form = CustomUserUpdateForm(instance=self.user1, data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('phone', form.errors)
        self.assertEqual(form.errors['phone'][0], 'Enter a valid phone number.')

    def test_form_email_already_exists_for_other_user(self):
        form_data = {
            'first_name': 'Janek',
            'last_name': 'Zaktualizowany',
            'email': 'user2@example.com',
        }
        form = CustomUserUpdateForm(instance=self.user1, data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertEqual(form.errors['email'][0], 'Email already exists')

    def test_form_empty_email_restores_from_instance(self):
        form_data = {
            'first_name': 'Janek',
            'last_name': 'Zaktualizowany',
            'email': '',
        }
        form = CustomUserUpdateForm(instance=self.user1, data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['email'], 'user1@example.com')

    def test_form_strips_html_tags_in_clean(self):
        form_data = {
            'first_name': 'Janek',
            'last_name': 'Zaktualizowany',
            'company': '<b>Moja</b> Firma',
            'city': '<i>Kraków</i>'
        }
        form = CustomUserUpdateForm(instance=self.user1, data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['company'], 'Moja Firma')
        self.assertEqual(form.cleaned_data['city'], 'Kraków')