from django.contrib import admin
from django.urls import path

from .views import CommentView, LikeView, PostDetailView, PostView

urlpatterns = [
    path('post/', PostView.as_view()),
    path('post-detail/<int:pk>', PostDetailView.as_view()),
    path('post/comment/<int:pk>', CommentView.as_view()),
    path('post/like/<int:pk>', LikeView.as_view()),
]
