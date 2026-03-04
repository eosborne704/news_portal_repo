from django.core.mail import send_mail

def send_article_approved_email(article):
    # Example email logic
    send_mail(
        subject=f"Article Approved: {article.title}",
        message=f"Your article '{article.title}' has been approved.",
        from_email="no-reply@nownews.com",
        recipient_list=[article.author.user.email],
        fail_silently=True,
    )
