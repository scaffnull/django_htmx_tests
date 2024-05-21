from django.db.models.signals import post_save
from .models import Car, CarPool

def create_carpool_instance(sender, instance, created, **kwargs):
    if created: # if a new car is created, add to carpool
        city = instance.city
        CarPool.objects.create(car=instance, city=city)
post_save.connect(create_carpool_instance, sender=Car)