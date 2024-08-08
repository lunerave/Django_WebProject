import os.path

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.test import APIClient

from user.models import User


# Create your tests here.

class UserTest(TestCase):

    # test data를 미리 생성해서 test할 때 사용한다.
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            email='test_login_email@naver.com',
            nickname='test_login_nickname',
            name='test_name',
            password=make_password('test_password'))

        # Uploadprofile test를 위한 필드 설정
        cls.client = APIClient()
        cls.upload_url = '/user/profile/upload'
        cls.original_media_root = settings.MEDIA_ROOT
        cls.media_root = os.path.join(settings.BASE_DIR, 'user', 'test_media')

    def setUp(self):
        # 테스트 환경에 맞게 MEDIA_ROOT를 설정
        settings.MEDIA_ROOT = self.media_root

        if not os.path.exists(self.media_root):
            os.makedirs(self.media_root)

    def tearDown(self):
        # 테스트 완료 후 MEDIA_ROOT 재설정
        settings.MEDIA_ROOT = self.original_media_root

        if os.path.exists(self.media_root):
            for file_name in os.listdir(self.media_root):
                file_path = os.path.join(self.media_root, file_name)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            os.rmdir(self.media_root)

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

    def test_upload_profile(self):
        temp_image = b'test_image'
        temp_image_name = 'test_image_name.png'
        temp_file = SimpleUploadedFile(temp_image_name, temp_image, content_type='image/png')

        response = self.client.post(self.upload_url, data=dict(
            file=temp_file,
            email=self.user.email))

        self.assertEqual(response.status_code, 200)

        self.user.refresh_from_db()
        uuid_name = self.user.profile_img
        saved_file_path = os.path.join(self.media_root, uuid_name)

        self.assertTrue(os.path.exists(saved_file_path))

        with open(saved_file_path, 'rb') as saved_file:
            saved_image = saved_file.read()

        self.assertEqual(saved_image, temp_image)

