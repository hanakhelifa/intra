# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tickets', '0002_message_ticket'),
    ]

    operations = [
        migrations.AddField(
            model_name='assign',
            name='assigned_to',
            field=models.ForeignKey(related_name='assigned_to', to=settings.AUTH_USER_MODEL, default=None),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='assign',
            name='author',
            field=models.ForeignKey(related_name='assigned_by', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
