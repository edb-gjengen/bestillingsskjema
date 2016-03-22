# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TekstOrder',
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
                ('text_type', models.CharField(max_length=50)),
                ('length', models.CharField(max_length=50)),
                ('image', models.CharField(max_length=50)),
                ('interview_name', models.CharField(max_length=20)),
                ('interview_contact', models.TextField(null=True, blank=True)),
                ('content', models.TextField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
