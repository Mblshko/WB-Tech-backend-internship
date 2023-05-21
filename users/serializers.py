from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from article.models import Article
from .models import Subscribe


class UserSerializer(serializers.ModelSerializer):
    articles = serializers.SlugRelatedField(slug_field='title', many=True, queryset=Article.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'articles']


class SubscribeSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(source='user.id')
    author = serializers.IntegerField(source='author.id')

    class Meta:
        model = Subscribe
        fields = ['user', 'author']

    def validate(self, attr):
        user = attr['user']['id']
        author = attr['author']['id']
        if user == author:
            raise ValidationError({'error': 'Нельзя подписаться на самого себя'})
        if len(Subscribe.objects.filter(user=user, author=author)) >= 1:
            raise ValidationError({'error': 'Вы уже подписаны'})
        author = User.objects.filter(pk=author)
        if not author:
            raise ValidationError({'error': 'Такого пользователя несуществует'})
        return attr

    def create(self, validated_data):
        user_id = validated_data['user']['id']
        author_id = validated_data['author']['id']
        user = User.objects.get(pk=user_id)
        author = User.objects.get(pk=author_id)
        return Subscribe.objects.create(user=user, author=author)
