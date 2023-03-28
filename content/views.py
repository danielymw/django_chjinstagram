from uuid import uuid4
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Feed, Reply, Like, Bookmark
from user.models import User
import os
from Jinstagram.settings import MEDIA_ROOT


# 메인 페이지
class Main(APIView):
    def get(self, request):
        email = request.session.get('email', None)

        if email is None:
            return render(request, "user/login.html")

        user = User.objects.filter(email=email).first()
        # print(user)

        if user is None:
            return render(request, "user/login.html")

        feed_object_list = Feed.objects.all().order_by('-id')  # select  * from content_feed;
        feed_list = []

        for feed in feed_object_list:
            writer = User.objects.filter(email=feed.email).first()
            #
            reply_object_list = Reply.objects.filter(feed_id=feed.id)
            reply_list = []
            for reply in reply_object_list:
                replier = User.objects.filter(email=reply.email).first()
                reply_list.append(dict(reply_content=reply.reply_content,
                                       nickname=replier.nickname))
            like_count=Like.objects.filter(feed_id=feed.id, is_like=True).count()
            is_liked=Like.objects.filter(feed_id=feed.id, email=email, is_like=True).exists()
            is_marked=Bookmark.objects.filter(feed_id=feed.id, email=email, is_marked=True).exists()
            feed_list.append(dict(id=feed.id,
                                  image=feed.image,
                                  content=feed.content,
                                  like_count=like_count,
                                  profile_image=writer.profile_image,
                                  nickname=writer.nickname,
                                  reply_list=reply_list,
                                  is_liked=is_liked,
                                  is_marked=is_marked
                                  ))
            # print(feed_list)
        return render(request, "jinstagram/main.html", context=dict(feeds=feed_list, user=user))

# 피드 업로드
class UploadFeed(APIView):
    def post(self, request):

        # 일단 파일 불러와
        file = request.FILES['file']

        save_path = os.path.join(MEDIA_ROOT, file.name)

        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        asdf = file.name
        content123 = request.data.get('content')
        email = request.session.get('email', None)

        Feed.objects.create(image=asdf, content=content123, email=email)

        return Response(status=200)

# 프로필 페이지
class Profile(APIView):
    def get(self, request):
        email = request.session.get('email', None)

        if email is None:
            return render(request, "user/login.html")

        user = User.objects.filter(email=email).first()

        if user is None:
            return render(request, "user/login.html")

        feed_list = Feed.objects.filter(email=email)
        like_list = list(Like.objects.filter(email=email, is_like=True).values_list('feed_id', flat=True))
        like_feed_list = Feed.objects.filter(id__in=like_list)
        bookmark_list = list(Bookmark.objects.filter(email=email, is_marked=True).values_list('feed_id', flat=True))
        bookmark_feed_list = Feed.objects.filter(id__in=bookmark_list)
        return render(request, 'content/profile.html', context=dict(feed_list=feed_list,
                                                                    like_feed_list=like_feed_list,
                                                                    bookmark_feed_list=bookmark_feed_list,
                                                                    user=user))

# 댓글 게시
class UploadReply(APIView):
    def post(self, request):
        email = request.session.get('email', None)

        if email is None:
            return render(request, "user/login.html")

        user = User.objects.filter(email=email).first()

        if user is None:
            return render(request, "user/login.html")

        feed_id = request.data.get('feed_id', None)
        reply_content = request.data.get('reply_content', None)
        email = request.session.get('email', None)

        Reply.objects.create(feed_id=feed_id, reply_content=reply_content, email=email)

        return Response(status=200)

# 댓글 수정
class EditReply(APIView):
    def post(self, request, pk):
        print("test")


# 댓글 삭제
class DeleteReply(APIView):
    def get(self, request, pk):
        email = request.session.get('email', None)

        if email is None:
            return render(request, "user/login.html")

        user = User.objects.filter(email=email).first()

        if user is None:
            return render(request, "user/login.html")

        # 댓글
        reply = get_object_or_404(Reply, id=pk)
        if reply==email:
            reply.delete()
            return redirect('main')

