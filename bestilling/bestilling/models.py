from django.db import models
from django_extensions.db.fields import UUIDField
import uuid

class Order(models.Model):
    uuid = UUIDField(unique=True, auto=True, version=1) # version 1 guarantees no collisions
    client = models.CharField(max_length=50)
    deadline = models.DateField()
    contact_name = models.CharField(max_length=50)
    contact_email = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    trello_card_id = models.CharField(max_length=40)

    class Meta:
        abstract = True

