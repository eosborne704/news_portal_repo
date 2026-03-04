from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .models import Article, CustomUser, Journalist, Publisher, Newsletter
from .forms import ArticleForm, CommentForm, NewsletterForm, RegisterUserForm
import secrets
from django.utils import timezone
from django.core.mail import EmailMessage
from django.http import HttpResponseNotFound, HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login

# Display all published articles
def article_list(request):
    user = request.user
    if user.is_authenticated and hasattr(user, 'role'):
        if user.role == 'reader':
            articles = Article.objects.filter(approved=True)
        elif user.role in ['editor', 'journalist']:
            articles = Article.objects.all()
        else:
            articles = Article.objects.none()
    else:
        articles = Article.objects.filter(approved=True)
    return render(request, "news/article_list.html", {"articles": articles})


# Show one specific news story
def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, "news/article_detail.html", {"article": article})


# Logic to publish a new article
@login_required
def article_create(request):
    user = request.user
    if not hasattr(user, 'role') or user.role != 'journalist':
        return HttpResponse("Access Denied: Only Journalists can create articles.")
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            journalist = Journalist.objects.get(user=user)
            article = form.save(commit=False)
            article.author = journalist
            article.save()
            return redirect("article_list")
    else:
        form = ArticleForm()
    return render(request, "news/article_form.html", {"form": form})


@login_required(login_url='/login/')
def read_exclusive_report(request, article_id):
    return render(request, 'news/exclusive.html')


@login_required
def publish_article(request):
    """
    Handles publishing a news article. Only users with 'news.add_article' permission can publish.
    Combines previous publish_article and publish_news_story logic for clarity.
    """
    if request.user.has_perm('news.add_article'):
        return render(request, 'news/publish_success.html')
    else:
        return HttpResponse("Access Denied: Only Journalists can publish news.")


def register_user(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            # Save subscriptions
            form.save_m2m()
            # Automatically create Journalist object if role is journalist
            if user.role == 'journalist':
                from .models import Journalist
                Journalist.objects.create(user=user)
            return redirect('login')
    else:
        form = RegisterUserForm()
    return render(request, 'news/register_user.html', {'form': form})


@login_required
def post_article_comment(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            return redirect("article_detail", pk=article.pk)
    else:
        form = CommentForm()
    return render(request, "news/comment_form.html", {"form": form, "article": article})


def send_news_password_reset(request):
    if request.method == 'POST':
        user_email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=user_email)
            token_value = secrets.token_urlsafe(32)
            reset_url = f"http://127.0.0.1:8000/reset-password/{token_value}/"
            email = EmailMessage(
                "News Portal Password Reset",
                [user_email]
            )
            email.send()
            return HttpResponse("Reset link sent!")
        except CustomUser.DoesNotExist:
            return HttpResponse("Email not found.")
    return render(request, 'news/password_reset_form.html')


@login_required
def edit_article_content(request, pk):
    article = get_object_or_404(Article, pk=pk)
    user = request.user
    can_edit = False
    if hasattr(user, 'role'):
        if user.role == 'editor':
            can_edit = True
        elif user.role == 'journalist' and article.author and article.author.user == user:
            can_edit = True
    if not can_edit:
        return HttpResponse("Access Denied: You do not have permission to edit this article.")
    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            return redirect("article_detail", pk=article.pk)
    else:
        form = ArticleForm(instance=article)
    return render(request, "news/edit_form.html", {"form": form})


@login_required
def newsletter_list(request):
    newsletters = Newsletter.objects.all()
    return render(request, "news/newsletter_list.html", {"newsletters": newsletters})


@login_required
def newsletter_detail(request, pk):
    newsletter = get_object_or_404(Newsletter, pk=pk)
    return render(request, "news/newsletter_detail.html", {"newsletter": newsletter})


@login_required
def newsletter_create(request):
    user = request.user
    if not hasattr(user, 'role') or user.role not in ['journalist', 'editor']:
        return HttpResponse("Access Denied: Only Journalists and Editors can create newsletters.")
    if request.method == "POST":
        # Assume a NewsletterForm exists
        form = NewsletterForm(request.POST)
        if form.is_valid():
            newsletter = form.save(commit=False)
            journalist = Journalist.objects.get(user=user)
            newsletter.author = journalist
            newsletter.save()
            form.save_m2m()
            return redirect("newsletter_list")
    else:
        form = NewsletterForm()
    return render(request, "news/newsletter_form.html", {"form": form})

@login_required
def newsletter_edit(request, pk):
    newsletter = get_object_or_404(Newsletter, pk=pk)
    user = request.user
    can_edit = False
    if hasattr(user, 'role'):
        if user.role == 'editor':
            can_edit = True
        elif user.role == 'journalist' and newsletter.author and newsletter.author.user == user:
            can_edit = True
    if not can_edit:
        return HttpResponse("Access Denied: You do not have permission to edit this newsletter.")
    if request.method == "POST":
        form = NewsletterForm(request.POST, instance=newsletter)
        if form.is_valid():
            form.save()
            return redirect("newsletter_detail", pk=newsletter.pk)
    else:
        form = NewsletterForm(instance=newsletter)
    return render(request, "news/newsletter_form.html", {"form": form})


@login_required(login_url='/accounts/login/')
def welcome_view(request):
    """
    Renders the welcome page
    """
    return render(request, 'welcome.html')


def welcome(request):
    """
    Render the welcome page template.
    """
    return render(request, 'welcome.html')

@login_required
def approve_article(request, pk):
    user = request.user
    if not hasattr(user, 'role') or user.role != 'editor':
        return HttpResponse("Access Denied: Only Editors can approve articles.<br><a href='/'>Back to Main Menu</a>")
    article = get_object_or_404(Article, pk=pk)
    if request.method == "POST":
        article.approved = True
        article.save()
        # Optionally, send email to subscribers and POST to API endpoint here
        return redirect("article_detail", pk=article.pk)
    return render(request, "news/approve_article.html", {"article": article})

def home_redirect(request):
    return redirect('login')

def profile_redirect(request):
    return HttpResponseNotFound("Profile page does not exist. Please use the navigation to view articles.")

def login_page(request):
    articles = Article.objects.filter(approved=True)
    if request.user.is_authenticated:
        return render(request, 'registration/login.html', {'articles': articles})
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return render(request, 'registration/login.html', {'articles': articles})
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form, 'articles': articles})

def create_missing_journalists():
    from .models import CustomUser, Journalist
    missing = CustomUser.objects.filter(role='journalist').exclude(id__in=Journalist.objects.values_list('user_id', flat=True))
    for user in missing:
        Journalist.objects.create(user=user)
    return f"Created {missing.count()} missing Journalist objects."