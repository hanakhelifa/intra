# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0008_myuser_has_module_perms'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='has_module_perms',
        ),
    ]
