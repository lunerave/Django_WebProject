from django.test import TestCase

from user.models import User


# Create your tests here.


class UserTest(TestCase):
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
