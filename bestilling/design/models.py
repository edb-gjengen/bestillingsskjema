from bestilling.models import Order
from django.db import models

class DesignOrder(Order):
    format_type = models.CharField(max_length=50)
    paper_size = models.CharField(max_length=50)
    colour = models.CharField(max_length=50)
    marger = models.CharField(max_length=50)
    content = models.TextField(blank=True, null=True)

