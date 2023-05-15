from django.contrib.auth.models import User

from rest_framework import serializers
from article.models import Article


class UserSerializer(serializers.ModelSerializer):
    articles = serializers.SlugRelatedField(slug_field='title', many=True, queryset=Article.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'articles']

