from django.urls import path, include

from onlineStoreApp.views.checkoutComparation import get_retailers_with_products_and_prices

urlpatterns = [
    # All URLS Patterns in product
    path('', get_retailers_with_products_and_prices),

]