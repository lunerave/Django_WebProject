import os
import tempfile

from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
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

        # Profile API를 위한 다른 임시 유저의 임시 피드 생성
        # 좋아요, 북마크한 피드들에 대해서만 API가 작동하는 지 확인 하기 위한 데이터
        cls.other_user = cls.User.objects.create(
            email='other_user@example.com',
            nickname='other_user',
            name='other_user_name',
            password=make_password('other_password')
        )

        # 피드, 댓글, 좋아요, 북마크 등 데이터 생성
        cls.feed = Feed.objects.create(email=cls.user.email, content="Test feed content", image="test_image.jpg")
        cls.other_feed = Feed.objects.create(email=cls.other_user.email, content="Other user feed content",
                                             image="other_feed_image.jpg")
        cls.reply = Reply.objects.create(feed_id=cls.feed.id, email=cls.user.email, reply_content="Test reply")
        cls.like = Like.objects.create(feed_id=cls.feed.id, email=cls.user.email, is_like=True)
        cls.like2 = Like.objects.create(feed_id=cls.other_feed.id, email=cls.user.email, is_like=True)
        cls.bookmark = Bookmark.objects.create(feed_id=cls.feed.id, email=cls.user.email, is_marked=True)

    def setUp(self):
        # 임시 디렉토리 생성 및 MEDIA_ROOT 설정
        self.media_root = tempfile.mkdtemp()
        self.original_media_root = settings.MEDIA_ROOT
        settings.MEDIA_ROOT = self.media_root

    def tearDown(self):
        # MEDIA_ROOT 재설정 및 임시 디렉토리 정리
        settings.MEDIA_ROOT = self.original_media_root
        if os.path.exists(self.media_root):
            for file_name in os.listdir(self.media_root):
                file_path = os.path.join(self.media_root, file_name)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            os.rmdir(self.media_root)

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
        # 마지막 피드가 가장 첫 번째 위치에 저장 된다.
        feeds = response.context['feeds']
        self.assertEqual(len(feeds), 2)
        self.assertEqual(feeds[0]['content'], "Other user feed content")

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
            'content': 'Test feed content2',
        }
        response = self.client.post(reverse('upload_feed'), data, format='multipart')

        # 응답 상태 코드 확인
        self.assertEqual(response.status_code, 200)

        # Feed 객체가 생성되었는지 확인
        # 사용자 데이터 생성에서 2개, 해당 API를 통해 1개 -> 총 3개 피드
        self.assertEqual(Feed.objects.count(), 3)

        # Main API가 실행되기 전까지는 피드가 id 역순으로 정렬되지 않는다.
        feed = Feed.objects.last()

        # 피드가 올바른 데이터로 생성되었는지 확인
        self.assertEqual(feed.email, self.user.email)
        self.assertEqual(feed.content, 'Test feed content2')
        self.assertTrue(feed.image)  # 이미지가 저장되었는지 확인

    def testProfile(self):
        # 세션에 이메일 저장
        session = self.client.session
        session['email'] = self.user.email
        session.save()

        # GET 요청을 통해 프로필 페이지 접근
        response = self.client.get(reverse('profile'))

        # 응답 상태 코드 확인
        self.assertEqual(response.status_code, 200)

        # 컨텍스트에 사용자 정보가 제대로 포함되었는지 확인
        self.assertIn('user', response.context)
        self.assertEqual(response.context['user'].email, self.user.email)

        # 사용자의 피드 리스트가 1개인지 확인
        self.assertIn('feed_list', response.context)
        self.assertEqual(len(response.context['feed_list']), 1)
        self.assertEqual(response.context['feed_list'][0].content, 'Test feed content')

        # 사용자가 좋아요한 피드 리스트 확인
        # 사용자가 좋아요한 피드는 총 2개이다.
        self.assertIn('like_feed_list', response.context)
        self.assertEqual(len(response.context['like_feed_list']), 2)
        self.assertEqual(response.context['like_feed_list'][0].content, 'Test feed content')
        self.assertEqual(response.context['like_feed_list'][1].content, 'Other user feed content')

        # 사용자가 북마크한 피드 리스트 확인
        self.assertIn('bookmark_feed_list', response.context)
        self.assertEqual(len(response.context['bookmark_feed_list']), 1)
        self.assertEqual(response.context['bookmark_feed_list'][0].content, 'Test feed content')

        # 다른 사용자의 피드가 잘 포함되지 않았는지 확인
        self.assertNotIn(self.other_feed, response.context['feed_list'])

        # 북마크하지 않은 피드가 잘 포함되지 않았는지 확인
        bookmark_feed_list = response.context['bookmark_feed_list']
        self.assertNotIn(self.other_feed, bookmark_feed_list)

    def testUploadReply(self):
        # 세션에 이메일 저장
        session = self.client.session
        session['email'] = self.user.email
        session.save()

        data = {
            'feed_id': self.feed.id,
            'reply_content': 'Test reply',
        }

        # 댓글 데이터 POST 전송
        response = self.client.post(reverse('upload_reply'), data, format='multipart')

        # 응답 상태 코드 확인
        self.assertEqual(response.status_code, 200)

        # 테스트 셋업 데이터 + 테스트 함수
        self.assertEqual(Reply.objects.count(), 2)

        # 생성된 댓글 정상 저장 확인
        reply = Reply.objects.first()
        self.assertEqual(reply.feed_id, self.feed.id)
        self.assertEqual(reply.reply_content, 'Test reply')
        self.assertEqual(reply.email, self.user.email)

    def testToggleLike(self):
        # 세션에 이메일 저장
        session = self.client.session
        session['email'] = self.user.email
        session.save()

        test_toggle_like_feed = Feed.objects.create(email=self.user.email, content="Toggle like test feed content",
                                                    image="toggle_like_feed.jpg")

        data = {
            'feed_id': test_toggle_like_feed.id,
            'favorite_text': 'favorite'
        }

        response = self.client.post(reverse('toggle_like'), data)

        # 응답 상태 코드 확인
        self.assertEqual(response.status_code, 200)

        # Like 객체가 생성되었는지 확인
        self.assertEqual(Like.objects.count(), 3)

        # 생성된 Like 객체의 is_like 값 확인
        like = Like.objects.last()
        self.assertTrue(like.is_like)

        # 좋아요 상태가 올바르게 저장되었는지 확인
        self.assertEqual(like.feed_id, test_toggle_like_feed.id)
        self.assertEqual(like.email, self.user.email)



