from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views_logout import CustomLogout

urlpatterns = [
    path('', views.home_redirect, name='home'),
    path('accounts/login/', views.login_page, name='login'),
    path('accounts/logout/', CustomLogout.as_view(), name='logout'),
    path('article/<int:pk>/', views.article_detail, name='article_detail'),
    path('write-article/', views.article_create, name='article_create'),
    path('article/<int:pk>/edit/', views.edit_article_content, name='edit_article_content'),
    path('article/<int:pk>/approve/', views.approve_article, name='approve_article'),
    path('comment/<int:article_id>/', views.post_article_comment, name='post_article_comment'),
    path('exclusive/<int:article_id>/', views.read_exclusive_report, name='read_exclusive_report'),
    path('register/', views.register_user, name='register_user'),
    path('password-reset/', views.send_news_password_reset, name='send_news_password_reset'),
    path('publish/', views.publish_article, name='publish_article'),
    path('articles/', views.article_list, name='article_list'),
    path('accounts/profile/', views.profile_redirect, name='profile_redirect'),
    # Newsletter routes
    path('newsletters/', views.newsletter_list, name='newsletter_list'),
    path('newsletter/<int:pk>/', views.newsletter_detail, name='newsletter_detail'),
    path('newsletter/create/', views.newsletter_create, name='newsletter_create'),
    path('newsletter/<int:pk>/edit/', views.newsletter_edit, name='newsletter_edit'),
]