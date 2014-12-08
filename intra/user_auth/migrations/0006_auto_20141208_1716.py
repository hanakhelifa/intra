# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0005_myuser_is_staff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='is_staff',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
