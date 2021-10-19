from rest_framework import serializers

from ..models import Category, Product, CDEK_PVZ, CDEKCities, RussianPostDelivery


class CategorySerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)
    slug = serializers.SlugField()

    class Meta:
        model = Category
        fields = [
            'id', 'title', 'slug'
        ]


class ProductSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)
    price = serializers.DecimalField(max_digits=9, decimal_places=2)
    slug = serializers.SlugField()

    class Meta:
        model = Product
        fields = [
            'id', 'title', 'price', 'slug'
        ]


class PVZSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    title = serializers.CharField(required=True)
    city = serializers.CharField(required=True)
    address = serializers.CharField(required=True)
    code = serializers.CharField(required=True)
    work_time = serializers.CharField(required=True)
    longitude = serializers.FloatField(required=True)
    latitude = serializers.FloatField(required=True)

    class Meta:
        model = CDEK_PVZ
        fields = [
            'id', 'title', 'city', 'address', 'code', 'work_time', 'longitude', 'latitude'
        ]

class CDEKCitySerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)
    code = serializers.CharField(required=True)
    delivery_price = serializers.DecimalField(max_digits=9, decimal_places=2)
    longitude = serializers.FloatField(required=True)
    latitude = serializers.FloatField(required=True)

    class Meta:
        model = CDEKCities
        fields = [
            'title', 'code', 'delivery_price', 'longitude', 'latitude', 'delivery_period_min', 'delivery_period_max'
        ]

class RussianPostDeliverySerializer(serializers.ModelSerializer):
    region = serializers.CharField(required=True)
    district = serializers.CharField(required=True)
    delivery_price = serializers.DecimalField(max_digits=9, decimal_places=2)

    class Meta:
        model = RussianPostDelivery
        fields = [
            'region', 'district', 'delivery_price'
        ]

