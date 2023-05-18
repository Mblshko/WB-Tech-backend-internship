from django.contrib import admin

from .models import Article, ReadArticle


admin.site.register(Article)
admin.site.register(ReadArticle)