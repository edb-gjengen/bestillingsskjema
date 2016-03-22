import uuid

from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.contrib.contenttypes.models import ContentType

from bestilling.utils import validate_file_extension


class Attachment(models.Model):

    _limit_order_choices = models.Q(app_label='design', model='designorder') \
        | models.Q(app_label='tekst', model='tekstorder') \
        | models.Q(app_label='prm', model='prmorder')

    uploaded_file = models.FileField(upload_to='uploads', validators=[validate_file_extension])
    trello_id = models.CharField(max_length=40, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    content_type = models.ForeignKey(ContentType, limit_choices_to=_limit_order_choices)
    object_id = models.PositiveIntegerField()
    order_object = GenericForeignKey('content_type', 'object_id')


class Order(models.Model):
    # uuid = UUIDField(unique=True, auto=True, version=1)  # version 1 guarantees no collisions
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)  # auto=True, version=1
    client = models.CharField(max_length=50)
    deadline = models.DateField()
    contact_name = models.CharField(max_length=50)
    contact_email = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    trello_card_id = models.CharField(max_length=40)

    class Meta:
        abstract = True


