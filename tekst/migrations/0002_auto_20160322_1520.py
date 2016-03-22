# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tekst', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tekstorder',
            name='uuid',
            field=models.UUIDField(unique=True),
        ),
    ]
