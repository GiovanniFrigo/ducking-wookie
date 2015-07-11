# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.AlterField(
            model_name='booking',
            name='place',
            field=models.ForeignKey(to='core.Place'),
        ),
        migrations.AddField(
            model_name='menu',
            name='available_in',
            field=models.ManyToManyField(to='core.Place'),
        ),
    ]
