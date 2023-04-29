from rest_framework import serializers

from onlineStoreApp.models import Cart, CartProduct


class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        fields = ['id', 'product_id', 'quantity']

class CartSerializer(serializers.ModelSerializer):
    cart_product = CartProductSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user_id', 'date', 'price', 'cart_status', 'cart_key', 'cart_product']


class CartSerializerWithoutKey(serializers.ModelSerializer):
    cart_product = CartProductSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user_id', 'date', 'price', 'cart_status', 'cart_product']