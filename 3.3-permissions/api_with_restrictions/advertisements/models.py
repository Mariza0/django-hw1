from django.conf import settings
from django.db import models


class AdvertisementStatusChoices(models.TextChoices):
    """Статусы объявления."""

    class Meta:
        verbose_name = 'статус объявления'


    OPEN = "OPEN", "Открыто"
    CLOSED = "CLOSED", "Закрыто"


class Advertisement(models.Model):
    """Объявление."""
    class Meta:
        verbose_name = 'объявление'
        verbose_name_plural = 'объявления'

    title = models.TextField()
    description = models.TextField(default='')
    status = models.TextField(
        choices=AdvertisementStatusChoices.choices,
        default=AdvertisementStatusChoices.OPEN
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )
    draft = models.BooleanField(default=True)

    def __str__(self):
        return "id: " + str(self.id) + ", title: " + str(self.title) + ", description: " + self.description


class FavouriteAdv(models.Model):
    """ избранные объявления"""
    class Meta:
        verbose_name = 'избранное'
        verbose_name_plural = 'избранные'

    fav_adv = models.ForeignKey(Advertisement, related_name='adv', on_delete=models.CASCADE, verbose_name='обявление')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)

    def __str__(self):
        return str(self.user)