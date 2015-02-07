# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('payments', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(unique=True, max_length=255, verbose_name=b'email address')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='admin status')),
                ('is_active', models.BooleanField(default=True)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'date joined')),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'swappable': 'AUTH_USER_MODEL',
                'verbose_name_plural': 'users',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('street', models.CharField(max_length=50, null=True)),
                ('apt', models.CharField(max_length=50, null=True)),
                ('city', models.CharField(max_length=20, null=True)),
                ('state', models.CharField(max_length=20, null=True)),
                ('zip', models.IntegerField(max_length=5, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Bar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('barName', models.CharField(max_length=50)),
                ('addressLine1', models.CharField(max_length=50)),
                ('addressLine2', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('zip', models.CharField(max_length=5)),
                ('foodMenu', models.BooleanField(default=False)),
                ('barType', models.CharField(max_length=20)),
                ('vendor', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CustomerProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('payment_info', models.OneToOneField(null=True, to='payments.Customer')),
                ('user', models.OneToOneField(related_name='user', null=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Deliveries',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('deliveryCompleted', models.BooleanField(default=False)),
                ('deliveryPerson', models.OneToOneField(null=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('eventName', models.CharField(max_length=250)),
                ('eventType', models.CharField(max_length=50)),
                ('eventDate', models.DateField()),
                ('eventTime', models.TimeField()),
                ('budget', models.DecimalField(max_digits=6, decimal_places=2)),
                ('totalCost', models.DecimalField(max_digits=6, decimal_places=2)),
                ('bar', models.ForeignKey(to='meHungry_customer_website.Bar')),
                ('customer', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FoodItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('itemName', models.CharField(max_length=30, null=True)),
                ('price', models.DecimalField(max_digits=6, decimal_places=2)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FoodOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order_price', models.DecimalField(null=True, max_digits=6, decimal_places=2)),
                ('delivery', models.BooleanField(default=False)),
                ('address_info', models.ForeignKey(to='meHungry_customer_website.Address', null=True)),
                ('charge_info', models.OneToOneField(null=True, to='payments.Charge')),
                ('customer', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
                ('orderItems', models.ManyToManyField(to='meHungry_customer_website.FoodItem', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('menuName', models.CharField(max_length=50, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('packageName', models.CharField(max_length=50)),
                ('packageCost', models.DecimalField(max_digits=6, decimal_places=2)),
                ('bar', models.ForeignKey(to='meHungry_customer_website.Bar')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PickUps',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pickUpPerson', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
                ('pickUpRestaurant', models.ForeignKey(to='meHungry_customer_website.FoodOrder', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('cuisine', models.CharField(max_length=15)),
                ('desc', models.TextField(max_length=250)),
                ('addressLine1', models.CharField(max_length=50)),
                ('addressLine2', models.CharField(max_length=50, blank=True)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=10)),
                ('delivery', models.BooleanField(default=False)),
                ('menu', models.OneToOneField(null=True, to='meHungry_customer_website.Menu')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='foodorder',
            name='restaurant',
            field=models.ForeignKey(to='meHungry_customer_website.Restaurant', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fooditem',
            name='menu',
            field=models.ForeignKey(to='meHungry_customer_website.Menu', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='package',
            field=models.ForeignKey(to='meHungry_customer_website.Package'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='deliveries',
            name='foodOrderInfo',
            field=models.ForeignKey(to='meHungry_customer_website.FoodOrder'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='address',
            name='customer_profile',
            field=models.ForeignKey(to='meHungry_customer_website.CustomerProfile'),
            preserve_default=True,
        ),
    ]
