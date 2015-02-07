# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meHungry_customer_website', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='apt',
            field=models.CharField(max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
    ]
