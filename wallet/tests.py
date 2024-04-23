from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Wallet
from user.models import CirkulaUser

User = get_user_model()


class WalletTestCase(TestCase):
    def setUp(self):
        self.user = CirkulaUser.objects.create_user(
            username='testuser',
            password='testpassword',
            email='testuser@testserver.com'
        )
        # Create a wallet for the user
        self.wallet = Wallet.objects.create(
            user=self.user,
            balance=1000,
            pin='1234',
            currency='NGN'
        )

    def test_deposit(self):
        initial_balance = self.wallet.balance
        amount = 500
        self.wallet.deposit(amount)
        self.assertEqual(self.wallet.balance, initial_balance + amount)

    def test_withdraw_correct_pin(self):
        initial_balance = self.wallet.balance
        amount = 500
        pin = '1234'
        self.wallet.withdraw(amount, pin)
        self.assertEqual(self.wallet.balance, initial_balance - amount)

    def test_withdraw_incorrect_pin(self):
        amount = 500
        pin = '0000'
        with self.assertRaises(ValueError):
            self.wallet.withdraw(amount, pin)

    def test_transfer_correct_pin(self):
        recipient_user = CirkulaUser.objects.create_user(
            username='recipient',
            password='testpassword',
            email='recipient@testserver.com'
        )
        recipient_wallet = Wallet.objects.create(
            user=recipient_user,
            balance=0,
            pin='5678',
            currency='NGN',
        )
        amount = 500
        pin = '1234'
        self.wallet.transfer(recipient_wallet, amount, pin)
        self.assertEqual(self.wallet.balance, 500)
        self.assertEqual(recipient_wallet.balance, amount)

    def test_transfer_incorrect_pin(self):
        recipient_user = CirkulaUser.objects.create_user(
            username='recipient',
            password='testpassword'
        )
        recipient_wallet = Wallet.objects.create(
            user=recipient_user,
            balance=0,
            pin='5678'
        )
        amount = 500
        pin = '0000'
        with self.assertRaises(ValueError):
            self.wallet.transfer(recipient_wallet, amount, pin)
