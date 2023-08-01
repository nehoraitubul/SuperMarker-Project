from rest_framework import serializers
from onlineStoreApp.models import Product, Manufacturer, Price

class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ('price', 'unit_of_measure_price', 'unit_of_measure', 'units')

class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = ('name',)

class MainPageSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()
    price_info = serializers.SerializerMethodField()
    more_info = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('name', 'catalog_number', 'manufacturer_id', 'quantity', 'discount_status',
                  'unit_of_measure', 'unit_of_measure_price', 'image', 'sold_qty', 'rating', 'units', 'photo_url', 'price_info', 'more_info')

    def get_photo_url(self, obj):
        return obj.image.url if obj.image else None

    def get_price_info(self, obj):
        try:
            price = Price.objects.get(retailer_id=1, product_id=obj.id)
            return PriceSerializer(price).data
        except Price.DoesNotExist:
            return {}

    def get_more_info(self, obj):
        try:
            manufacturer_info = obj.manufacturer_id
            manu_info = ManufacturerSerializer(manufacturer_info).data

            return {'manu_info': manu_info}
        except Manufacturer.DoesNotExist:
            return {}