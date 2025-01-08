from onlineStoreApp.models import Product, ProductInfo, SubSubSubCategory, SubSubCategory,\
    SubCategory, Category, Manufacturer, Price, PromoProduct, Promo

from rest_framework import serializers

class PromoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promo
        fields = '__all__'

class CategoryExtendedSerializer4(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'id')

class CategoryExtendedSerializer3(serializers.ModelSerializer):
    category_id = CategoryExtendedSerializer4()

    class Meta:
        model = SubCategory
        fields = ('name', 'id', 'category_id')

class CategoryExtendedSerializer2(serializers.ModelSerializer):
    sub_category_id = CategoryExtendedSerializer3()

    class Meta:
        model = SubSubCategory
        fields = ('name', 'id', 'sub_category_id')

class CategoryExtendedSerializer1(serializers.ModelSerializer):

    sub_sub_category_id = CategoryExtendedSerializer2()
    class Meta:
        model = SubSubSubCategory
        fields = ('name', 'id', 'sub_sub_category_id')

class ManufacturerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Manufacturer
        fields = '__all__'

class PriceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Price
        fields = '__all__'

class ProductExtendedSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductInfo
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):

    product_info_id = ProductExtendedSerializer()
    manufacturer_id = ManufacturerSerializer()
    category_id = CategoryExtendedSerializer1()
    price = serializers.SerializerMethodField('get_product_price')
    promo_details = serializers.SerializerMethodField('get_promo_details')

    class Meta:
        model = Product
        fields = ('name', 'catalog_number', 'units', 'image', 'unit_of_measure', 'unit_of_measure_price',
                  'product_info_id', 'manufacturer_id', 'category_id', 'price', 'promo_details')


    def get_product_price(self, obj):
        retailer_id = self.context.get('retailer_id')
        price = Price.objects.filter(product_id=obj.id, retailer_id=retailer_id).first()
        if price:
            return PriceSerializer(price).data
        return None

    def get_promo_details(self, obj):
        retailer_id = self.context.get('retailer_id')
        promo_products = PromoProduct.objects.filter(product_id=obj.id)
        promos = Promo.objects.filter(id__in=promo_products.values_list('promo_id', flat=True))
        promo_serializer = PromoSerializer(promos, many=True)
        return promo_serializer.data