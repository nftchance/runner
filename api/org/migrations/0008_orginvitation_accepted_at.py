# Generated by Django 4.0.6 on 2022-08-02 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('org', '0007_orginvitation'),
    ]

    operations = [
        migrations.AddField(
            model_name='orginvitation',
            name='accepted_at',
            field=models.DateTimeField(null=True),
        ),
    ]