import os
from uuid import uuid4

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from django.contrib.auth.hashers import make_password
from Jinstagram.settings import MEDIA_ROOT
from django.db.models import Q, Prefetch
# Prefetch 추가
from django.views import View



class Join(APIView):
    def get(self, request):
        return render(request, "user/join.html")

    def post(self, request):
        # TODO 회원가입
        email = request.data.get('email', None)
        nickname = request.data.get('nickname', None)
        name = request.data.get('name', None)
        password = request.data.get('password', None)

        User.objects.create(email=email,
                            nickname=nickname,
                            name=name,
                            password=make_password(password),
                            profile_image="default_profile.png")

        return Response(status=200)


class Login(APIView):
    def get(self, request):
        return render(request, "user/login.html")

    def post(self, request):
        # TODO 로그인
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        user = User.objects.filter(email=email).first()

        if user is None:
            return Response(status=400, data=dict(message="회원정보가 잘못되었습니다."))

        if user.check_password(password):
            # TODO 로그인을 했다. 세션 or 쿠키
            request.session['email'] = email
            return Response(status=200)
        else:
            return Response(status=400, data=dict(message="회원정보가 잘못되었습니다."))


class LogOut(APIView):
    def get(self, request):
        request.session.flush()
        return render(request, "user/login.html")




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




class SearchUser(View):
    def get(self, request):
        query = request.GET.get('q', '')
        if query:
            users = User.objects.filter(Q(email__icontains=query) | Q(nickname__icontains=query))
        else:
            users = User.objects.none()
        return render(request, 'user/search.html', {"users": users})

'''

'''
<?php
// Include the necessary PHP files
require_once 'db.php'; // Your database connection file
require_once 'models/user.php'; // Your user model file
require_once 'templates/search.php'; // Your search results template file

// Get the search query from the request
$query = $_GET['q'];

if ($query) {
  // Prepare the SQL query with the search term
  $sql_query = "SELECT * FROM users WHERE email LIKE '%$query%' OR nickname LIKE '%$query%'";

  // Execute the query
  $result = mysqli_query($conn, $sql_query);

  // Check if the query returned any results
  if (mysqli_num_rows($result) > 0) {
    // Loop through the results and store them in an array
    $users = array();
    while ($row = mysqli_fetch_assoc($result)) {
      $users[] = new User($row['id'], $row['email'], $row['nickname']); // Instantiate a new user object
    }
  } else {
    // No results found
    $users = array();
  }
} else {
  // No query provided
  $users = array();
}

// Render the search results in the HTML template
include 'templates/search.php';
?>






# 검색 기능 추가
# WJ 어드민 로그인 페이지 (데이터베이스 값을 가져오지 않음)
class Admin(APIView):
    def get(self, request):
        # admin_login.html 랜더링
        return render(request, "user/admin.html")

    def post(self, request):
        # TODO Login
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        if email == 'rhksflwk' and password == 'rhksflwk':
            request.session['email'] = email
            return Response(status=200)
        else:
            return Response(status=200)


# WJ 어드민 로그인 페이지 성공시 아래의 AdminPage 클래스로
class AdminPage(APIView):
    # WJ 유저 DB 출력 : 앱의 views.py 파일에서 쿼리를 실행하고 데이터베이스에서 데이터를 가져올 뷰를 생성
    def get(self, request):
        users = User.objects.all()
        context = {'users': users}
        return render(request, 'user/adminpage.html', context)





'''
    def get(self, request):
        # admin_login.html 랜더링
        return render(request, "user/adminpage.html")

    def post(self, request):
        # TODO 로그인
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        user = User.objects.filter(email=email).first()

        if user is None:
            return Response(status=400, data=dict(message="관리자정보가 잘못되었습니다."))

        if user.check_password(password):
            # TODO 로그인을 했다. 세션 or 쿠키
            request.session['email'] = email
            return Response(status=200)
        else:
            return Response(status=400, data=dict(message="관리자정보가 잘못되었습니다."))
'''

