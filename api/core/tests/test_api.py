from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.models import Post
from core.serializers import PostSerializer


class TravelApiTestCase(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user('user')
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

    def test_post(self):
        url = reverse('posts-details')
        response = self.client.post(url)

        serializer_data = PostSerializer(self.post1)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])