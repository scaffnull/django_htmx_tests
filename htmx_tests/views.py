from django.shortcuts import render, get_object_or_404
from .models import City, Car, CarPool

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
    print(city)
    context = {'cars':cars,'city':city,'car':car}
    return render(request, 'partials/car_pool_cars.html', context)


def car_pool_add(request, pk, city_id):
    '''Add a car with no cities to a city that is clicked'''
    city = get_object_or_404(City, pk=city_id)
    car = get_object_or_404(CarPool, pk=pk)
    car.city = city
    car.save()
    return render(request, 'partials/added_cars.html', {
        'car':car,
    })

def car_pool_remove(request, pk):
    '''Remove a car from a city'''
    car = get_object_or_404(CarPool, pk=pk)
    car.city = None
    car.save()
    return render(request, 'partials/filter_cars.html', {
        'car':car,
    })
