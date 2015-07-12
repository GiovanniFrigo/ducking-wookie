# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_menu_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='transaction_id',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='cook',
            field=models.ForeignKey(blank=True, to='core.Cook', null=True),
        ),
    ]
