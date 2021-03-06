# Generated by Django 4.0.1 on 2022-01-12 01:31

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('seller', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Request_Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('book_name', models.CharField(max_length=100)),
                ('author', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_date'],
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('incart', 'incart'), ('cancelled', 'cancelled')], default='incart', max_length=120)),
                ('quantity', models.IntegerField(default=1)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item', to='seller.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_date'],
            },
        ),
        migrations.CreateModel(
            name='BookBuy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('quantity', models.PositiveIntegerField(default=1, help_text='No: of Books You Want To Buy')),
                ('address', models.CharField(max_length=120)),
                ('seller', models.CharField(default=None, max_length=250)),
                ('status', models.CharField(choices=[('pending', 'pending'), ('orderplaced', 'orderplaced'), ('dispatch', 'dispatch'), ('intransit', 'intransit'), ('delivered', 'delivered'), ('ordercancelled', 'ordercancelled')], default='orderplaced', max_length=120)),
                ('expected_delivery', models.DateField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(datetime.date.today)])),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='buybook', to='seller.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buyuser', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_date'],
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('mob_no', models.CharField(max_length=30)),
                ('house', models.CharField(max_length=150)),
                ('street', models.CharField(max_length=150)),
                ('town', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('pin', models.CharField(max_length=30)),
                ('landmark', models.CharField(max_length=150)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_date'],
            },
        ),
    ]
