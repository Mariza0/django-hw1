from django.contrib.auth.models import User
from rest_framework import serializers

from advertisements.models import Advertisement


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
                  'status', 'created_at', )
        read_only_fields = ('creator',)

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        print('validated_data', validated_data) #admin
        print('context', self.context)
        print('user', self.context["request"].user) #admin
        validated_data["creator"] = self.context["request"].user
        validated_data.pop("user")
        print('validated_data', validated_data)
        return super().create(validated_data)

    # def validate(self, data):
    #     """Метод для валидации. Вызывается при создании и обновлении."""
    #
    #     # TODO: добавьте требуемую валидацию
    #     # у пользователя не больше 10 открытых объявлений
    #     print(data)
    #     return data
