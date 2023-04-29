from django.urls import path
from rest_framework.routers import DefaultRouter

from onlineStoreApp.views.search import SearchViewSet

router = DefaultRouter()
router.register('', SearchViewSet)
router.register('category', SearchViewSet)

urlpatterns = []

# adding movies urls to urlpatterns
urlpatterns.extend(router.urls)