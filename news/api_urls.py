from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import ArticleViewSet, api_auth_patterns

router = DefaultRouter()
router.register(r"articles", ArticleViewSet, basename="article")

urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include("rest_framework.urls")),
    path("token/", include(api_auth_patterns)),
]
