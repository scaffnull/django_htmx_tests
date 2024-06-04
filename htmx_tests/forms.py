from django import forms
from .models import Location, Company, Orderer, OrderSummary
from dynamic_forms import DynamicField, DynamicFormMixin


class OrderForm(DynamicFormMixin, forms.Form):
    """Order form for a new Order"""

    def module_choices(form):
        location = form['location'].value()
        return Company.objects.filter(location=location)
    
    def initial_module(form):
        location = form['location'].value()
        return Company.objects.filter(location=location)


    location = forms.ModelChoiceField(
        queryset=Location.objects.all().order_by('place'),
        label="Location",
        empty_label="All Locations"
    )

    companies = DynamicField(
        forms.ModelChoiceField,
        queryset=module_choices,
        initial=initial_module,
    )

class NewOrderForm(forms.Form):
    location = forms.ModelChoiceField(queryset=Location.objects.all().order_by('place'),
            widget=forms.Select(attrs={"hx-get":"load_companies", "hx-target": "#id_company"}))
    company = forms.ModelChoiceField(queryset=Company.objects.none(),
            widget=forms.Select(attrs={"hx-get":"load_orderers", "hx-target": "#id_orderer"}))
    orderer = forms.ModelChoiceField(queryset=Orderer.objects.none())
    
    


# FROM YOUTUBE: https://www.youtube.com/watch?v=UCl5O-XVChk&t=1s