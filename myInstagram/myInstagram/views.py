from django.shortcuts import render
from rest_framework.views import APIView


class Sub(APIView):
    def get(self, request):
        print("get 호출")
        return render(request, "myInstagram/main.html")
