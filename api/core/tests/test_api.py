import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.models import Post
from core.serializers import PostSerializer


class TravelApiTestCase(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create(username='test_user')
        self.post1 = Post.objects.create(h1='test post 1', title='post1', slug='post1', description='test',
                                         content='user', author=self.test_user)
        self.post2 = Post.objects.create(h1='test post 2', title='post2', slug='post2', description='test1',
                                         content='user1', author=self.test_user)
    def test_get(self):
        url = reverse('posts-list')
        response = self.client.get(url)
        serializer_data = PostSerializer([self.post1, self.post2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

    def test_create(self):
        self.assertEqual(2, Post.objects.all().count())
        url = reverse('posts-list')
        data = {
            "h1": "test post",
            "title": "test post",
            "slug": "test_post",
            "description": "test1",
            "content": "user1",
            "author": self.test_user.username
        }
        json_data = json.dumps(data)
        self.client.force_login(self.test_user)
        response = self.client.post(url, data=json_data, content_type="application/json")
        self.assertEqual(self.test_user, Post.objects.last().author)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(3, Post.objects.all().count())



    def test_update(self):
        url = reverse('posts-detail', args=(self.post1.slug,))
        data = {
            "h1": "test post 1",
            "title": "test post 1",
            "slug": "post1",
            "description": "test description",
            "content": "user1",
            "author": "user"
        }
        json_data = json.dumps(data)
        self.client.force_login(self.test_user)
        response = self.client.put(url, data=json_data, content_type="application/json")
        self.assertEqual(2, Post.objects.all().count())
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_delete(self):
        self.assertEqual(2, Post.objects.all().count())
        url = reverse('posts-detail', args=(self.post1.slug,))
        data = {
            "h1": "test post 1",
            "title": "test post 1",
            "slug": "post1",
            "description": self.post1.description,
            "content": "user1",
            "author": "user"
        }
        json_data = json.dumps(data)
        self.client.force_login(self.test_user)
        response = self.client.delete(url, data=json_data, content_type="application/json")
        self.assertEqual(1, Post.objects.all().count())
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
