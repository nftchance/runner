# Generated by Django 4.0.6 on 2022-08-10 19:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('governance', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposalvote',
            name='voter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='proposal',
            name='proposed_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='proposal',
            name='votes',
            field=models.ManyToManyField(blank=True, to='governance.proposalvote'),
        ),
    ]