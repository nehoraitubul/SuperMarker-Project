from rest_framework import serializers
from onlineStoreApp.models import Promo, Product, PromoProduct

class PromoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promo
        fields = '__all__'


class PromoProductsSerializer(serializers.Serializer):
    product_catalog_number = serializers.CharField()

    def to_representation(self, instance):
        product_catalog_number = self.validated_data.get('product_catalog_number')

        # Retrieve the product instance based on the provided catalog number
        try:
            product = Product.objects.get(catalog_number=product_catalog_number)
        except Product.DoesNotExist:
            return {'error': 'Product not found'}

        # Retrieve all promos associated with the given product
        promos = Promo.objects.filter(promoprod__product_id=product)

        # Serialize the promos along with their associated promo products
        promo_serializer = PromoSerializer(promos, many=True)
        return promo_serializer.data