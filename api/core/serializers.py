from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from taggit.models import Tag

from .models import Post, Comment, UserPostRelation
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer
from django.contrib.auth.models import User


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ("name", "slug")
        lookup_field = 'name'
        extra_kwargs = {
            'url': {'lookup_field': 'name'}
        }

class PostAppreciatedSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')

class PostSerializer(TaggitSerializer, serializers.ModelSerializer):

    tags = TagSerializer(many=True, read_only=True)
    # author = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())
    author = serializers.CharField(source='author.username', default='', read_only=True)
    # like_count = serializers.SerializerMethodField()
    annotated_likes = serializers.IntegerField(read_only=True)
    rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)
    appreciated = PostAppreciatedSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = '__all__'
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }

    # def get_like_count(self, instance):
    #     return UserPostRelation.objects.filter(post=instance, like=True).count()

class ContactSerializer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.CharField()
    subject = serializers.CharField()
    message = serializers.CharField()


class RegisterSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "password2"
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        username = validated_data["username"]
        password = validated_data["password"]
        password2 = validated_data["password2"]
        if password != password2:
            raise serializers.ValidationError({"password": "Пароли не совпадают!!!"})
        user = User(username=username)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())
    post = serializers.SlugRelatedField(slug_field="slug", queryset=Post.objects.all())

    class Meta:
        model = Comment
        fields = '__all__'
        lookup_field = 'id'
        extra_kwargs = {
            'url': {'lookup_field': 'id'}
        }

class UserPostRelationSerializer(ModelSerializer):
    class Meta:
        model = UserPostRelation
        fields = ('user', 'post', 'like', 'is_favorites', 'rate')
