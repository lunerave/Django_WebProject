from django.urls import path
from .views import UploadFeed, Profile, Main, UploadReply, ToggleLike, ToggleBookmark, DeleteFeed

urlpatterns = [
    path('delete', DeleteFeed.as_view()),
    path('bookmark', ToggleBookmark.as_view()),
    path('like', ToggleLike.as_view()),
    path('reply', UploadReply.as_view(), name='upload_reply'),
    path('upload', UploadFeed.as_view(), name='upload_feed'),
    path('profile', Profile.as_view(), name='profile'),
    path('main', Main.as_view(), name='main'),
]


