from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # All URLS Patterns in auth
    # path('signup/', signup),

    # Access check
    path('token/', TokenObtainPairView.as_view()),
    # Refresh Access
    path('token/refresh/', TokenRefreshView.as_view()),
]