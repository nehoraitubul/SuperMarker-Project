from rest_framework import serializers

from onlineStoreApp.models import SubCategory


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = SubCategory
        fields = ("name", "id")