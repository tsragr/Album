from django.shortcuts import render
from rest_framework import generics, permissions, viewsets, mixins
from rest_framework.response import Response
from knox.models import AuthToken
from app.serializers import RegisterSerializer, UserSerializer, ImageSerializer, UpdateImageSerializer, \
    ListImagesSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import login
from app.models import Image
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from app.services import convert_to_webp, convert_to_webm
from pathlib import Path
from app.permissions import IsOwner


class RegisterAPI(generics.GenericAPIView):
    """
    View to register user
    """
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class LoginAPI(KnoxLoginView):
    """
    Login View
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super().post(request, format=None)


class ImageViewSet(viewsets.GenericViewSet,
                   mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin):
    """
    Create, Retrieve and Update image
    """
    queryset = Image.objects.all()
    serializer_classes = {'update': UpdateImageSerializer,
                          'particular_update': UpdateImageSerializer,
                          'create': ImageSerializer,
                          'list': ListImagesSerializer}

    def get_permissions(self):
        if self.action == 'update' or self.action == 'particular_update':
            permission_classes = [permissions.IsAuthenticated, IsOwner]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        return self.serializer_classes[self.action]

    @action(methods=['GET'], detail=True)
    def get_image_detail_and_webp(self, request, pk=None):
        """
        endpoint to return one image and image.webp
        :param request:
        :param pk:
        :return: image and image.webp
        """
        image = get_object_or_404(Image, pk=pk)
        webp_img = Path(f"/media{str(convert_to_webp(image.image.path)).split('/media')[1]}")
        img = Path(f"/media{str(image.image.path).split('/media')[1]}")
        image.views += 1
        image.save()
        return Response({"img_webp": f"{webp_img}",
                         "img": f'{img}'})

    @action(methods=['GET'], detail=False)
    def get_top_webm(self, request):
        """
        endpoint to return top images by views in .webm format
        :param request:
        :return: top.webm
        """
        top_images = [f"media/{image['image']}" for image in
                      Image.objects.order_by('-views').values('image')[:10]]
        return Response({"top_webm": f"/{convert_to_webm(top_images)}"})

    @action(methods=['GET'], detail=False)
    def get_my_top_webm(self, request):
        """
        endpoint to return user's top images by views in .webm format
        :param request:
        :return: op.webm
        """
        top_images = [f"media/{image['image']}" for image in
                      Image.objects.filter(owner=self.request.user).order_by('-views').values('image')[:10]]
        return Response({"top_webm": f"/{convert_to_webm(top_images)}"})
