from django.db import models
from simple_history.models import HistoricalRecords

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

class Category(models.Model):
    """What category the person is active in"""
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class SocialMedia(models.Model):
    """Social media, active/inactive following list"""
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    is_following = models.BooleanField(default=True)

    def __str__(self):
        return self.name


'''
END SOCIAL MEDIA SECTION
'''


'''
SECTION FOR ORDERS
'''
class Location(models.Model):
    place = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.place

class Company(models.Model):
    name = models.CharField(max_length=50)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Orderer(models.Model):
    orderer = models.CharField(max_length=50)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.orderer

class OrderSummary(models.Model):
    order_number = models.IntegerField()
    order_for = models.CharField(max_length=200)
    order_invoice = models.CharField(max_length=200)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    orderer = models.ForeignKey(Orderer, on_delete=models.CASCADE)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.order_number}: {self.location.place}"
    
    class Meta:
        """Make sure order_number can not same for the same location, but can be
        same but for other locations"""
        unique_together = ('location', 'order_number')

class OrderInvoice(models.Model):
    """From the created orders, a feature to invoice the order"""
    ordersummary = models.ForeignKey(OrderSummary, on_delete=models.CASCADE)
    invoice_date = models.DateField()
    invoice_hours = models.IntegerField(null=True)
    invoice_comment = models.CharField(max_length=200)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.ordersummary.order_number}: {self.ordersummary.orderer}: {self.ordersummary.company} {self.invoice_date}"

'''
END ORDERS SECTION
'''