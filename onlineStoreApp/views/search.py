from rest_framework import viewsets, mixins

from onlineStoreApp.models import Product, SubSubSubCategory, SubSubCategory, SubCategory
from onlineStoreApp.serializers.search import SearchSerializer
from django.db.models import Q


# class SearchViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
#     queryset = Product.objects.all()
#     serializer_class = SearchSerializer
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         search_query = self.request.query_params.get('query', None)
#         category_query = self.kwargs.get('category_query', None)
#
#         if search_query:
#             queryset = queryset.filter(name__icontains=search_query)
#         if category_query:
#             subquery = SubSubSubCategory.objects.filter(name=category_query).values('id').first()
#             queryset = queryset.filter(category_id=subquery['id'])
#
#         return queryset

from django.contrib.postgres.search import SearchVector

class SearchViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = SearchSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.query_params.get('s_query', None)
        category4_query = self.request.query_params.get('sc4_id', None)
        category3_query = self.request.query_params.get('sc3_id', None)
        category2_query = self.request.query_params.get('sc2_id', None)
        category1_query = self.request.query_params.get('sc1_id', None)

        if search_query:
            vector = SearchVector('name')
            queryset = queryset.annotate(search=vector).filter(search=search_query)
        # Start building the query to filter by category parameters
        category_filter = Q()

        # Check for sc4 query parameter
        if category4_query:
            category_filter |= Q(category_id__in=SubSubSubCategory.objects.filter(id=category4_query))

        # Check for sc3 query parameter
        if category3_query:
            category_filter |= Q(category_id__in=SubSubSubCategory.objects.filter(
                sub_sub_category_id__in=SubSubCategory.objects.filter(id=category3_query).values_list('id', flat=True)).values_list('id', flat=True))

        # Check for sc2 query parameter
        if category2_query:
            category_filter |= Q(category_id__in=SubSubSubCategory.objects.filter(
                sub_sub_category_id__in=SubSubCategory.objects.filter(
                    sub_category_id__in=SubCategory.objects.filter(id=category2_query).values_list('id', flat=True)).values_list(
                    'id', flat=True)).values_list('id', flat=True))


        # Check for sc1 query parameter
        if category1_query:
            return queryset.filter(product_status=True)

        # Apply the category filter to the queryset
        if category_filter:
            queryset = queryset.filter(category_filter).filter(product_status=True)

        # queryset = queryset.order_by('catalog_number', 'name').distinct('catalog_number')

        return queryset