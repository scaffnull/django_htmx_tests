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
                                      empty_label="Select Location",
            widget=forms.Select(attrs={"hx-get":"load_companies", "hx-target": "#id_company"}))
    company = forms.ModelChoiceField(queryset=Company.objects.none(),
                                     empty_label="Select Company",
            widget=forms.Select(attrs={"hx-get":"load_orderers", "hx-target": "#id_orderer"}))
    orderer = forms.ModelChoiceField(queryset=Orderer.objects.none(),
                                     empty_label="Select Orderer",
            widget=forms.Select(attrs={"hx-get":"selected_orderers", "hx-target":"#id_selected_orderer"})
                                    )
    selected_orderer = forms.ModelChoiceField(queryset=Orderer.objects.none(),
                                              widget=forms.HiddenInput(),
                                              required=False)
    order_number = forms.IntegerField(label="Order Number")
    order_for = forms.CharField(label="Order For", max_length=200)
    order_invoice = forms.CharField(label="Order Invoice", max_length=200)  

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "location" in self.data and "company" in self.data:
            location_id = int(self.data.get("location"))
            self.fields["company"].queryset = Company.objects.filter(location_id=location_id)
            company_id = int(self.data.get("company"))
            self.fields["orderer"].queryset = Orderer.objects.filter(company_id=company_id)
    
# FROM YOUTUBE: https://www.youtube.com/watch?v=UCl5O-XVChk&t=1s
    

