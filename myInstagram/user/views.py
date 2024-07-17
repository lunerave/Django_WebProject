import os
from uuid import uuid4
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from django.contrib.auth.hashers import make_password
from myInstagram.settings import MEDIA_ROOT


# Create your views here.
class Join(APIView):
    def get(self, request):
        return render(request, 'user/join.html')

    def post(self, request):
        email = request.data.get('email', None)
        nickname = request.data.get('nickname', None)
        name = request.data.get('name', None)
        password = request.data.get('password', None)

        User.objects.create(email=email, nickname=nickname, name=name, password=make_password(password), profile_img='default_profile.jpg')

        return Response(status=200)


class Login(APIView):
    def get(self, request):
        return render(request, 'user/login.html')

    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        user = User.objects.filter(email=email).first()

        if user is None:
            return Response(status=400, data=dict(message="회원 정보가 잘못되었습니다."))

        if user.check_password(password):
            # 로그인 성공. 세션 or 쿠키
            request.session['email'] = email
            return Response(status=200)
        else:
            return Response(status=400, data=dict(message="회원 정보가 잘못되었습니다."))


class Logout(APIView):
    def get(self, request):
        request.session.flush()
        return render(request, 'user/login.html')


class UploadProfile(APIView):
    def post(self, request):
        file = request.FILES['file']
        uuid_name = uuid4().hex
        save_path = os.path.join(MEDIA_ROOT, uuid_name)

        # 실제로 파일을 저장하는 코드
        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        profile_img = uuid_name

        email = request.data.get('email')

        user = User.objects.filter(email=email).first()

        user.profile_img = profile_img
        user.save()

        return Response(status=200)

