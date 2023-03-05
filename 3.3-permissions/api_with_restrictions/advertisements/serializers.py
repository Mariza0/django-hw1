from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from advertisements.models import Advertisement, FavouriteAdv


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', 'draft')
        read_only_fields = ('creator',)

    def create(self, validated_data):
        """Метод для создания"""
        validated_data["creator"] = self.context["request"].user
        print(validated_data)
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""
        # у пользователя не больше 10 открытых объявлений
        quantity = Advertisement.objects.filter(creator_id=self.context["request"].user.id).all()
        q = quantity.filter(status='OPEN').count()
        if q >= 10 and data.get('status') != 'CLOSED' and self.context.get('request').method == 'POST':
            raise ValidationError("Количество объявлений достигло 10")
        return data


class FavouriteAdvSerializer(serializers.ModelSerializer):
    fav_adv = AdvertisementSerializer(read_only=True)

    class Meta:
        model = FavouriteAdv
        fields = ('id', 'fav_adv', )

    def create(self, validated_data):
        """Метод для создания"""

        validated_data["user"] = self.context["request"].user
        fav_adv_id=self.initial_data.get('fav_adv')
        if Advertisement.objects.filter(creator_id=validated_data["user"].id).filter(id=fav_adv_id):
            raise ValidationError('вы не можете добавить в избранное свое объявление')
        fav, created = FavouriteAdv.objects.get_or_create(fav_adv_id=fav_adv_id,
                                                             user_id=validated_data["user"].id
                                                             )
        return fav
