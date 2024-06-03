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
    path("emp_pool/<int:pk>/<int:rest_id>/remove/", views.emp_pool_remove, name="emp_pool_remove"),
    # SOC MEDIA
    path("social_media/", views.social_media, name="social_media"),
    path("social_media_list/", views.social_media_list, name="social_media_list"),
    path("social_media/unfollow/<int:pk>/", views.social_media_unfollow, name="social_media_unfollow"),
    path("social_media/follow/<int:pk>/", views.social_media_follow, name="social_media_follow"),

    # ORDERERS
    path("location_list/", views.location_list, name="location_list"),
    path("location_create", views.LocationCreate.as_view(), name="location_create"),
    path("location_edit/<int:pk>/", views.LocationEdit.as_view(), name="location_edit"),
    path("company_list/", views.company_list, name="company_list"),
    path("company_create/", views.CompanyCreate.as_view(), name="company_create"),
    path("company_edit/<int:pk>/", views.CompanyEdit.as_view(), name="company_edit"),
    path("orderer_list/", views.orderer_list, name="orderer_list"),
    path("orderer_create", views.OrdererCreate.as_view(), name="orderer_create"),
    path("orderer_edit/<int:pk>/", views.OrdererEdit.as_view(), name="orderer_edit"),
    path("order_summary_list/", views.order_summary_list, name="order_summary_list"),
]
