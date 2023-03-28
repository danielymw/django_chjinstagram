from django.urls import path
from .views import UploadFeed, Profile, Main, UploadReply, ToggleLike, ToggleBookmark, AdminPage, AdminPageFeed

urlpatterns = [
    path('upload', UploadFeed.as_view()),
    path('reply', UploadReply.as_view()),
    path('like', ToggleLike.as_view()),
    path('bookmark', ToggleBookmark.as_view()),
    path('profile', Profile.as_view()),
    path('main', Main.as_view()),
    # WJ 어드민 페이지에 피드값 경로지정
    path('adminpage', AdminPage.as_view()),
    # WJ 어드민페이지피드 경로지정
    path('adminpagefeed', AdminPageFeed.as_view()),
]

