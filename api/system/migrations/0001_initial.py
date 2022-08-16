# Generated by Django 4.0.6 on 2022-08-12 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Broadcast',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('link_text', models.CharField(max_length=100)),
                ('link_url', models.CharField(max_length=100)),
                ('external', models.BooleanField(default=False)),
                ('expired_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='WaitlistEntry',
            fields=[
                ('id', models.CharField(blank=True, max_length=256, primary_key=True, serialize=False, unique=True)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('invited_at', models.DateTimeField(blank=True, null=True)),
                ('invite_id', models.CharField(blank=True, max_length=100, null=True)),
                ('accepted_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
    ]