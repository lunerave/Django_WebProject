from django.contrib.auth.hashers import make_password
from django.test import TestCase
from django.urls import reverse

from user.models import User


# Create your tests here.


class UserTest(TestCase):

    # test data를 미리 생성해서 test할 때 사용한다.
    @classmethod
    def setUpTestData(cls):
        User.objects.create(
            email='test_login_email@naver.com',
            nickname='test_login_nickname',
            name='test_name',
            password=make_password('test_password'))

    def test(self):
        self.assertEqual(1, 1)

    def test_join(self):
        response = self.client.post('/user/join', data=dict(
            email='test_email@naver.com',
            nickname='test_nickname',
            name='test_name',
            password='test_password'))
        self.assertEqual(response.status_code, 200)

        user = User.objects.filter(email='test_email@naver.com').first()

        self.assertEqual(user.nickname, 'test_nickname')
        self.assertEqual(user.name, 'test_name')
        self.assertTrue(user.check_password('test_password'))

    def test_login(self):
        response = self.client.post('/user/login', data=dict(
            email='test_login_email@naver.com',
            password='test_password'))
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        response = self.client.get('/user/logout')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/login.html')

        self.assertFalse('_auth_user_id' in self.client.session)
