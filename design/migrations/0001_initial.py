# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DesignOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('uuid', django_extensions.db.fields.UUIDField(editable=False, version=1, blank=True, unique=True)),
                ('client', models.CharField(max_length=50)),
                ('deadline', models.DateField()),
                ('contact_name', models.CharField(max_length=50)),
                ('contact_email', models.CharField(max_length=50)),
                ('contact_number', models.CharField(null=True, max_length=20, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('trello_card_id', models.CharField(max_length=40)),
                ('format_type', models.CharField(choices=[('Trykk - Flyer', 'Trykk - Flyer'), ('Trykk - Plakat', 'Trykk - Plakat'), ('Trykk - Banner', 'Trykk - Banner'), ('Web - Annonse', 'Web - Annonse'), ('Web - Banner', 'Web - Banner'), ('Web - Bilde', 'Web - Bilde')], max_length=50)),
                ('paper_size', models.CharField(choices=[('A1', 'A1 (594 x 841 mm)'), ('A2', 'A2 (420 x 594 mm)'), ('B3', 'B3 (353 x 500 mm)'), ('A3', 'A3 (297 x 420 mm)'), ('A4', 'A4 (210 x 297 mm)'), ('A5', 'A5 (148 x 210 mm)'), ('A6', 'A6 (105 x 148 mm)')], max_length=50)),
                ('colour', models.CharField(max_length=50)),
                ('marger', models.CharField(max_length=50)),
                ('content', models.TextField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
