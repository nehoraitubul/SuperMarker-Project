from rest_framework import serializers

from onlineStoreApp.models import SubCategory


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = SubCategory
        fields = ("name", "id")


class AllCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = SubCategory
        fields = ("name", "id")


class AllSubSubCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = SubCategory
        fields = ("name", "id")


class AllSubSubSubCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = SubCategory
        fields = ("name", "id")