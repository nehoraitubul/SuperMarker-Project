from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, mixins

from onlineStoreApp.models import Product, Cart, CartProduct, Price
from onlineStoreApp.serializers.cart import CartSerializer, CartSerializerWithoutKey
from onlineStoreApp.serializers.product import ProductSerializer
from django.db.models import F, Sum



@api_view(['POST'])
def product_add_to_cart(request, product):
    product_instance = get_object_or_404(Product, catalog_number=product)
    if not product_instance.product_status:
        return Response(data={'error': 'Product is not available'}, status=status.HTTP_400_BAD_REQUEST)
    product_serializer = ProductSerializer(instance=product_instance, many=False)
    return Response(data=product_serializer.data)


class CartViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):

    queryset = Cart.objects.all()
    http_method_names = ['get', 'post', 'put', 'patch']

    def create(self, request, *args, **kwargs):
        product_id = request.data.get('product')
        quantity = request.data.get('quantity')
        product_instance = get_object_or_404(Product, catalog_number=product_id, product_status=True)

        if request.user.is_authenticated:
            cart = Cart(user_id=request.user)
        else:
            cart = Cart()
        cart.save()


        cart_product = CartProduct(product_id=product_instance, quantity=quantity, cart_id=cart)
        cart_product.save()


        serializer = CartSerializer(cart)
        return Response({'cart': serializer.data})

    def partial_update(self, request, *args, **kwargs):
        product_id = request.data.get('product')
        quantity = request.data.get('quantity')
        cart_id = kwargs['pk']   # !!
        key = request.data.get('key')
        product_instance = get_object_or_404(Product, catalog_number=product_id, product_status=True)
        cart = get_object_or_404(Cart, cart_key=key, id=cart_id)

        try:
            cart_product = CartProduct.objects.get(cart_id=cart, product_id=product_instance)
            cart_product.quantity = quantity
            cart_product.save()
        except CartProduct.DoesNotExist:
            cart_product = CartProduct.objects.create(cart_id=cart, product_id=product_instance, quantity=quantity)



        cart_products_qs = cart.products.all()
        cart_product_ids = [cart_prod.id for cart_prod in cart_products_qs]
        all_prices = Price.objects.filter(retailer_id=5, product_id__in=cart_product_ids)
        sum = 0
        for i in all_prices:
            curr_product = cart.cartproduct_set.filter(product_id=i.product_id)
            quantity = curr_product[0].quantity
            print(type(quantity))
            sum += i.price * quantity

        # print('total sum:', sum)


        cart.price = sum
        cart.save()


        serializer = CartSerializerWithoutKey(cart)
        return Response({'cart': serializer.data})
