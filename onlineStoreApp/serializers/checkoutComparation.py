from rest_framework import serializers
from onlineStoreApp.models import Product, Price, Retailer

class RetailerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Retailer
        fields = ('name', 'last_scan')

class PriceSerializer(serializers.ModelSerializer):
    retailer = RetailerSerializer()  # Serialize retailer data within PriceSerializer

    class Meta:
        model = Price
        fields = ('retailer', 'price', 'unit_of_measure_price', 'unit_of_measure', 'units')

class ProductSerializer(serializers.ModelSerializer):
    prices = PriceSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('name', 'catalog_number', 'prices')