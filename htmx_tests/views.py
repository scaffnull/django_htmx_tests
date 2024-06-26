from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django_htmx.http import trigger_client_event
from django.views.generic.edit import CreateView, UpdateView
from .forms import NewOrderForm
from .models import (
    City,
    Car,
    CarPool,
    Employee,
    Resturant,
    EmpPool,
    SocialMedia,
    Category,
    Location,
    Company,
    Orderer,
    OrderSummary)
from .filters import CategoryFilter

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
        emp.resturant.add(resturant)
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

""" END SECTION"""

"""
SECTION SOCIAL MEDIA, use with bool field, either follow or not follow from a list 
with a click
"""

'''
#TODO: Fix the issue when no category is selected and follow/unfollow htmx request is made
Right now it returns the filtered result (which works if there is a category filtered)
'''

def social_media(request):
    category_filter = CategoryFilter(request.GET,
                            queryset=SocialMedia.objects.none().order_by('name'))
    social = category_filter.qs
    selected_value = category_filter.data.get('category')
    print(selected_value)
    if request.GET:
        category_filter = CategoryFilter(request.GET,
                                         queryset=SocialMedia.objects.order_by('name'))
        social = category_filter.qs
        following_count = social.filter(is_following=True).count()
    #Making sure the following count only is showing True results
    following_count = social.filter(is_following=True).count()
    return render(request, 'partials/social_media.html', {
        'form':category_filter.form,
        'social': social,
        'following_count':following_count,
    })

def social_media_list(request, selected_value):
    category_filter = CategoryFilter(request.GET,
                            queryset=SocialMedia.objects.none().order_by('name'))
    selected_value = category_filter.data.get('category')   
    social = SocialMedia.objects.filter(category=selected_value)
    return render(request, 'partials/social_media_htmx.html', {
        'social':social,
    })   

def social_media_unfollow(request, pk):
    name = get_object_or_404(SocialMedia, pk=pk)
    if request.htmx:
        name.is_following = False
        name.save()
        social = SocialMedia.objects.filter(category=name.category).order_by('name')
        following_count = social.filter(is_following=True).count()
        return render(request, 'partials/social_media_htmx.html', {
            'social':social,
            'following_count':following_count
        })

def social_media_follow(request, pk):
    name = get_object_or_404(SocialMedia, pk=pk)
    print(name)
    if request.htmx:
        name.is_following = True
        name.save()
        social = SocialMedia.objects.filter(category=name.category).order_by('name')
        following_count = social.filter(is_following=True).count()
        return render(request, 'partials/social_media_htmx.html', {
            'social':social,
            'following_count':following_count
        })

'''
END SOCIAL MEDIA SECTION
'''


'''
SECTION ORDERS
'''

def location_list(request):
    location = Location.objects.all().order_by('place')
    count = location.count()
    return render(request, 'htmx_tests/location.html', {
        'location':location,
        'count':count,
    })

class LocationCreate(CreateView):
    model = Location
    template_name = 'htmx_tests/location_create.html'
    fields = '__all__'
    success_url = reverse_lazy('htmx_tests:location_list')

class LocationEdit(UpdateView):
    model = Location
    template_name = 'htmx_tests/location_edit.html'
    fields = '__all__'
    success_url = reverse_lazy('htmx_tests:location_list')


def company_list(request):
    company = Company.objects.all().order_by('name')
    count = company.count()
    return render(request, 'htmx_tests/company.html', {
        'company':company,
        'count':count,
    })

class CompanyCreate(CreateView):
    model = Company
    template_name = 'htmx_tests/company_create.html'
    fields = '__all__'
    success_url = reverse_lazy('htmx_tests:company_list')

class CompanyEdit(UpdateView):
    model = Company
    template_name = 'htmx_tests/company_edit.html'
    fields = '__all__'
    success_url = reverse_lazy('htmx_tests:company_list')


def orderer_list(request):
    orderer = Orderer.objects.all().order_by('company__name')
    count = orderer.count()
    return render(request, 'htmx_tests/orderer.html', {
        'orderer':orderer,
        'count':count,
    })

class OrdererCreate(CreateView):
    model = Orderer
    template_name = 'htmx_tests/orderer_create.html'
    fields = '__all__'
    success_url = reverse_lazy('htmx_tests:orderer_list')

class OrdererEdit(UpdateView):
    model = Orderer
    template_name = 'htmx_tests/orderer_edit.html'
    fields = '__all__'
    success_url = reverse_lazy('htmx_tests:orderer_list')


def order_summary_list(request):
    order_summary = OrderSummary.objects.all().order_by('order_number')
    count = order_summary.count()
    return render(request, 'htmx_tests/order_summary.html',{
        'order_summary':order_summary,
        'count':count,
    })

class OrderSummaryEdit(UpdateView):
    model = OrderSummary
    template_name = 'htmx_tests/order_summary_edit.html'
    fields = '__all__'
    success_url = reverse_lazy('htmx_tests:order_summary_list')

def order_summary_history(request, orderer_id):
    """OrderSummary history table"""
    ordersummary = OrderSummary.objects.get(pk=orderer_id)
    ch = ordersummary.history.all()
    # To fetch the history
    changes = []
    if ch is not None and orderer_id:
        last = ch.first()
        for all_changes in range(ch.count()):
            new_record, old_record = last, last.prev_record
            if old_record is not None:
                delta = new_record.diff_against(old_record)
                changes.append(delta)
            last = old_record

    return render(request, 'htmx_tests/order_summary_history.html', {
        'ordersummary':ordersummary,
        'ch':ch,
        'changes':changes,
    })

def new_order(request):
    form = NewOrderForm(request.POST or None)
    if request.POST and form.is_valid():
        form.save()
        return redirect('htmx_tests:order_summary_list')
    return render(request, 'htmx_tests/new_order.html', {
        'form':form,
    })

def load_companies(request):
    location_id = request.GET.get('location')
    companies = Company.objects.filter(location_id=location_id)
    return render(request, 'partials/option_companies.html', {
        'companies':companies,
    })

def load_orderers(request):
    company_id = request.GET.get('company')
    orderers = Orderer.objects.filter(company_id=company_id)
    return render(request, 'partials/option_orderers.html', {
        'orderers':orderers,
    })

# NOT OPTIMAL BUT MAKES THE ORDERS WORK?
# What happens is that I fecth this from the forms.py and have it hidden,
# just to keep the lists available still in "Create New Order"
def selected_orderers(request):
    orderer_id = request.GET.get('orderer')
    order = Orderer.objects.get(pk=orderer_id)
    return render(request, 'partials/orderer_selected.html', {
        'order':order,
    })

'''
END ORDERS SECTION
'''