# Generated by Django 4.0.6 on 2022-07-30 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0003_job_schedule'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='id',
            field=models.CharField(blank=True, max_length=256, primary_key=True, serialize=False, unique=True),
        ),
    ]
