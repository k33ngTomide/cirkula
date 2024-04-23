from django.test import TestCase
from django.contrib.auth import get_user_model


class CustomUserTest(TestCase):
    def setUp(self):
        self.CirkulaUser = get_user_model()

    def test_create_user(self):
        # Test creating a new user
        user = self.CirkulaUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpassword'))

    def test_create_superuser(self):
        # Test creating a new superuser
        admin_user = self.CirkulaUser.objects.create_superuser(
            username='adminuser',
            email='admin@example.com',
            password='adminpassword'
        )
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_staff)
