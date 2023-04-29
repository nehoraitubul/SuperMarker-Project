from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from onlineStoreApp.views.auth import signup, me

urlpatterns = [
    # All URLS Patterns in auth
    path('signup/', signup),
    path('me/', me),


    # Access check
    path('token/', TokenObtainPairView.as_view()),
    # Refresh Access
    path('token/refresh/', TokenRefreshView.as_view()),
]