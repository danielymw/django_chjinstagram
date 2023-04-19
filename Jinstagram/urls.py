"""Jinstagram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from content.views import Main, UploadFeed
from .settings import MEDIA_URL, MEDIA_ROOT
from django.conf.urls.static import static
from django.contrib.auth import get_user_model
from .views import index
from . import views
from django.views.generic import RedirectView
User = get_user_model()

handler404 = views.custom_404
handler500 = views.custom_500

urlpatterns = [
    # 그냥 링크 검색 시 자동으로 main으로 가게 함.
    path('', RedirectView.as_view(url='/main')),
    path('main/', Main.as_view()),
    path('content/', include('content.urls')),
    path('user/', include('user.urls')),
    path('index/', index, name='index'),
]

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
