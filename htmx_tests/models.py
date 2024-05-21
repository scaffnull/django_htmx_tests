from django.db import models

# Create your models here.

'''
SECTION FOR THE CARPOOL TEST
'''

class City(models.Model):
    """
    City for where the cars will be located
    """
    city = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return self.city

class CarType(models.Model):
    """What type of car it is"""
    name = models.CharField(max_length=100, unique=True, verbose_name="Car Type")

    def __str__(self):
        return self.name
    
class Car(models.Model):
    """
    Car register with all the cars
    """
    car_license_plate = models.CharField(max_length=30, unique=True,
                                         verbose_name="License Plate")
    car_type = models.ForeignKey(CarType, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return self.car_license_plate
    
class CarPool(models.Model):
    """
    Car pool model, 
    """
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.car.car_license_plate} - {self.city}"

'''
END CARPOOL TEST SECTION
''' 
