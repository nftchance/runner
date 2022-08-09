from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Transfer(models.Model):
    def save(self, *args, **kwargs):
        if not self.settled:
            if self.from_user == self.to_user:
                raise ValueError('Cannot transfer coin to self.')

            if not self.mint and self.from_user.balance < self.amount:
                raise ValueError("Exceeds balance.")

            if self.from_user:
                self.from_user.balance -= self.amount
                self.from_user.save()

            if self.to_user:
                self.to_user.balance += self.amount
                self.to_user.save()

        super(Transfer, self).save(*args, **kwargs)

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

    def mint(self, to_user, amount):
        transfer = Transfer.objects.create(
            to_user=to_user, amount=amount, mint=True)
        return transfer

    def burn(self, from_user, amount):
        transfer = Transfer.objects.create(
            from_user=from_user, amount=amount, mint=True)
        return transfer

    def transfer(self, from_user, to_user, amount):
        transfer = Transfer.objects.create(
            from_user=from_user, to_user=to_user, amount=amount)
        return transfer

    class Meta:
        ordering = ['-created_at']
