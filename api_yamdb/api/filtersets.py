from django_filters import rest_framework as filters
from reviews.models import Title


class TitleFilter(filters.FilterSet):
    """
    Фильтр для модели Title, позволяющий фильтровать
    по жанру, категории, году и имени
    """
    genre = filters.CharFilter(field_name='genre__slug',
                               lookup_expr='exact')
    category = filters.CharFilter(field_name='category__slug',
                                  lookup_expr='exact')
    year = filters.NumberFilter(field_name='year')
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Title
        fields = ['genre', 'category', 'year', 'name']
