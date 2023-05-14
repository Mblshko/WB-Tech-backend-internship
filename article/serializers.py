from rest_framework import serializers

from article.models import Article, ReadPost


# class ReadPostSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = ReadPost
#         fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Article
        fields = '__all__'
