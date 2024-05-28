from django.contrib import admin
from .models import (
    City,
    Car,
    CarPool, 
    CarType, 
    Employee, 
    EmpPool, 
    Resturant,
    SocialMedia,
    Category)
# Register your models here.

admin.site.register(City)
admin.site.register(Car)
admin.site.register(CarPool)
admin.site.register(CarType)
admin.site.register(Employee)
admin.site.register(EmpPool)
admin.site.register(Resturant)
admin.site.register(SocialMedia)
admin.site.register(Category)
