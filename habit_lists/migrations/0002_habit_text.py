# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('habit_lists', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='habit',
            name='text',
            field=models.TextField(default=''),
        ),
    ]
