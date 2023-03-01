
from rest_framework import serializers
from logistic.models import Product, StockProduct, Stock


class ProductSerializer(serializers.ModelSerializer):
    # настройте сериализатор для продукта
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']


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
        #print('self.request.context', StockSerializer.fields)
        positions = validated_data.pop('positions')
        # создаем склад по его параметрам
        stock = super().create(validated_data)
        for pos in positions:
            # здесь вам надо заполнить связанные таблицы
            # в нашем случае: таблицу StockProduct
            pos['stock_id'] = stock.id
            values_for_update = pos
            defaults = {'price': values_for_update.get('price'), 'quantity': values_for_update.get('quantity')}
            stockProduct, created = StockProduct.objects.update_or_create(stock_id=stock.id,
                                                                          product_id=values_for_update.get('product').id,
                                                                          defaults=defaults)

        return stock

    def update(self, instance, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')
        # обновляем склад по его параметрам
        stock = super().update(instance, validated_data)
        for pos in positions:
            # обновляем таблицу stockproduct
            values_for_update = pos
            defaults = {'price': values_for_update.get('price'), 'quantity': values_for_update.get('quantity')}
            stockProduct, created = StockProduct.objects.update_or_create(stock_id=stock.id,
                                                                          product_id=values_for_update.get('product').id,
                                                                          defaults=defaults)

        return stock
