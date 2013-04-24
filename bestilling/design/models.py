from django.db import models

class DesignOrder(models.Model):
    client = models.CharField(max_length=50)
    deadline = models.DateField()
    contact_name = models.CharField(max_length=50)
    contact_email = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    format_type = models.CharField(max_length=50)
    paper_size = models.CharField(max_length=50)
    colour = models.CharField(max_length=50)
    marger = models.CharField(max_length=50)
    content = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    trello_card_id = models.CharField(max_length=40)
