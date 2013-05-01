from bestilling.models import Order
from django.db import models

class PrmOrder(Order):
    assignment_type = models.CharField(max_length=50)
    content = models.TextField(blank=True, null=True)