# 좋아요 기능
class ToggleLike(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        favorite_text = request.data.get('favorite_text', True)

        if favorite_text == 'favorite_border':
            is_like = True
        else:
            is_like = False
        email = request.session.get('email', None)

        like = Like.objects.filter(feed_id=feed_id, email=email).first()

        if like:
            like.is_like = is_like
            like.save()
        else:
            Like.objects.create(feed_id=feed_id, is_like=is_like, email=email)

        return Response(status=200)

# 북마크 기능
class ToggleBookmark(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        bookmark_text = request.data.get('bookmark_text', True)

        if bookmark_text == 'bookmark_border':
            is_marked = True
        else:
            is_marked = False
        email = request.session.get('email', None)

        bookmark = Bookmark.objects.filter(feed_id=feed_id, email=email).first()

        if bookmark:
            bookmark.is_marked = is_marked
            bookmark.save()
        else:
            Bookmark.objects.create(feed_id=feed_id, is_marked=is_marked, email=email)

        return Response(status=200)

# 피드 상세 보기
class feedDetail(APIView):

    def get(self, request, pk):

        email = request.session.get('email', None)

        if email is None:
            return render(request, "user/login.html")

        user = User.objects.filter(email=email).first()

        if user is None:
            return render(request, "user/login.html")

        # feed = get_object_or_404(Feed, id=pk)
        # context = {
        #     'feed': feed,
        # }

        # 피드 가져 오기
        feed = Feed.objects.get(id=pk)
        # 작성자
        writer = User.objects.filter(email=feed.email).first()
        # 댓글
        reply_object_list = Reply.objects.filter(feed_id=feed.id)
        reply_list = []

        for reply in reply_object_list:
            replier = User.objects.filter(email=reply.email).first()
            reply_list.append(dict(id=reply.id, reply_content=reply.reply_content,
                                   nickname=replier.nickname))
        # 좋아요, 북마크
        like_count = Like.objects.filter(feed_id=feed.id, is_like=True).count()
        is_liked = Like.objects.filter(feed_id=feed.id, email=email, is_like=True).exists()
        is_marked = Bookmark.objects.filter(feed_id=feed.id, email=email, is_marked=True).exists()

        # 가져온 피드 정보
        context = {
            'feed': feed,
            'reply_list': reply_list,
            'writer': writer,
            'user': user,
            'like_count': like_count,
            'is_liked': is_liked,
            'is_marked': is_marked
        }
        return render(request, 'content/feedDetail.html',  context)

# 피드 수정
class feedEdit(APIView):
    def get(self, request, pk):
        feed = get_object_or_404(Feed, id=pk)

        email = request.session.get('email', None)

        if email is None:
            return render(request, "user/login.html")

        user = User.objects.filter(email=email).first()

        if user is None:
            return render(request, "user/login.html")

        # 작성자
        writer = User.objects.filter(email=feed.email).first()
        context = {
            'feed': feed,
            'writer': writer,
            'user': user,
        }

        return render(request, 'content/feedEdit.html', context)

    def post(self, request, pk):
        email = request.session.get('email', None)

        if email is None:
            return render(request, "user/login.html")

        user = User.objects.filter(email=email).first()

        if user is None:
            return render(request, "user/login.html")

        feed = get_object_or_404(Feed, id=pk)

        # feed.image = uuid_name
        feed.content = request.data.get('content')

        # feed.email = request.session.get('email', None)
        #
        feed.save()

        return redirect('main')

# 피드 수정 완료
class feedUpdate(APIView):
    def post(self, request):
        return render(request, 'content/feedUpdate.html')

# 피드 삭제
class feedDelete(APIView):
    def get(self, request, pk):
        email = request.session.get('email', None)

        if email is None:
            return render(request, "user/login.html")

        user = User.objects.filter(email=email).first()

        if user is None:
            return render(request, "user/login.html")

        feed = get_object_or_404(Feed, id=pk)
        if feed.email==email:
            feed.delete()
            return redirect('main')
        else:
            return Response(status=404)

# WJ 어드민 로그인 페이지 성공시 아래의 AdminPage 클래스에 content 내용들 보내기
class AdminPage(APIView):
    # WJ 유저 DB 출력 : 앱의 views.py 파일에서 쿼리를 실행하고 데이터베이스에서 데이터를 가져올 뷰를 생성
    def get(self, request):
        feeds = Feed.objects.all()
        content_feed = {'content_feed': feeds}
        return render(request, 'user/adminpage.html', content_feed)


class AdminPageFeed(APIView):
    # WJ 유저 DB 출력 : 앱의 views.py 파일에서 쿼리를 실행하고 데이터베이스에서 데이터를 가져올 뷰를 생성
    def get(self, request):
        feed = Feed.objects.all()
        content_feed = {'content_feed': feed}
        return render(request, 'content/adminpagefeed.html', content_feed)
