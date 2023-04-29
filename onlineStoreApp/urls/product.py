from django.urls import path, include

from onlineStoreApp.views.product import product

urlpatterns = [
    # All URLS Patterns in product
    path('<int:product>/', product),

]