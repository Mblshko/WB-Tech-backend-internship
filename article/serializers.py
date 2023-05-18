from rest_framework import serializers

from article.models import Article, ReadArticle


class ReadPostSerializer(serializers.ModelSerializer):
    article = serializers.ReadOnlyField(source='article.title')
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = ReadArticle
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'author']
