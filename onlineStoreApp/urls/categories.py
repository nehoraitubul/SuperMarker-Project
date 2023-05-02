from django.urls import path, include

from onlineStoreApp.views.categories import get_categories

urlpatterns = [
    # All URLS Patterns in product
    path('', get_categories),

]