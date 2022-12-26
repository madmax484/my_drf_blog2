import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from taggit.models import Tag

from core.models import Post
from core.serializers import PostSerializer, TagSerializer, ContactSerializer, RegisterSerializer


class PostSerializerTestCase(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user('user')
        self.post1 = Post.objects.create(h1='test post 1', title='post1', slug='post1', description='test',
                                         content='user', author=self.test_user)
        self.post2 = Post.objects.create(h1='test post 2', title='post2', slug='post2', description='test1',
                                         content='user1', author=self.test_user)
    def test_ok(self):
        data = PostSerializer([self.post1, self.post2], many=True).data
        expected_data = [
            {
                'id': self.post1.id,
                'h1': 'test post 1',
                'title': 'post1',
                'slug': 'post1',
                'description': 'test',
                'content': 'user',
                'image': None,
                'created_at': datetime.date.today().strftime('%Y-%m-%d'),
                'author': 'user',
                'tags': []
            },
            {
                'id': self.post2.id,
                'h1': 'test post 2',
                'title': 'post2',
                'slug': 'post2',
                'description': 'test1',
                'content': 'user1',
                'image': None,
                'created_at': datetime.date.today().strftime('%Y-%m-%d'),
                'author': 'user',
                'tags': []
            }
        ]
        self.assertEqual(expected_data, data)


class TagSerializerTestCase(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name='tag')
        self.tag1 = Tag.objects.create(name='tag1')
    def test_tag(self):
        expected_data = [
            {
                'name': 'tag',
                'slug': 'tag'
            },
            {
                'name': 'tag1',
                'slug': 'tag1'
            }
        ]
        data = TagSerializer([self.tag, self.tag1], many=True).data
        self.assertEqual(expected_data, data)


class ContactSerializerTestCase(TestCase):
    def setUp(self):
        self.user = {
            'name': 'user',
            'email': 'user@mail.ru',
            'subject': 'theme',
            'message': 'message'
        }
        self.user1 = {
            'name': 'user1',
            'email': 'user1@mail.ru',
            'subject': 'theme1',
            'message': 'message1'
        }
    def test_contact(self):
        expected_data = [
            {
                'name': 'user',
                'email': 'user@mail.ru',
                'subject': 'theme',
                'message': 'message'
            },
            {
                'name': 'user1',
                'email': 'user1@mail.ru',
                'subject': 'theme1',
                'message': 'message1'
            }
        ]
        data = ContactSerializer([self.user, self.user1], many=True).data
        self.assertEqual(expected_data, data)


class RegisterSerializerTestCase(TestCase):
    def setUp(self):
        self.user = {
            'username': 'user',
            'password': '123',
            'password2': '123'
        },
        self.user1 = {
            'username': 'user1',
            'password': '321',
            'password2': '321'
        }
    def test_register(self):
        expected_data = [
            {
                "username": 'user',
                "password": '123',
                "password2": '123'
            },
            {
                "username": 'user1',
                "password": '321',
                "password2": '321'
            }
        ]
        data = RegisterSerializer([self.user])
        print(data)
