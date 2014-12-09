# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0007_auto_20141208_1720'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='has_module_perms',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
