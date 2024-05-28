from django_filters import FilterSet, ModelChoiceFilter

from .models import (
    Category,
    SocialMedia
)

class CategoryFilter(FilterSet):
    """Filter on category in Socialmediauser list"""
    category = ModelChoiceFilter(
                    queryset=Category.objects.all(),
                    empty_label="All Categories",
                    label="Category")
    class Meta:
        model = SocialMedia
        fields = ['category',]
        order_by = ('name',)
