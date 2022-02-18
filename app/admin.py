from django.contrib import admin
from app import models


@admin.register(models.Image)
class PhotoAdmin(admin.ModelAdmin):
    """
    Image admin model
    """
    list_display = ('owner', 'title', 'image', 'created', 'updated')


@admin.register(models.Mailing)
class PhotoAdmin(admin.ModelAdmin):
    """
    Mailing admin model
    """
    list_display = ('title', 'text')
