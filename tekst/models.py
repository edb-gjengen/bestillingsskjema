from bestilling.models import Order
from django.db import models


class TekstOrder(Order):
    text_type = models.CharField(max_length=50)
    length = models.CharField(max_length=50)
    image = models.CharField(max_length=50)
    interview_name = models.CharField(max_length=20)
    interview_contact = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)

