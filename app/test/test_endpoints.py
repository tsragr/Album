from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from knox.models import AuthToken
from app.models import Image
import io
from PIL import Image as img

client = APIClient()


class EndPointTest(TestCase):

    def generate_photo_file(self):
        file = io.BytesIO()
        image = img.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file

    def setUp(self) -> None:
        self.user = User.objects.create(
            username='maxim', password='123qwe', email='test@test.com')
        self.token = AuthToken.objects.create(self.user)[1]

    def test_register_login(self):
        """
        Test registration and login endpoint
        """
        response_register = client.post('/api/v1/register/',
                                        {'username': 'test', 'email': 'test@test.com', 'password': '123qwe',
                                         'password_confirm': '123qwe'})
        response_login = client.post('/api/v1/login/', {'username': 'test', 'password': '123qwe'})
        self.assertEqual(response_register.status_code, 200)
        self.assertEqual(response_login.status_code, 200)

    def test_views_image(self):
        """
        Test image's endpoints
        """
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response_post = client.post('/api/v1/image/', {'title': 'image', 'image': self.generate_photo_file()})
        response_get = client.get('/api/v1/image/')
        response_put = client.put('/api/v1/image/1/', {'title': 'new title'})
        response_get_detail_webp = client.get('/api/v1/image/1/get_image_detail_and_webp/')
        response_get_top_webm = client.get('/api/v1/image/get_top_webm/')
        response_get_my_top_webm = client.get('/api/v1/image/get_my_top_webm/')
        self.assertEqual(response_post.status_code, 201)
        self.assertEqual(response_get.status_code, 200)
        self.assertEqual(response_put.status_code, 200)
        self.assertEqual(response_get_detail_webp.status_code, 200)
        self.assertEqual(response_get_top_webm.status_code, 200)
        self.assertEqual(response_get_my_top_webm.status_code, 200)

    def tearDown(self) -> None:
        Image.objects.all().delete()
        User.objects.all().delete()
