from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from onlineStoreApp.models import SubCategory, SubSubCategory, SubSubSubCategory
from onlineStoreApp.serializers.categories import CategorySerializer, AllCategorySerializer, \
    AllSubSubCategorySerializer, AllSubSubSubCategorySerializer


@api_view(['GET'])
def get_categories(request):
    categories = SubCategory.objects.all()
    response_data = []
    for category in categories:
        sub_sub_categories = category.subsubcategory_set.all()
        sub_sub_category_serializer = AllSubSubCategorySerializer(sub_sub_categories, many=True)

        data = []
        for sub_sub_category in sub_sub_categories:
            sub_sub_sub_categories = sub_sub_category.subsubsubcategory_set.all()
            sub_sub_sub_category_serializer = AllSubSubSubCategorySerializer(sub_sub_sub_categories, many=True)
            sub_sub_category_data = {
                'id': sub_sub_category.id,
                'name': sub_sub_category.name,
                'sub_sub_sub_categories': sub_sub_sub_category_serializer.data
            }
            data.append(sub_sub_category_data)
            data = sorted(data, key=lambda x: len(x['sub_sub_sub_categories']), reverse=True)
            

        category_data = {
            'category': AllCategorySerializer(category).data,
            'sub_categories': sub_sub_category_serializer.data,
            'sub_sub_categories': data
        }
        response_data.append(category_data)

    return Response(response_data)


    # category = request.query_params.get('category')
    # if category:
    #     sub_category = SubCategory.objects.get(name=category)
    #     sub_sub_categories = sub_category.subsubcategory_set.all()
    #     sub_sub_category_serializer = AllSubSubCategorySerializer(sub_sub_categories, many=True)
    #
    #     data = []
    #     for sub_sub_category in sub_sub_categories:
    #         sub_sub_sub_categories = sub_sub_category.subsubsubcategory_set.all()
    #         sub_sub_sub_category_serializer = AllSubSubSubCategorySerializer(sub_sub_sub_categories, many=True)
    #         sub_sub_category_data = {
    #             'id': sub_sub_category.id,
    #             'name': sub_sub_category.name,
    #             'sub_sub_sub_categories': sub_sub_sub_category_serializer.data
    #         }
    #         data.append(sub_sub_category_data)
    #
    #     response_data = {
    #         'category': AllCategorySerializer(sub_category).data,
    #         'sub_categories': sub_sub_category_serializer.data,
    #         'sub_sub_categories': data
    #     }
    #
    #     return Response(response_data)
    #
    #
    # else:
    #     categories = SubCategory.objects.all()
    #     category_serializer = CategorySerializer(categories, many=True)
    #
    #
    # return Response(data=category_serializer.data)