from django.urls import path

from onlineStoreApp.views.categories import get_categories

urlpatterns = [
    # All URLS Patterns in product
    path('', get_categories),

]