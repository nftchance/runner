# Generated by Django 4.0.6 on 2022-08-14 08:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coin', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transfer',
            options={'ordering': ['-created_at'], 'permissions': (('manage_transfer', 'Can manage transfer'),)},
        ),
    ]