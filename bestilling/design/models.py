from bestilling.models import Order
from django.db import models

class DesignOrder(Order):
    PAPER_SIZES = [
        ('A1', 'A1 (594 x 841 mm)'),
        ('A2', 'A2 (420 x 594 mm)'),
        ('B3', 'B3 (353 x 500 mm)'),
        ('A3', 'A3 (297 x 420 mm)'),
        ('A4', 'A4 (210 x 297 mm)'),
        ('A5', 'A5 (148 x 210 mm)'),
        ('A6', 'A6 (105 x 148 mm)'),
    ]

    FORMATS = [
        ('Trykk - Flyer', 'Trykk - Flyer'),
        ('Trykk - Plakat', 'Trykk - Plakat'),
        ('Trykk - Banner', 'Trykk - Banner'),
        ('Web - Annonse', 'Web - Annonse'),
        ('Web - Banner', 'Web - Banner'),
        ('Web - Bilde', 'Web - Bilde'),
    ]

    format_type = models.CharField(max_length=50, choices=FORMATS)
    paper_size = models.CharField(max_length=50, choices=PAPER_SIZES)
    colour = models.CharField(max_length=50)
    marger = models.CharField(max_length=50)
    content = models.TextField(blank=True, null=True)

