from django.urls import path
from .views import Join, Login, LogOut, UploadProfile, SearchUser

urlpatterns = [
    path('join', Join.as_view()),
    path('login', Login.as_view()),
    path('logout', LogOut.as_view()),
    path('profile/upload', UploadProfile.as_view()),
    path('search/', SearchUser.as_view(), name='user-search')
    # 검색 url 추가
]

