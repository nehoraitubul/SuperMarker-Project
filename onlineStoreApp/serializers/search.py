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

class SearchSerializer(serializers.ModelSerializer):
    more_info = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('name', 'catalog_number', 'manufacturer_id', 'quantity', 'discount_status', 'unit_of_measure', 'unit_of_measure_price', 'image', 'sold_qty', 'rating', 'units', 'more_info')

    def get_more_info(self, obj):
        try:
            price = Price.objects.filter(retailer_id=1, product_id=obj.id).first()
            price_info = price.price
            unit_of_measure_price = price.unit_of_measure_price
            unit_of_measure = price.unit_of_measure
            units = price.units

            manufacturer_info = obj.manufacturer_id
            manu_info =  ManufacturerSerializer(manufacturer_info).data

            return {'price_info': price_info, 'unit_of_measure_price': unit_of_measure_price, 'unit_of_measure': unit_of_measure, 'units': units, 'manu_info': manu_info}
        except Manufacturer.DoesNotExist:
            return {}