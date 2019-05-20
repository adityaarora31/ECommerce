from django.db import models
from BestStore.user_master.models import Merchant

CATEGORY_CHOICES = (
    ('General', 'General'),
    ('Mobile', 'Mobile'),
    ('Men Fashion', 'Men Fashion'),
    ('Women Fashion', 'Women Fashion'),
    ('Sport', 'Sport'),
    ('Toy', 'Toy'),
    ('Computer', 'Computer'),
)


class Product(models.Model):
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='General')
    description = models.CharField(max_length=100)
    price = models.IntegerField(max_length=10)
    quantity = models.IntegerField(max_length=100)
    image_1 = models.ImageField()
    image_2 = models.ImageField()
    image_3 = models.ImageField()
    image_4 = models.ImageField()