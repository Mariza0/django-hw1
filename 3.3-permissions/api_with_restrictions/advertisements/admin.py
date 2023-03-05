from django.contrib import admin

from advertisements.models import AdvertisementStatusChoices, Advertisement, FavouriteAdv


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'creator', 'created_at']


@admin.register(FavouriteAdv)
class FavouriteAdvAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'fav_adv',]

