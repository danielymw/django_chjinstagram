from django.urls import path, include
from .views import UploadFeed, Profile, Main, UploadReply, ToggleLike, ToggleBookmark, feedDetail,feedEdit, feedDelete

urlpatterns = [
    path('upload', UploadFeed.as_view()),
    path('reply', UploadReply.as_view()),
    path('like', ToggleLike.as_view()),
    path('bookmark', ToggleBookmark.as_view()),
    path('profile', Profile.as_view()),
    path('main', Main.as_view()),
    path('detail/<int:pk>', feedDetail.as_view()),
    path('edit/<int:pk>', feedEdit.as_view()),
    path('delete/<int:pk>', feedDelete.as_view())
]

