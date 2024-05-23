from django.urls import path
from . import views

app_name = 'htmx_tests'

urlpatterns = [
    path('', views.index, name="index"),
    #CAR POOL
    path('car_pool/', views.car_pool, name="car_pool"),
    path('car_pool/<int:pk>/', views.car_pool_cars, name="car_pool_cars"),
    path('car_pool/<int:pk>/<int:city_id>/add/', views.car_pool_add, name="car_pool_add"),
    path('car_pool/<int:pk>/remove/', views.car_pool_remove, name="car_pool_remove"),
    # EMP POOL
    path("emp_pool/", views.emp_pool, name="emp_pool"),
    path("emp_pool/<int:pk>/", views.emp_pool_workers, name="emp_pool_workers"),
    path("emp_pool/<int:pk>/<int:rest_id>/add/", views.emp_pool_add, name="emp_pool_add"),
    path("emp_pool/<int:pk>/remove/", views.emp_pool_remove, name="emp_pool_remove"),
]
