from rest_framework import serializers
from django.contrib.auth.models import User
from app import models


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for authenticated users
    """

    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class RegisterSerializer(serializers.ModelSerializer):
    """
    Registration serializer
    """

    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm')

    def create(self, validated_data):
        if validated_data['password'] == validated_data['password_confirm']:
            user = User.objects.create_user(
                username=validated_data['username'],
                password=validated_data['password'],
                email=validated_data['email']
            )
        return user


class ImageSerializer(serializers.ModelSerializer):
    """
    Serializer for image create
    """
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Image
        exclude = ('views',)


class UpdateImageSerializer(serializers.ModelSerializer):
    """
    Serializer for edit image title
    """

    class Meta:
        model = models.Image
        fields = ('title',)


class ListImagesSerializer(serializers.ModelSerializer):
    """
        Serializer for image list
    """
    user = serializers.SlugRelatedField(source='owner', slug_field='username', read_only=True)

    class Meta:
        model = models.Image
        fields = ('title', 'user', 'image', 'views', 'created', 'updated')
