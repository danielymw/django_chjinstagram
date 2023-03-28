from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
User = get_user_model()

class Sub(APIView):
    def get(self, request):
        print("겟으로 호출")
        return render(request, "jinstagram/main.html")

    def post(self, request):
        print("포스트로 호출")
        return render(request, "jinstagram/main.html")


