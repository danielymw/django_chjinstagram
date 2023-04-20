import os
import re
from uuid import uuid4

from django.contrib.auth.models import User

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from Jinstagram.settings import MEDIA_ROOT
from django.db.models import Q, Prefetch
# Prefetch 추가
from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
import time
from django.core.cache import cache
from datetime import timedelta

from django.core.cache import cache
from datetime import datetime, timedelta



# 회원가입
class Join(APIView):
    def get(self, request):
        return render(request, "user/join.html")

    def post(self, request):
        # Join TODO
        email = request.data.get('email', None)
        nickname = request.data.get('nickname', None)
        name = request.data.get('name', None)
        password = request.data.get('password', None)

        # WJ 패스워드 정책 설정
        if len(password) >= 8:
            has_uppercase = False
            has_lowercase = False
            has_number = False
            has_special = False
            for char in password:
                if char.isupper():
                    has_uppercase = True
                elif char.islower():
                    has_lowercase = True
                elif char.isdigit():
                    has_number = True
                elif char in "!@#$%^&*()-_=+[]{}\\|;:'\",.<>/?`~":
                    has_special = True
            if (has_uppercase + has_lowercase + has_number + has_special) >= 3:
                User.objects.create(email=email,
                                    nickname=nickname,
                                    name=name,
                                    password=make_password(password),
                                    profile_image="default_profile.png")
                return Response(status=200)
            else:
                return Response(status=400)
        else:
            return Response(status=400)


class Login(APIView):
    def get(self, request):
        return render(request, "user/login.html")

    def post(self, request):
        # TODO Login
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        user = User.objects.filter(email=email).first()

        if user is None:
            return Response(status=400, data=dict(message="아이디 또는 비밀번호가 잘못되었습니다."))

        failed_attempts_key = f"failed_attempts:{email}"
        failed_attempts = cache.get(failed_attempts_key, 0)

        if failed_attempts >= 5:
            return Response(status=400, data=dict(message="아이디 또는 패스워드가 잘못 되었습니다. 5번 틀릴 시 5분간 정지됩니다."))

        if user.check_password(password):
            # TODO login. session or cookie
            request.session['email'] = email
            cache.delete(failed_attempts_key)  # reset failed attempts count
            return Response(status=200)
        else:
            failed_attempts += 1
            cache.set(failed_attempts_key, failed_attempts, timeout=timedelta(minutes=5).total_seconds())
            return Response(status=400, data=dict(message="아이디 또는 패스워드가 잘못 되었습니다. 5번 틀릴 시 5분간 정지됩니다."))
        # 비밀번호를 평문 그대로 검증하게 변경

# 로그아웃
class LogOut(APIView):
    def get(self, request):
        request.session.flush()

        # 쿠키에서 CSRF 토큰 삭제
        response = render(request, "user/login.html")
        response.delete_cookie('csrftoken')
        response.delete_cookie('sessionid')

        return response

# 프로필 사진업로드로 파일 업로드 취약점 만들려면 고쳐야되는 코드
class UploadProfile(APIView):
    def post(self, request):

        # 일단 파일 불러와
        file = request.FILES['file']
        email = request.data.get('email')

        uuid_name = uuid4().hex
        save_path = os.path.join(MEDIA_ROOT, uuid_name)

        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        profile_image = uuid_name

        user = User.objects.filter(email=email).first()

        user.profile_image = profile_image
        user.save()

        return Response(status=200)

# 사용자 검색
# 검색 기능 추가 / 검색창 sql 인젝션 가능하게 수정
class SearchUser(APIView):
    def get(self, request):
        query = request.GET.get('q', '')
        if query:
            users = User.objects.filter(Q(email=query) | Q(nickname=query))
        else:
            users = User.objects.none()
        return render(request, 'user/search.html',{"users": users})

# WJ 어드민 로그인 페이지 (데이터베이스 값을 가져오지 않음)
class Admin(APIView):
    def get(self, request):
        # admin_login.html 랜더링
        return render(request, "user/admin.html")

    def post(self, request):
        # TODO Login
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        user = User.objects.filter(email=email).first()

        if user is None:
            return Response(status=400, data=dict(message="회원정보가 없습니다."))

        if user.check_password(password):
            if (user.permission == 2) or (user.permission == 3):
                request.session['email'] = email
                return Response(status=200)
            else:
                return Response(status=400, data=dict(message="관리자가 아닙니다."))

        return Response(status=400, data=dict(message="아이디 또는 패스워드 오류입니다."))

# WJ 어드민 로그인 페이지 성공시 아래의 AdminPage 클래스로
class AdminPage(APIView):
    # WJ 유저 DB 출력 : 앱의 views.py 파일에서 쿼리를 실행하고 데이터베이스에서 데이터를 가져올 뷰를 생성
    def get(self, request):
        email = request.session.get('email', None)

        if email is None:
            return render(request, "user/admin.html")

        user = User.objects.filter(email=email).first()

        if user is None:
            return render(request, "user/admin.html")

        if user.permission is not 3:
            return render(request, "user/admin.html")

        users = User.objects.all()
        context = {'users': users}
        return render(request, 'user/adminpage.html', context)


class Test(APIView):
    def get(self, request):
        request.session.flush()
        return render(request, "user/test.html")