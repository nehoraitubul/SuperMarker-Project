from rest_framework import serializers

from onlineStoreApp.models import Product


class SearchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'
