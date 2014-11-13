# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0003_forumrights'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='comment',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
