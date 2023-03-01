from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet

from logistic.models import Product, Stock, StockProduct
from logistic.serializers import ProductSerializer, StockSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter]
    #GET {{baseUrl}}/products/?search=помидор
    search_fields = ['description', 'title']


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Stock.objects.all()
        #GET {{baseUrl}}/stocks/?products=2
        products = self.request.query_params.get('products')
        if products is not None:
            queryset = queryset.filter(products=products)
        search = self.request.query_params.get('search')
        if search is not None:
            # запрос типа GET{{baseUrl}} / stocks /?products = 2
            product_id = Product.objects.all().filter(title__icontains=search).get().id # list of id product
            query_prod = StockProduct.objects.filter(product_id=product_id).all()
            list_stock_id = []
            for q in query_prod:
                list_stock_id.append(q.stock_id)
            queryset = queryset.filter(pk__in=list_stock_id)
        return queryset
