from django.db import models

# Create your models here.


class PropertyDetail(models.Model):
    property_name = models.CharField(max_length=128)
    address = models.CharField(max_length=256)
    city = models.CharField(max_length=128)
    state = models.CharField(max_length=128)