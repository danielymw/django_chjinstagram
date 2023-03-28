from django.urls import path
from .views import UploadFeed, Profile, Main, UploadReply, ToggleLike, ToggleBookmark, AdminPage, AdminPageFeed
from django.urls import path, include
from .views import UploadFeed, Profile, Main, UploadReply, ToggleLike, \
    ToggleBookmark, feedDetail,feedEdit, feedUpdate, feedDelete,\
    DeleteReply, EditReply

urlpatterns = [
    # 피드 업로드 url
    path('upload', UploadFeed.as_view()),
    # 피드 댓글 게시 url
    path('reply', UploadReply.as_view()),
    # 피드 댓글 수정 url
    path('reply/edit/<int:pk>', EditReply.as_view()),
    # 피드 댓글 수정 url
    path('reply/delete/<int:pk>', DeleteReply.as_view()),
    # 피드 좋아요 url
    path('like', ToggleLike.as_view()),
    # 피드 북마크 url
    path('bookmark', ToggleBookmark.as_view()),
    # 프로필 url
    path('profile', Profile.as_view()),
    path('main', Main.as_view()),
    # WJ 어드민 페이지에 피드값 경로지정
    path('adminpage', AdminPage.as_view()),
    # WJ 어드민페이지피드 경로지정
    path('adminpagefeed', AdminPageFeed.as_view()),
    # 메인 url
    path('main', Main.as_view(), name='main'),
    # 피드 상세 url
    path('detail/<int:pk>', feedDetail.as_view()),
    # 피드 수정 url
    path('edit/<int:pk>', feedEdit.as_view()),
    # 피드 수정 후 url
    path('update/<int:pk>', feedUpdate.as_view()),
    # 피드 삭제 url
    path('delete/<int:pk>', feedDelete.as_view())
]

