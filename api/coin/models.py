from decimal import Decimal
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .utils import Label


class Transfer(models.Model):
    def save(self, *args, **kwargs):
        if not self.settled:
            if self.from_user == self.to_user:
                raise ValueError('Cannot transfer coin to self.')

            self.amount = Decimal(self.amount)

            if not self.mint and self.from_user.balance < self.amount:
                raise ValueError("Exceeds balance.")

            if self.from_user:
                self.from_user.balance -= self.amount
                self.from_user.save()
                print('from_user.balance', self.from_user.balance)


            if self.to_user:
                self.to_user.balance += self.amount
                self.to_user.save()

        super(Transfer, self).save(*args, **kwargs)

    LABELS = (
        (Label.MINT, 'Mint'),
        (Label.TRANSFER, 'Transfer'),
        (Label.BURN, 'Burn'),
        (Label.DEPOSIT, 'Deposit'),
        (Label.WITHDRAW, 'Withdraw'),
    )

    label = models.CharField(max_length=255, blank=True,
                             null=True, choices=LABELS, default=Label.TRANSFER)

    from_user = models.ForeignKey(
        'user.User', blank=True, null=True, on_delete=models.CASCADE, related_name='from_user')
    to_user = models.ForeignKey(
        'user.User', blank=True, null=True, on_delete=models.CASCADE, related_name='to_user')

    mint = models.BooleanField(default=False)

    amount = models.DecimalField(max_digits=20, decimal_places=4)

    settled = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.from_user} - {self.to_user} - {self.amount}"

    class Meta:
        ordering = ['-created_at']


class Coin(models.Model):
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"

    def mint(self, to_user, amount, label=Label.MINT):
        transfer = Transfer.objects.create(
            to_user=to_user, amount=amount, mint=True, label=label)
        return transfer

    def burn(self, from_user, amount, label=Label.BURN):
        transfer = Transfer.objects.create(
            from_user=from_user, amount=amount, label=label)
        return transfer

    def transfer(self, from_user, to_user, amount, label=Label.TRANSFER):
        transfer = Transfer.objects.create(
            from_user=from_user, to_user=to_user, amount=amount, label=label)
        return transfer

    def deposit(self, from_user, amount):
        return self.burn(from_user, amount, Label.DEPOSIT)

    def withdraw(self, to_user, amount):
        return self.mint(to_user, amount, Label.WITHDRAW)

    class Meta:
        ordering = ['-created_at']
