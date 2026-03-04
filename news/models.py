from django.db import models
from django.contrib.auth.models import AbstractUser


# Custom user model
class CustomUser(AbstractUser):
    """
    Custom user model.
    """
    ROLE_CHOICES = (
        ('reader', 'Reader'),
        ('editor', 'Editor'),
        ('journalist', 'Journalist'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    subscriptions_publishers = models.ManyToManyField('Publisher', blank=True, related_name='subscribed_readers')
    subscriptions_journalists = models.ManyToManyField('Journalist', blank=True, related_name='subscribed_readers')
    groups = models.ManyToManyField('auth.Group', related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='customuser_permissions', blank=True)

    def save(self, *args, **kwargs):
            """
            Save custom user object.
            """
            super().save(*args, **kwargs)
            if self.role == 'journalist':
                self.subscriptions_publishers.set([])
                self.subscriptions_journalists.set([])

# Publisher model
class Publisher(models.Model):
    """
    Describes publisher behavior
    """
    name = models.CharField(max_length=255)
    editors = models.ManyToManyField('CustomUser', related_name='publisher_editors', limit_choices_to={'role': 'editor'})
    journalists = models.ManyToManyField('CustomUser', related_name='publisher_journalists', limit_choices_to={'role': 'journalist'})

    def __str__(self):
            """
            Return publisher name.
            """
            return str(self.name)

# Journalist model
class Journalist(models.Model):
    """
    Journalist model.
    """
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE, limit_choices_to={'role': 'journalist'})
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
            """
            Return journalist user.
            """
            return str(self.user)

# Article model
class Article(models.Model):
    """
    Article model.
    """
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    author = models.ForeignKey(Journalist, on_delete=models.CASCADE, null=True, blank=True)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
            """
            Return article title.
            """
            return str(self.title)

# Newsletter model
class Newsletter(models.Model):
    """Newsletter model."""
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Journalist, on_delete=models.CASCADE)
    articles = models.ManyToManyField(Article)

    def __str__(self):
            """
            Return newsletter title.
            """
            return str(self.title)


# ReaderComment model remains for now, but user should reference CustomUser
class ReaderComment(models.Model):
    """Reader comment model."""
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment_text = models.TextField()
    is_premium_subscriber = models.BooleanField(default=False)
    is_verified_subscriber = models.BooleanField(default=False)
