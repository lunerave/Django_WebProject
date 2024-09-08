from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.hashers import make_password

from content.models import Feed, Reply, Like, Bookmark


# Create your tests here.
class ContentTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # 사용자 모델을 가져오기
        cls.User = get_user_model()

        # 테스트에 사용할 사용자 생성
        cls.user = cls.User.objects.create(
            email='test@example.com',
            nickname='test_user',
            name='test_name',
            password=make_password('test_password')
        )

        # 피드, 댓글, 좋아요, 북마크 등 데이터 생성
        cls.feed = Feed.objects.create(email=cls.user.email, content="Test feed content", image="test_image.jpg")
        cls.reply = Reply.objects.create(feed_id=cls.feed.id, email=cls.user.email, reply_content="Test reply")
        cls.like = Like.objects.create(feed_id=cls.feed.id, email=cls.user.email, is_like=True)
        cls.bookmark = Bookmark.objects.create(feed_id=cls.feed.id, email=cls.user.email, is_marked=True)

    def testMain(self):
        session = self.client.session
        session['email'] = self.user.email
        session.save()

        self.assertEqual(session['email'], self.user.email)

        # Main 뷰에 대한 GET 요청
        response = self.client.get(reverse('main'))

        # 응답 상태 코드가 200인지 확인
        self.assertEqual(response.status_code, 200)

        # 템플릿이 올바르게 렌더링되었는지 확인
        self.assertTemplateUsed(response, 'myInstagram/main.html')

        # 피드 데이터가 템플릿 컨텍스트에 포함되어 있는지 확인
        feeds = response.context['feeds']
        self.assertEqual(len(feeds), 1)
        self.assertEqual(feeds[0]['content'], "Test feed content")

        # 사용자 데이터가 포함되어 있는지 확인
        user = response.context['user']
        self.assertEqual(user.email, self.user.email)

    def testUploadFeed(self):
        # 세션에 이메일 저장
        session = self.client.session
        session['email'] = self.user.email
        session.save()

        # 가짜 이미지 파일 생성
        test_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'\x00\x01\x02',  # 가짜 이미지 파일 생성
            content_type='image/jpeg'
        )

        # POST 요청을 통해 피드 업로드
        data = {
            'file': test_image,
            'content': 'Test feed content',
        }
        response = self.client.post(reverse('upload_feed'), data, format='multipart')

        # 응답 상태 코드 확인
        self.assertEqual(response.status_code, 200)

        # Feed 객체가 생성되었는지 확인
        # 사용자 데이터 생성에서 1개, 해당 API를 통해 1개 -> 총 2개 피드
        self.assertEqual(Feed.objects.count(), 2)
        feed = Feed.objects.first()

        # 피드가 올바른 데이터로 생성되었는지 확인
        self.assertEqual(feed.email, self.user.email)
        self.assertEqual(feed.content, 'Test feed content')
        self.assertTrue(feed.image)  # 이미지가 저장되었는지 확인