# Generated by Django 4.0.6 on 2022-08-10 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('governance', '0006_proposal_approved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposalvote',
            name='vote',
            field=models.CharField(choices=[('for', 'For'), ('against', 'Against'), ('abstain', 'Abstain')], default='abstain', max_length=255),
        ),
    ]
