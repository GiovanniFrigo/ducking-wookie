# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20150712_0529'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='confirmation_sent',
            field=models.BooleanField(default=False),
        ),
    ]
