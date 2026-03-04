from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Article, models
from .serializers import ArticleSerializer, UserSerializer, PublisherSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .api_permissions import IsJournalist, IsEditor, IsOwnerOrEditor
from django.db import models
from .signals import send_article_approved_email

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.filter(approved=True)
    serializer_class = ArticleSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == 'create':
            return [IsJournalist()]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerOrEditor()]
        if self.action == 'approve':
            return [IsEditor()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if self.action == 'subscribed':
            # Only return articles from user's subscriptions
            publisher_ids = user.subscriptions_publishers.values_list('id', flat=True)
            journalist_ids = user.subscriptions_journalists.values_list('id', flat=True)
            return Article.objects.filter(approved=True).filter(
                models.Q(publisher_id__in=publisher_ids) |
                models.Q(author_id__in=journalist_ids)
            )
        return Article.objects.filter(approved=True)

    @action(detail=False, methods=['get'])
    def subscribed(self, request):
        articles = self.get_queryset()
        serializer = self.get_serializer(articles, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        article = self.get_object()
        article.approved = True
        article.save()
        send_article_approved_email(article)
        return Response({'status': 'approved'})

# JWT Auth endpoints
from django.urls import path
api_auth_patterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
