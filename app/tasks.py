from config.celery import app
from app.models import Image, Mailing
from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER


@app.task
def send_mailing():
    """
    task for mailing letters
    """
    title = Mailing.objects.first().title
    text = Mailing.objects.first().text
    top = list(set([el.owner.email for el in Image.objects.order_by('-views').select_related('owner')[:3]]))
    send_mail(f'{title}', f'{text}', EMAIL_HOST_USER, top, fail_silently=False)
