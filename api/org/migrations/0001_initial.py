# Generated by Django 4.0.6 on 2022-08-12 20:37

from django.db import migrations, models
import django.db.models.deletion
import org.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Org',
            fields=[
                ('id', models.CharField(blank=True, max_length=256, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=256)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['created_at'],
                'permissions': (('manage_org', 'Can manage organization'),),
            },
        ),
        migrations.CreateModel(
            name='OrgInvitation',
            fields=[
                ('id', models.CharField(blank=True, max_length=256, primary_key=True, serialize=False, unique=True)),
                ('role', models.CharField(choices=[('revoked', 'Revoked'), ('customer', 'Customer'), ('team', 'Team'), ('manager', 'Manager'), ('admin', 'Admin')], default='revoked', max_length=256)),
                ('expires_at', models.DateTimeField(null=True)),
                ('accepted_at', models.DateTimeField(null=True)),
                ('revoked_at', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['created_at'],
                'permissions': (('manage_orginvitation', 'Can manage organization invitations'),),
            },
        ),
        migrations.CreateModel(
            name='OrgRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('revoked', 'Revoked'), ('customer', 'Customer'), ('team', 'Team'), ('manager', 'Manager'), ('admin', 'Admin')], default='customer', max_length=256, unique=True)),
                ('permissions', models.ManyToManyField(blank=True, to='auth.permission', verbose_name='permissions')),
            ],
            options={
                'ordering': ['name'],
            },
            managers=[
                ('objects', org.models.OrgRoleManager()),
            ],
        ),
        migrations.CreateModel(
            name='OrgRelationship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('org', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relationships', to='org.org')),
                ('permissions', models.ManyToManyField(blank=True, help_text='Permissions for the user of this relationship in this organization.', related_name='relationship_set', related_query_name='relationship', to='auth.permission')),
            ],
            options={
                'ordering': ['created_at'],
                'permissions': (('manage_orgrelationship', 'Can manage organization relationships of other users'),),
            },
        ),
    ]
