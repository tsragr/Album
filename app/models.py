from django.db import models
from django.contrib.auth.models import User
from app.services import get_path_upload_file, validate_image
from django.core.validators import FileExtensionValidator


class Image(models.Model):
    """
    Image's model
    """
    title = models.CharField(max_length=120)
    owner = models.ForeignKey(User, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_path_upload_file, validators=[validate_image, FileExtensionValidator(
        allowed_extensions=['png', 'jpg', 'jpeg'],
        message=' PNG and JPG only file extension'
    )])
    views = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} - {self.owner.username}'


class Mailing(models.Model):
    """
    Model mailing letters
    """
    title = models.CharField(max_length=120)
    text = models.TextField()

    def __str__(self):
        return f'{self.title} - {self.text[:200]}'
