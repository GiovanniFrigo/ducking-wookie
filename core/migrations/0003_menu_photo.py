# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_menu_available_number_per_day'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='photo',
            field=models.ImageField(upload_to=b'', blank=True),
        ),
    ]
