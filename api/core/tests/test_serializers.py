import datetime

from django.contrib.auth.models import User
from django.db.models import Count, Case, When, Avg
from django.test import TestCase
from django.utils import timezone
from taggit.models import Tag

from core.models import Post, Comment, UserPostRelation
from core.serializers import PostSerializer, TagSerializer, ContactSerializer, RegisterSerializer, UserSerializer, \
    CommentSerializer


class PostSerializerTestCase(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(username='user',
                                                  first_name='Mark', last_name='Shagal')
        self.test_user2 = User.objects.create_user(username='user2',
                                                  first_name='Mark', last_name='Ivanov')
        self.test_user3 = User.objects.create_user(username='user3',
                                                  first_name='Ivan', last_name='Markov')

        self.post1 = Post.objects.create(h1='test post 1', title='post1', slug='post1', description='test',
                                         content='user', author=self.test_user)
        self.post2 = Post.objects.create(h1='test post 2', title='post2', slug='post2', description='test1',
                                         content='user1', author=self.test_user)

        UserPostRelation.objects.create(user=self.test_user, post=self.post1, like=True, rate=4)
        UserPostRelation.objects.create(user=self.test_user2, post=self.post1, like=True, rate=4)
        UserPostRelation.objects.create(user=self.test_user3, post=self.post1, like=False, rate=5)

        UserPostRelation.objects.create(user=self.test_user, post=self.post2, like=True)
        UserPostRelation.objects.create(user=self.test_user2, post=self.post2, like=False, rate=4)
        UserPostRelation.objects.create(user=self.test_user3, post=self.post2, like=False)

    def test_ok(self):
        posts = Post.objects.all().annotate(annotated_likes=Count(Case(When(userpostrelation__like=True, then=1))),
                                            rating=Avg('userpostrelation__rate')
                                            )
        data = PostSerializer(posts, many=True).data
        expected_data = [
            {
                'id': self.post1.id,
                'h1': 'test post 1',
                'title': 'post1',
                'slug': 'post1',
                'description': 'test',
                'content': 'user',
                'image': None,
                'created_at': str(timezone.localdate()),
                'appreciated': [
                    {
                        'first_name': 'Mark',
                        'last_name': 'Shagal'
                    },
                    {
                        'first_name': 'Mark',
                        'last_name': 'Ivanov'
                    },
                    {
                        'first_name': 'Ivan',
                        'last_name': 'Markov'
                    }
                ],
                'author': 'user',
                'tags': [],
                # 'like_count': 2,
                'annotated_likes': 2,
                'rating': '4.33'
            },
            {
                'id': self.post2.id,
                'h1': 'test post 2',
                'title': 'post2',
                'slug': 'post2',
                'description': 'test1',
                'content': 'user1',
                'image': None,
                'created_at': str(timezone.localdate()),
                'appreciated': [
                    {
                        'first_name': 'Mark',
                        'last_name': 'Shagal'
                    },
                    {
                        'first_name': 'Mark',
                        'last_name': 'Ivanov'
                    },
                    {
                        'first_name': 'Ivan',
                        'last_name': 'Markov'
                    }
                ],
                'author': 'user',
                'tags': [],
                # 'like_count': 1,
                'annotated_likes': 1,
                'rating': '4.00'
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
        }
    def test_register(self):
        expected_data = {
                "username": 'user',
                "password": '123',
                "password2": '123'
            }
        data = RegisterSerializer().create(self.user)
        self.assertEqual(expected_data['username'], data.get_username())


class UserSerializerTestCase(TestCase):
    def setUp(self):
        self.test_user = {
            'username': 'user1',
            'password': '123'
        }
    def test_user(self):
        expected_data = {
            'username': 'user1',
            'last_login': None,
            'password': '123'
        }
        data = UserSerializer(self.test_user).data
        self.assertEqual(expected_data, data)


class CommentSerializerTestCase(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(username='test user')
        self.post1 = Post.objects.create(h1='test post 1', title='post1', slug='post1', description='test',
                                             content='user', author=self.test_user)
        self.comment = CommentSerializer().create({'username': self.test_user, 'post': self.post1,
                                             'text': 'text comment'})

    def test_comment(self):
        expected_data = {
            'id': 1,
            'username': 'test user',
            'post': 'post1',
            'text': 'text comment',
            'created_date': datetime.date.today().strftime('%Y-%m-%d')
        }
        data = CommentSerializer(self.comment).data
        self.assertEqual(expected_data, data)
        self.assertEqual(1, Comment.objects.all().count())

