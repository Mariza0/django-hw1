from django.conf import settings
from django.db import models


class AdvertisementStatusChoices(models.TextChoices):
    """Статусы объявления."""

    OPEN = "OPEN", "Открыто"
    CLOSED = "CLOSED", "Закрыто"


class Advertisement(models.Model):
    """Объявление."""

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

    def __str__(self):
        return str(self.id) + " " + self.creator #+ " " + self.status

class FavouriteAdv(models.Model):
    """ избранные объявления"""
    fav_adv = models.ForeignKey(Advertisement, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return "у пользователя " + str(self.user) + " избранное: " + self.fav_adv