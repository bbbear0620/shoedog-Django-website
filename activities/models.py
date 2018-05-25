from django.db import models

# Create your models here.
class Activity(models.Model):
    name = models.CharField(max_length=50)
    palace = models.CharField(max_length=100,default='Not Know')
    detail = models.TextField()
    start_time = models.DateField()
    end_time = models.DateField()
