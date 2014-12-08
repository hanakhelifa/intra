# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0002_auto_20141203_1316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='birth_date',
            field=models.DateField(null=True),
            preserve_default=True,
        ),
    ]
