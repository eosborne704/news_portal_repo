from django import forms
from .models import (
    CustomUser,
    Article,
    Newsletter,
    ReaderComment,
    Publisher,
    Journalist,
)


class RegisterUserForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    subscriptions_publishers = forms.ModelMultipleChoiceField(
        queryset=Publisher.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Subscribe to Publishers",
    )
    subscriptions_journalists = forms.ModelMultipleChoiceField(
        queryset=Journalist.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Subscribe to Journalists",
    )

    class Meta:
        model = CustomUser
        fields = [
            "email",
            "username",
            "password",
            "role",
            "subscriptions_publishers",
            "subscriptions_journalists",
        ]


class ArticleForm(forms.ModelForm):
    """
    Form for making articles
    """

    class Meta:
        model = Article
        fields = ["title", "content", "author"]


class NewsletterForm(forms.ModelForm):
    """
    Form for making newsletters
    """

    articles = forms.ModelMultipleChoiceField(
        queryset=Article.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Articles",
    )

    class Meta:
        model = Newsletter
        fields = ["title", "description", "author", "articles"]


class CommentForm(forms.ModelForm):
    """
    Form for making comments
    """

    class Meta:
        model = ReaderComment
        fields = ["comment_text", "is_premium_subscriber", "is_verified_subscriber"]
