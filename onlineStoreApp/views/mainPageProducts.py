from rest_framework import viewsets, mixins
from rest_framework.response import Response
from onlineStoreApp.models import Product, Category
from onlineStoreApp.serializers.search import SearchSerializer
from django.db.models import Count
import random


class MainProductsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = SearchSerializer

    def get_random_products(self):
        products = Product.objects.filter(image__isnull=False, name__isnull=False)
        if products.count() >= 20:
            return random.sample(list(products), 20)
        else:
            return products

    def list(self, request, *args, **kwargs):
        random_products = self.get_random_products()
        serializer = self.get_serializer(random_products, many=True)
        return Response(serializer.data)