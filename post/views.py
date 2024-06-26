from django.shortcuts import render

from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Comment, Like, Post
from .serializers import CommentSerializer, LikeSerializer, PostSerializer

class PostView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)

        return Response(
            {
                'success': True,
                'message': 'Fetched all posts',
                'data': serializer.data,
                'status': status.HTTP_200_OK,
                'code': 'created'
            },
            status.HTTP_200_OK
        )

    def post(self, request):
        data = request.data
        data['author'] = request.user.id
        serializer = PostSerializer(data = data)

        if not serializer.is_valid():
            return Response(
                {
                    'success': False,
                    'message': 'Validation Error',
                    'data': serializer.errors,
                    'status': status.HTTP_400_BAD_REQUEST,
                    'code': 'bad request'
                },
                status.HTTP_400_BAD_REQUEST
            )
        
        serializer.save()

        return Response(
            {
                'success': True,
                'message': 'Post Created',
                'data': serializer.data,
                'status': status.HTTP_201_CREATED,
                'code': 'created'
            },
            status.HTTP_201_CREATED
        )

    def put(self, request):
        data = request.data
        data["author"] = request.user.id

        if 'id' not in data:
            return Response(
                {
                    'success': False,
                    'message': 'Post id is required',
                    'status': status.HTTP_400_BAD_REQUEST,
                    'code': 'bad request'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            post = Post.objects.get(id=data['id'])
        except Post.DoesNotExist:
            return Response(
                {
                    'success': False,
                    'message': 'Post not found',
                    'status': status.HTTP_404_NOT_FOUND,
                    'code': 'not found'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = PostSerializer(post, data=data)

        if not serializer.is_valid():
            return Response(
                {
                    'success': False,
                    'message': 'Validation Error',
                    'data': serializer.errors,
                    'status': status.HTTP_400_BAD_REQUEST,
                    'code': 'bad request'
                },
                status.HTTP_400_BAD_REQUEST
            )

        serializer.save()

        return Response(
            {
                'success': True,
                'message': 'Post Updated',
                'data': serializer.data,
                'status': status.HTTP_201_CREATED,
                'code': 'created'
            },
            status.HTTP_201_CREATED
        )

    def patch(self, request):
        data = request.data
        data["author"] = request.user.id

        if 'id' not in data:
           return Response(
                {
                    'success': False,
                    'message': 'Post id is required',
                    'status': status.HTTP_400_BAD_REQUEST,
                    'code': 'bad request'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try: 
            post = Post.objects.get(id=data['id'])
        except Post.DoesNotExist:
            return Response(
                {
                    'success': False,
                    'message': 'Post not found',
                    'status': status.HTTP_404_NOT_FOUND,
                    'code': 'not found'
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = PostSerializer(post, data=data, partial=True)

        if not serializer.is_valid():
            return Response(
                {
                    'success': False,
                    'message': 'Validation Error',
                    'data': serializer.errors,
                    'status': status.HTTP_400_BAD_REQUEST,
                    'code': 'bad request'
                },
                status.HTTP_400_BAD_REQUEST
            )
        
        serializer.save()

        return Response(
            {
                'success': True,
                'message': 'Post Updated',
                'data': serializer.data,
                'status': status.HTTP_201_CREATED,
                'code': 'created'
            },
            status.HTTP_201_CREATED
        )

    def delete(self, request):
        data = request.data

        if 'id' not in data:
            return Response(
                {
                    'success': False,
                    'message': 'Post id is required',
                    'status': status.HTTP_400_BAD_REQUEST,
                    'code': 'bad request'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            post = Post.objects.get(id=data["id"])
        except Post.DoesNotExist:
            return Response(
                {
                    'success': False,
                    'message': 'Post not found',
                    'status': status.HTTP_404_NOT_FOUND,
                    'code': 'not found'
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        post.delete()

        return Response(
            {
                'success': True,
                'message': 'Post Deleted',
                'status': status.HTTP_200_OK,
                'code': 'Ok'
            },
            status.HTTP_200_OK
        )


class PostDetailView(APIView):
    def get(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
        except Post.DoesNotExist:
            return Response(
                {
                    'success': False,
                    'message': 'Post not found',
                    'status': status.HTTP_404_NOT_FOUND,
                    'code': 'not found'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = PostSerializer(post)

        return Response(
            {
                'success': True,
                'message': 'Post Fetched',
                'data': serializer.data,
                'status': status.HTTP_200_OK,
                'code': 'Ok'
            },
            status.HTTP_200_OK
        )


class CommentView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, pk):
        comments = Comment.objects.filter(post=pk)

        if not comments.exists():
            return Response(
                {
                    'success': False,
                    'message': 'Comments not found',
                    'status': status.HTTP_404_NOT_FOUND,
                    'code': 'not found'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CommentSerializer(comments, many=True)

        return Response(
            {
                'success': True,
                'message': 'Comments Fetched',
                'data': serializer.data,
                'status': status.HTTP_200_OK,
                'code': 'Ok'
            },
            status.HTTP_200_OK
        )

    def post(self, request, pk):
        data = request.data
        data['post'] = pk
        data['author'] = request.user.id

        serializer = CommentSerializer(data=data)

        if not serializer.is_valid():
            return Response(
                {
                    'success': False,
                    'message': 'Validation Error',
                    'data': serializer.errors,
                    'status': status.HTTP_400_BAD_REQUEST,
                    'code': 'bad request'
                },
                status.HTTP_400_BAD_REQUEST
            )

        serializer.save()

        return Response(
            {
                'success': True,
                'message': 'Comment Created',
                'data': serializer.data,
                'status': status.HTTP_201_CREATED,
                'code': 'created'
            },
            status.HTTP_201_CREATED
        )

    def patch(self, request, pk):
        data = request.data
        try:
            comment = Comment.objects.get(id=pk)
        except Comment.DoesNotExist:
            return Response(
                {
                    'success': False,
                    'message': 'Comment not found',
                    'status': status.HTTP_404_NOT_FOUND,
                    'code': 'not found'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CommentSerializer(comment, data=data, partial=True)

        if not serializer.is_valid():
            return Response(
                {
                    'success': False,
                    'message': 'Validation Error',
                    'data': serializer.errors,
                    'status': status.HTTP_400_BAD_REQUEST,
                    'code': 'bad request'
                },
                status.HTTP_400_BAD_REQUEST
            )
        
        serializer.save()

        return Response(
            {
                'success': True,
                'message': 'Comment Updated',
                'data': serializer.data,
                'status': status.HTTP_201_CREATED,
                'code': 'created'
            },
            status.HTTP_201_CREATED
        )

    def delete(self, request, pk):
        try:
            comment = Comment.objects.get(id=pk)
        except Comment.DoesNotExist:
            return Response(
                {
                    'success': False,
                    'message': 'Comment not found',
                    'status': status.HTTP_404_NOT_FOUND,
                    'code': 'not found'
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        comment.delete()

        return Response(
            {
                'success': True,
                'message': 'Comment Deleted',
                'status': status.HTTP_200_OK,
                'code': 'Ok'
            },
            status.HTTP_200_OK
        )


class LikeView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, pk):
        likes = Like.objects.filter(post=pk)

        if not likes.exists():
            return Response(
                {
                    'success': False,
                    'message': 'Likes not found',
                    'status': status.HTTP_404_NOT_FOUND,
                    'code': 'not found'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = LikeSerializer(likes, many=True)
        
        return Response(
            {
                'success': True,
                'message': 'Like Fetched',
                'data': serializer.data,
                'status': status.HTTP_200_OK,
                'code': 'Ok'
            },
            status.HTTP_200_OK
        )
    
    def post(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response(
                {
                    'success': False,
                    'message': 'Post not found',
                    'status': status.HTTP_404_NOT_FOUND,
                    'code': 'not found'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        like, created = Like.objects.get_or_create(post=post, user=request.user)

        if created:
            message = 'Post Liked'
        else:
            like.delete()
            message = 'Post unliked'

        return Response(
            {
                'success': True,
                'message': message,
                'status': status.HTTP_200_OK,
                'code': 'Ok'
            },
            status.HTTP_200_OK
        )
