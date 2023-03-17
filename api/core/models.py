import datetime

from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from taggit.managers import TaggableManager


class Post(models.Model):
    """Модель поста"""
    h1 = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    description = RichTextUploadingField()
    content = RichTextUploadingField()
    image = models.ImageField(default=None)
    created_at = models.DateField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.SET_NULL,
                               null=True, related_name='my_posts')
    appreciated = models.ManyToManyField(User, through='UserPostRelation',
                                         related_name='posts')
    tags = TaggableManager()

    def __str__(self):
        return self.title


class Comment(models.Model):
    """Модель комментариев"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_name')
    text = models.TextField()
    created_date = models.DateField(default=datetime.datetime)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.text


class UserPostRelation(models.Model):
    """Модель рэйтинга"""
    RATE_CHOICES = (
        (1, 'Bad'),
        (2, 'Not bad'),
        (3, 'Normal'),
        (4, 'Good'),
        (5, 'Very good')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    is_favorites = models.BooleanField(default=False)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES, null=True)

    def __str__(self):
        return f'{self.user.username}: {self.post.title}, RATE {self.rate}'
