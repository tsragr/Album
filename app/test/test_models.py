from django.test import TestCase
from app.models import Image, Mailing
from django.contrib.auth.models import User


class UserImageTest(TestCase):
    """ Test module for User, Image model """

    def setUp(self):
        self.user = User.objects.create(
            username='maxim', password='123qwe', email='test@test.com')
        User.objects.create(
            username='misha', password='123qwe', email='test2@test.com')
        Image.objects.create(title='test', owner=self.user, image='fixture_image/test.jpg', views=0)

    def test_user(self):
        user_maxim = User.objects.get(username='maxim')
        user_misha = User.objects.get(username='misha')
        self.assertEqual(user_maxim.email, 'test@test.com')
        self.assertEqual(user_misha.email, 'test2@test.com')

    def test_image(self):
        image = Image.objects.get(id=1)
        self.assertEqual(image.title, 'test')
        self.assertEqual(image.views, 0)
        self.assertEqual(image.owner.username, 'maxim')

    def tearDown(self) -> None:
        Image.objects.all().delete()
        User.objects.all().delete()
