from django.db import models
from django.utils import timezone
from user.models import CirkulaUser


class Wallet(models.Model):
    user = models.OneToOneField(CirkulaUser, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, default='NGN')
    pin = models.CharField(max_length=4, default='0000')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Wallet for {self.user.username}, {self.balance}{self.currency}"

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")
        self.balance += amount
        self.save()

    def withdraw(self, amount, pin):
        self.validate_amount(amount)
        self.validate_pin(pin)
        self.balance -= amount
        self.save()

    def transfer(self, recipient_wallet, amount, pin):
        self.validate_amount(amount)
        self.validate_pin(pin)
        self.balance -= amount
        recipient_wallet.balance += amount
        self.save()
        recipient_wallet.save()

    def validate_amount(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")
        if self.balance < amount:
            raise ValueError("Insufficient funds.")

    def validate_pin(self, pin):
        if pin != self.pin:
            raise ValueError("Incorrect PIN.")


class Transaction(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    wallet = models.ForeignKey(Wallet, related_name='transactions', on_delete=models.CASCADE)
    date = models.DateField()
    description = models.TextField()
    type = models.TextField()

    def __str__(self):
        return str(self.amount) + str(self.date)


class TransferTransaction(Transaction):
    sender = models.ForeignKey(CirkulaUser, related_name='debit', on_delete=models.CASCADE)
    receiver = models.ForeignKey(CirkulaUser, related_name='credit', on_delete=models.CASCADE)

