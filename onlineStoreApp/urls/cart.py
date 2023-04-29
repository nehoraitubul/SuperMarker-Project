from django.urls import path, include
from rest_framework.routers import DefaultRouter

from onlineStoreApp.views.cart import CartViewSet

router = DefaultRouter()
router.register('', CartViewSet)

urlpatterns = []

# adding movies urls to urlpatterns
urlpatterns.extend(router.urls)