
from rest_framework import serializers
from logistic.models import Product, StockProduct, Stock


class ProductSerializer(serializers.ModelSerializer):
    # настройте сериализатор для продукта
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']


# class FilteredListSerializer(django_filters.FilterSet):
#
#     def to_representation(self, data):
#         data = data.filter(product=self.context['request'].product, edition__hide=False)
#         return super(FilteredListSerializer, self).to_representation(data)


class ProductPositionSerializer(serializers.ModelSerializer):
    # настройте сериализатор для позиции продукта на складе
    class Meta:
        model = StockProduct
        #list_serializer_class = FilteredListSerializer
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)
    # настройте сериализатор для склада
    class Meta:
        model = Stock
        fields =['id', 'address', 'positions']

    def create(self, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # создаем склад по его параметрам
        stock = super().create(validated_data)
        # здесь вам надо заполнить связанные таблицы
        # в нашем случае: таблицу StockProduct
        positions[0]['stock_id'] = stock.id
        values_for_update = positions[0]
        print('values_for_update',values_for_update)
        stockProduct, created = StockProduct.objects.update_or_create(
            id=values_for_update.get('product.id'), defaults=values_for_update)

        return stock

    def update(self, instance, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')
        # обновляем склад по его параметрам
        stock = super().update(instance, validated_data)
        # обновляем таблицу stockproduct
        values_for_update = positions[0]
        stockProduct, created = StockProduct.objects.update_or_create(id=values_for_update.get('product.id'),
                                                                      defaults=values_for_update)

        return stock
