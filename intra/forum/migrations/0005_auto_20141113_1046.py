# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0004_post_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='comment',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
