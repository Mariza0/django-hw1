
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from advertisements.filters import AdvertisementFilter, FavouriteAdvFilter
from advertisements.models import Advertisement, FavouriteAdv
from advertisements.permissions import IsOwnerOrReadOnly, IsOwnerOrReadOnlyFavourites
from advertisements.serializers import AdvertisementSerializer, FavouriteAdvSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    def get_queryset(self):
        print(self.action)
        if self.action in ['retrieve', 'list']:
            query = Advertisement.objects.filter(creator_id=self.request.user.id).filter(draft=True)|\
                    Advertisement.objects.filter(draft=False)
            return query
        else:
            return Advertisement.objects.all()

    serializer_class = AdvertisementSerializer
    filterset_class = AdvertisementFilter

    @action(detail=False, methods=['get'])
    def favourites(self, request, pk=None):
        """ получение списка избранных объявлений по доп. ссылке /advertisements/favourites"""
        fav = FavouriteAdv.objects.select_related('fav_adv').filter(user_id=self.request.user.id).all()
        serializer = FavouriteAdvSerializer(fav, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "destroy", "partial_update"]:
            if self.request.user.is_superuser:
                return [IsAuthenticated()]
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
        return []


class FavouriteAdvViewSet(ModelViewSet):
    """ избранные объявления"""
    queryset = FavouriteAdv.objects.all()
    filterset_class = FavouriteAdvFilter
    serializer_class = FavouriteAdvSerializer
    http_method_names = ["post", "patch", "delete", "head"]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "destroy", "partial_update"]:
            if self.request.user.is_superuser:
                return [IsAuthenticated()]
            return [IsAuthenticated(), IsOwnerOrReadOnlyFavourites()]
        return []