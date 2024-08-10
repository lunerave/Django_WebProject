from django.urls import path

from chat.views import Chat

urlpatterns = [
    path('', Chat.as_view()),
]
