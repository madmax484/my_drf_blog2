
from django.core.mail import send_mail
from django.db.models import Count, Case, When, Avg
from rest_framework import viewsets, pagination, generics, filters
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from taggit.models import Tag

from .permissions import IsAuthorOrStaffOrReadOnly
from .serializers import PostSerializer, TagSerializer, ContactSerializer, RegisterSerializer, UserSerializer, \
    CommentSerializer, UserPostRelationSerializer
from .models import Post, Comment, UserPostRelation
from rest_framework.response import Response
from rest_framework import permissions


class PageNumberSetPagination(pagination.PageNumberPagination):
    page_size = 6
    page_query_param = 'page_size'
    ordering = 'created_at'

class PostViewSet(viewsets.ModelViewSet):
    search_fields = ['$content', '$h1']
    filter_backends = (filters.SearchFilter,)
    serializer_class = PostSerializer
    queryset = Post.objects.all().annotate(annotated_likes=Count(Case(When(userpostrelation__like=True, then=1))),
                                            rating=Avg('userpostrelation__rate')
                                            )
    lookup_field = 'slug'
    permission_classes = [IsAuthorOrStaffOrReadOnly]
    pagination_class = PageNumberSetPagination

    def perform_create(self, serializer):
        serializer.validated_data['author'] = self.request.user
        serializer.save()

class TagDetailView(generics.ListAPIView):
    serializer_class = PostSerializer
    pagination_class = PageNumberSetPagination
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        tag_slug = self.kwargs['tag_slug'].lower()
        tag = Tag.objects.get(slug=tag_slug)
        return Post.objects.filter(tags=tag)

class TagView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]

class AsideView(generics.ListAPIView):
    queryset = Post.objects.all().order_by('-id')[:5]
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]

class FeedBackView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ContactSerializer

    def post(self, request, *args, **kwargs):
        serializer_class = ContactSerializer(data=request.data)
        if serializer_class.is_valid():
            data = serializer_class.validated_data
            name = data.get('name')
            from_email = data.get('email')
            subject = data.get('subject')
            message = data.get('message')
            send_mail(f'От {name} | {subject}', message, from_email, ['levchenkomaksmsk@gmail.com'])
            return Response({"success": "Sent"})


class RegisterView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "Пользователь успешно создан!",
        })


class ProfileView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return Response({
            "user": UserSerializer(request.user, context=self.get_serializer_context()).data,
        })


class CommentView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        post_slug = self.kwargs['post_slug'].lower()
        for slug in range(len(Post.objects.all())):
            if str(Post.objects.all()[slug]).lower() == post_slug:
                return Comment.objects.filter(post=slug + 1)
        # post = Post.objects.get(slug=post_slug)
        # return Comment.objects.filter(post=post)

class UserPostRelationView(UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserPostRelation.objects.all()
    serializer_class = UserPostRelationSerializer
    lookup_field = 'post'

    def get_object(self):
        obj, created = UserPostRelation.objects.get_or_create(user=self.request.user,
                                                        post_id=self.kwargs['post'])
        return obj

