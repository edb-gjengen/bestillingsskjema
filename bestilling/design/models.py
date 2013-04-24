from django.db import models

# Create your models here.
class DesignOrder(models.Model):
    client = models.CharField(max_length=50)
    deadline = models.DateField()
    contact_name = models.CharField(max_length=50)
    contact_email = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=20)
    format = models.CharField(max_length=50)
    format_other = models.CharField(max_length=50)
    paper_size = models.CharField(max_length=50)
    paper_size_other = models.CharField(max_length=50)
    colour = models.CharField(max_length=50)
    marger = models.CharField(max_length=50)
    content = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
