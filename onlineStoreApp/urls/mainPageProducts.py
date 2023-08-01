from django.urls import path
from rest_framework.routers import DefaultRouter

from onlineStoreApp.views.mainPageProducts import MainProductsViewSet

router = DefaultRouter()
router.register(r'', MainProductsViewSet, basename='')

urlpatterns = []

# adding movies urls to urlpatterns
urlpatterns.extend(router.urls)