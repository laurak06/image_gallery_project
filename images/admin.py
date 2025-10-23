from django.contrib import admin
from rangefilter.filters import DateRangeFilter
from .models import ImageItem


@admin.register(ImageItem)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'image_url', 'uploaded_at')       # колонки в списке
    search_fields = ('title',)                  # поиск по названию
    list_filter = (
        ('uploaded_at', DateRangeFilter),  # фильтр по диапазону
    )
