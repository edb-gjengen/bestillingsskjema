# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import bestilling.utils


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('uploaded_file', models.FileField(validators=[bestilling.utils.validate_file_extension], upload_to='uploads')),
                ('trello_id', models.CharField(null=True, max_length=40, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
        ),
    ]
