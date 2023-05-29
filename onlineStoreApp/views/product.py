from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, mixins
from rest_framework.viewsets import GenericViewSet

from onlineStoreApp.models import Product
from onlineStoreApp.serializers.product import ProductSerializer



@api_view(['GET'])
def product(request, product):
    retailer_id = 1
    product_instance = get_object_or_404(Product, catalog_number=product)
    if not product_instance.product_status:
        return Response(data={'error': 'Product is not available'}, status=status.HTTP_400_BAD_REQUEST)
    product_serializer = ProductSerializer(instance=product_instance, many=False, context={'retailer_id': retailer_id})
    return Response(data=product_serializer.data)