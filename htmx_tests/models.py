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


'''
SECTION FOR RESTURANT WORKERS
'''

class Employee(models.Model):
    """Name of the employee"""
    name = models.CharField(max_length=100)
    start_date = models.DateField()

    def __str__(self):
        return self.name

class Resturant(models.Model):
    """Name of the resturant where employee works"""
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name
    

class EmpPool(models.Model):
    """Employee pool, one employee can be working at many resturants at the same time"""
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    resturant = models.ManyToManyField(Resturant, blank=True)

    def __str__(self):
        return f"{self.employee.name}"


'''
END RESTURANT WORKERS SECTION
'''

'''
SECTION FOR SOCIAL MEDIA
'''

class SocialMedia(models.Model):
    """Social media, active/inactive following list"""
    name = models.CharField(max_length=255)
    is_following = models.BooleanField(default=True)

    def __str__(self):
        return self.name


'''
END SOCIAL MEDIA SECTION
'''