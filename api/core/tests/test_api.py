import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase

from core.models import Post, UserPostRelation
from core.serializers import PostSerializer


class TravelApiTestCase(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create(username="test_user")
        self.post1 = Post.objects.create(h1='test post 1', title='post1', slug='post1', description='test',
                                         content='user', author=self.test_user)
        self.post2 = Post.objects.create(h1='test post 2', title='post2', slug='post2', description='test1',
                                         content='user1')
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
        self.client.force_authenticate(self.test_user)
        response = self.client.post(url, data=json_data, content_type="application/json")
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(self.test_user, Post.objects.last().author)
        self.assertEqual(3, Post.objects.all().count())



    def test_update(self):
        url = reverse('posts-detail', args=(self.post1.slug,))
        data = {
            "h1": self.post1.h1,
            "title": self.post1.title,
            "slug": self.post1.slug,
            "description": "test description",
            "content": self.post1.content,
            "author": self.test_user.username
        }
        json_data = json.dumps(data)
        self.client.force_authenticate(self.test_user)
        response = self.client.put(url, data=json_data, content_type="application/json")
        self.post1.refresh_from_db()
        self.assertEqual(2, Post.objects.all().count())
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('test description', self.post1.description)

    def test_delete(self):
        self.assertEqual(2, Post.objects.all().count())
        url = reverse('posts-detail', args=(self.post1.slug,))
        data = {
            "h1": "test post 1",
            "title": "test post 1",
            "slug": "post1",
            "description": self.post1.description,
            "content": "user1",
            "author": self.test_user.username
        }
        json_data = json.dumps(data)
        self.client.force_authenticate(self.test_user)
        response = self.client.delete(url, data=json_data, content_type="application/json")
        self.assertEqual(1, Post.objects.all().count())
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_update_not_author(self):
        self.test_user2 = User.objects.create(username="test_user2")
        url = reverse('posts-detail', args=(self.post1.slug,))
        data = {
            "h1": self.post1.h1,
            "title": self.post1.title,
            "slug": self.post1.slug,
            "description": "test description",
            "content": self.post1.content,
            "author": self.test_user.username
        }
        json_data = json.dumps(data)
        self.client.force_authenticate(self.test_user2)
        response = self.client.put(url, data=json_data, content_type="application/json")
        self.post1.refresh_from_db()
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual({'detail': ErrorDetail(string='У вас недостаточно прав для выполнения данного действия.',
                                     code='permission_denied')}, response.data)
        self.assertEqual(2, Post.objects.all().count())
        self.assertEqual('test', self.post1.description)

    def test_update_not_author_but_staff(self):
        self.test_user2 = User.objects.create(username="test_user2", is_staff=True)
        url = reverse('posts-detail', args=(self.post1.slug,))
        data = {
            "h1": self.post1.h1,
            "title": self.post1.title,
            "slug": self.post1.slug,
            "description": "test description",
            "content": self.post1.content,
            "author": self.test_user.username
        }
        json_data = json.dumps(data)
        self.client.force_authenticate(self.test_user2)
        response = self.client.put(url, data=json_data, content_type="application/json")
        self.post1.refresh_from_db()
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(2, Post.objects.all().count())
        self.assertEqual('test description', self.post1.description)

    def test_delete_not_author(self):
        self.assertEqual(2, Post.objects.all().count())
        self.test_user2 = User.objects.create(username="test_user2")
        url = reverse('posts-detail', args=(self.post1.slug,))
        data = {
            "h1": self.post1.h1,
            "title": self.post1.title,
            "slug": self.post1.slug,
            "description": self.post1.description,
            "content": self.post1.content,
            "author": self.test_user.username
        }
        json_data = json.dumps(data)
        self.client.force_authenticate(self.test_user2)
        response = self.client.delete(url, data=json_data, content_type="application/json")
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual({'detail': ErrorDetail(string='У вас недостаточно прав для выполнения данного действия.',
                                     code='permission_denied')}, response.data)
        self.assertEqual(2, Post.objects.all().count())

    def test_delete_not_author_but_staff(self):
        self.assertEqual(2, Post.objects.all().count())
        self.test_user2 = User.objects.create(username="test_user2", is_staff=True)
        url = reverse('posts-detail', args=(self.post1.slug,))
        data = {
            "h1": self.post1.h1,
            "title": self.post1.title,
            "slug": self.post1.slug,
            "description": self.post1.description,
            "content": self.post1.content,
            "author": self.test_user.username
        }
        json_data = json.dumps(data)
        self.client.force_authenticate(self.test_user2)
        response = self.client.delete(url, data=json_data, content_type="application/json")
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(1, Post.objects.all().count())

class PostsRelationApiTestCase(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create(username="test_user")
        self.test_user2 = User.objects.create(username="test_user2")
        self.post1 = Post.objects.create(h1='test post 1', title='post1', slug='post1', description='test',
                                         content='user', author=self.test_user)
        self.post2 = Post.objects.create(h1='test post 2', title='post2', slug='post2', description='test1',
                                         content='user1')
    def test_like(self):
        url = reverse('userpostrelation-detail', args=(self.post1.id,))

        data = {
            "like": True
        }
        json_data = json.dumps(data)
        self.client.force_authenticate(self.test_user)
        response = self.client.patch(url, data=json_data, content_type="application/json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relations = UserPostRelation.objects.get(user=self.test_user, post=self.post1)
        self.assertTrue(relations.like)

        data = {
            "is_favorites": True
        }
        json_data = json.dumps(data)
        response = self.client.patch(url, data=json_data, content_type="application/json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relations = UserPostRelation.objects.get(user=self.test_user, post=self.post1)
        self.assertTrue(relations.is_favorites)

    def test_rate(self):
        url = reverse('userpostrelation-detail', args=(self.post1.id,))

        data = {
            "rate": 2
        }
        json_data = json.dumps(data)
        self.client.force_authenticate(self.test_user)
        response = self.client.patch(url, data=json_data, content_type="application/json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relations = UserPostRelation.objects.get(user=self.test_user, post=self.post1)
        self.assertEqual(2, relations.rate)

    def test_rate_wrong(self):
        url = reverse('userpostrelation-detail', args=(self.post1.id,))

        data = {
            "rate": 6
        }
        json_data = json.dumps(data)
        self.client.force_authenticate(self.test_user)
        response = self.client.patch(url, data=json_data, content_type="application/json")
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        relations = UserPostRelation.objects.get(user=self.test_user, post=self.post1)
        self.assertEqual(None, relations.rate)
