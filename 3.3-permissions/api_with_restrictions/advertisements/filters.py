from django_filters import rest_framework as filters, DateFromToRangeFilter
from django_filters.rest_framework import DjangoFilterBackend
from advertisements.models import Advertisement, FavouriteAdv


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""
    created_at = DateFromToRangeFilter()
    creator = DjangoFilterBackend()
    class Meta:
        model = Advertisement
        fields = ["creator", "created_at", "status"]


class FavouriteAdvFilter(filters.FilterSet):
    """Фильтры для объявлений."""
    class Meta:
        model = FavouriteAdv
        fields = ["user", ]