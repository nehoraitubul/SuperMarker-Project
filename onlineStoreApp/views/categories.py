from rest_framework.decorators import api_view
from rest_framework.response import Response

from onlineStoreApp.models import SubCategory
from onlineStoreApp.serializers.categories import CategorySerializer



@api_view(['GET'])
def get_categories(request):
    categories = SubCategory.objects.all()
    category_serializer = CategorySerializer(categories, many=True)
    return Response(data=category_serializer.data)