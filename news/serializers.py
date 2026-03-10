from rest_framework import serializers
from .models import Article, CustomUser, Publisher, Newsletter


class ArticleSerializer(serializers.ModelSerializer):
    """
    Serializer for Article
    """

    class Meta:
        """
        Meta for Article
        """

        model = Article
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.
    """

    class Meta:
        """
        Meta for UserSerializer.
        """

        model = CustomUser
        fields = ["id", "email", "username", "role"]


class PublisherSerializer(serializers.ModelSerializer):
    """
    Serializer for Publisher
    """

    class Meta:
        """
        Meta for PublisherSerializer.
        """

        model = Publisher
        fields = "__all__"


class NewsletterSerializer(serializers.ModelSerializer):
    """
    Serializer for Newsletter
    """

    class Meta:
        """
        Meta for Newsletter
        """

        model = Newsletter
        fields = "__all__"
