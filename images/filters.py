from django_filters import rest_framework as filters
from .models import ImageItem


class ImageItemFilter(filters.FilterSet):
    uploaded_at = filters.DateFromToRangeFilter()  # фильтр диапазона даты

    class Meta:
        model = ImageItem
        fields = ['uploaded_at']
