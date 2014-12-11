# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tickets', '0003_auto_20141205_1629'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='last_assigned',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='last_assigned', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ticket',
            name='last_event_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ticket',
            name='last_status',
            field=models.IntegerField(null=True, choices=[(0, 'Opened'), (1, 'Closed')], blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='assign',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='message',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='status',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ticket',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
    ]
