from django.contrib.auth.models import User
from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название статьи')
    content = models.TextField(max_length=10000, verbose_name='Текст статьи')
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True, verbose_name='Опубликовать?')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles', verbose_name='Автор')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Ститья'
        verbose_name_plural = 'Статьи'


class ReadArticle(models.Model):
    article = models.ForeignKey(Article, related_name='read', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    read = models.BooleanField(default=False, verbose_name='Прочитано')

    class Meta:
        verbose_name = 'Прочитанный пост'
        verbose_name_plural = 'Прочитанные посты'
