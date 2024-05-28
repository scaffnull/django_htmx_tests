from django_filters import FilterSet, ModelChoiceFilter, OrderingFilter

from .models import (
    Category,
    SocialMedia
)

class CategoryFilter(FilterSet):
    """Filter on category in Socialmediauser list"""
    category = ModelChoiceFilter(
                    queryset=Category.objects.all().order_by('name'),
                    empty_label="All Categories",
                    label="Category")
    # order_by = OrderingFilter(
    #     fields=('category__name',),
    # )
    class Meta:
        model = SocialMedia
        fields = ['category',]
