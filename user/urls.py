from django.urls import path
from .views import Join, Login, LogOut, UploadProfile, Admin, AdminPage, SearchUser

urlpatterns = [
    path('join', Join.as_view()),
    path('login', Login.as_view()),
    path('logout', LogOut.as_view()),
    path('profile/upload', UploadProfile.as_view()),
    path('search/', SearchUser.as_view(), name='user-search'),
    # 검색 url 추가
    # WJ user 앱에서 admin 경로를 만들고 view.py의 Admin 클래스 참조
    path('admin', Admin.as_view()),
    # WJ user 앱에서 admin 경로 성공 시 user/adminpage 경로를 새로 만듬, view.py의 AdminDb 클래스 참조
    path('adminpage', AdminPage.as_view()),
]

