from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from .models import Article
from .serializers import ArticleSerializer


class ArticleTests(APITestCase):
    '''Тестирование Articles и ReadArticle'''
    def setUp(self):
        self.user_test1 = User.objects.create_user(username='user_test1', password='qwer1234')
        self.token_user_test1 = Token.objects.create(user=self.user_test1)

        self.article = Article.objects.create(title='Test', content='Content Test', author=self.user_test1)
        self.article_data = {'title': self.article.title, 'content': self.article.content}

    def test_article_list(self):
        response = self.client.get(reverse('articles_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_article_detail(self):
        response = self.client.get(reverse('article_detail', kwargs={'pk': self.article.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serialaizer_data = ArticleSerializer(self.article).data
        self.assertEqual(serialaizer_data, response.data)

    def test_article_create_invalid(self):
        response = self.client.post(reverse('articles_list'), self.article_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_article_create_valid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user_test1.key)
        response = self.client.post(reverse('articles_list'), self.article_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_read_article(self):
        response = self.client.post(reverse('article_read', kwargs={'pk': self.article.id}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user_test1.key)
        response = self.client.post(reverse('article_read', kwargs={'pk': self.article.id}))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(reverse('article_read', kwargs={'pk': self.article.id}))
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
