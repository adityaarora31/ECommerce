from django.db import models

# Create your models here.


class ContactQuery(models.Model):
    name = models.CharField(max_length=60),
    email = models.EmailField(max_length=50),
    subject = models.CharField(max_length=30),
    query = models.TextField()
