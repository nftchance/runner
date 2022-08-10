# Generated by Django 4.0.6 on 2022-08-10 17:48

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('governance', '0008_proposalvote_released_at_proposalvote_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposal',
            name='summary',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='proposal',
            name='tags',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('dashboard', 'Dashboard'), ('fees', 'Fees'), ('financials', 'Financials'), ('governance', 'Governance'), ('integrations', 'Integrations'), ('payments', 'Payments'), ('reviews', 'Reviews'), ('taxes', 'Taxes'), ('ux', 'UX')], max_length=255), blank=True, null=True, size=None),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='votes',
            field=models.ManyToManyField(blank=True, to='governance.proposalvote'),
        ),
    ]
