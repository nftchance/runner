# Generated by Django 4.0.6 on 2022-08-10 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coin', '0002_alter_transfer_to_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='transfer',
            name='label',
            field=models.CharField(blank=True, choices=[('mint', 'Mint'), ('transfer', 'Transfer'), ('burn', 'Burn'), ('deposit', 'Deposit'), ('withdraw', 'Withdraw')], default='transfer', max_length=255, null=True),
        ),
    ]
