from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django_htmx.http import trigger_client_event
from .models import (
    City,
    Car,
    CarPool,
    Employee,
    Resturant,
    EmpPool)

# Create your views here.
def index(request):
    return render(request, 'htmx_tests/index.html')

"""Section Carpool test with HTMX"""
def car_pool(request):
    '''List all the cities'''
    cities = City.objects.all().order_by('city')
    cars = CarPool.objects.all()
    return render(request, 'partials/car_pool.html', {
        'cities':cities,
        'cars':cars,
    })


def car_pool_cars(request, pk):
    '''List all cars with no city, and also filtered cars when clicked
    from htmx and car_pool view
    '''
    cars = CarPool.objects.all().order_by('car__car_license_plate')
    city = get_object_or_404(City, pk=pk)
    car = CarPool.objects.filter(city=city).order_by('car__car_license_plate')
    context = {'cars':cars,'city':city,'car':car}
    return render(request, 'partials/car_pool_cars.html', context)


def car_pool_add(request, pk, city_id):
    '''Add a car with no cities to a city that is clicked'''
    city = get_object_or_404(City, pk=city_id)
    car = get_object_or_404(CarPool, pk=pk)
    if request.htmx:
        car.city = city
        car.save()
        return trigger_client_event(
            HttpResponse(''),
            "citySelected",
            after="swap")


def car_pool_remove(request, pk):
    '''Remove a car from a city'''
    car = get_object_or_404(CarPool, pk=pk)
    if request.htmx:
        car.city = None
        car.save()
        return trigger_client_event(
            HttpResponse(''),
            "citySelected",
            after="swap")


"""Section EmplPool test with HTMX
This is the same concept as the CarPool, but this uses a
FK and M2M in the model.
"""

def emp_pool(request):
    employees = Employee.objects.all().order_by('name')
    resturant = Resturant.objects.all().order_by('name')
    print(resturant)
    return render(request, 'partials/emp_pool.html', {
        'employees':employees,
        'resturant':resturant,
    })

def emp_pool_workers(request, pk):
    """List all emp workers that, and be able to add them to a resturant"""
    resturant = get_object_or_404(Resturant, pk=pk)
    employ = EmpPool.objects.exclude(resturant__name=resturant).order_by('employee__name')
    emp_filter = EmpPool.objects.filter(resturant=resturant).order_by('employee__name')
    context = {'resturant':resturant,'emp_filter':emp_filter,
               'employ':employ
               }
    return render(request, 'partials/emp_pool_workers.html', context)


def emp_pool_add(request, pk, rest_id):
    resturant = get_object_or_404(Resturant, pk=rest_id)
    emp = get_object_or_404(EmpPool, pk=pk)
    print(emp)
    if request.htmx:
        emp.resturant.set([resturant])
        emp.save()
        return trigger_client_event(
            HttpResponse(''),
            'resturantSelected',
            after="swap")

def emp_pool_remove(request, pk, rest_id):
    emp = get_object_or_404(EmpPool, pk=pk)
    print(emp.pk)
    resturant = get_object_or_404(Resturant, pk=rest_id)
    if request.htmx:
        emp.resturant.remove(resturant)
        emp.save()
        return trigger_client_event(
            HttpResponse(''),
            'resturantSelected',
            after="swap")

