from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView

from .serializers import CategorySerializer, ProductSerializer, PVZSerializer, CDEKCitySerializer, \
    RussianPostDeliverySerializer
from ..models import Category, Product, CDEK_PVZ, CDEKCities, RussianPostDelivery


class CategoryListApiView(ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class ProductListApiView(ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['price', 'title']


class PVZCDEKListApiView(ListAPIView):
    serializer_class = PVZSerializer
    queryset = CDEK_PVZ.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['city__title']


class CDEKCityListApiView(ListAPIView):
    serializer_class = CDEKCitySerializer
    queryset = CDEKCities.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['title']


class RussianPostDeliveryListApiView(ListAPIView):
    serializer_class = RussianPostDeliverySerializer
    queryset = RussianPostDelivery.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['region']
