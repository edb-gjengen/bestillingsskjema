# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prm', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prmorder',
            name='uuid',
            field=models.UUIDField(unique=True),
        ),
    ]
